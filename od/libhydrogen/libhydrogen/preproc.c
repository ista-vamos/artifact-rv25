#include <assert.h>
#include <immintrin.h> /* _mm_pause */
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <threads.h>
#include <time.h>
#include <unistd.h>

#include "vamos-buffers/core/arbiter.h"
#include "vamos-buffers/core/event.h"
#include "vamos-buffers/core/signatures.h"
#include "vamos-buffers/core/stream.h"
#include "vamos-buffers/streams/streams.h"
#include "vamos-buffers/streams/stream-generic.h"

#define SLEEP_NS_INIT (50)
#define SLEEP_THRESHOLD_NS (10000000)

static vms_stream *
create_stream(int argc, char *argv[], int arg_i,
              const char *expected_stream_name,
              const vms_stream_hole_handling *hole_handling) {
    assert(arg_i < argc && "Index too large");

    char streamname[256];
    vms_stream *stream;
    const char *dc = strchr(argv[arg_i], ':');
    if (!dc) {
      printf("Only SHM key given, assuming 'generic' stream and giving it the "
             "name 'stream-%d'\n",
             arg_i);
      sprintf(streamname, "stream-%d", arg_i);
      stream =
          vms_create_generic_stream(argv[arg_i], streamname, hole_handling);
    } else {
      strncpy(streamname, argv[arg_i], dc - argv[arg_i]);
      streamname[dc - argv[arg_i]] = 0;
      stream =
          vms_stream_create_from_argv(streamname, argc, argv, hole_handling);
    }

    if (!stream) {
      fprintf(stderr, "Failed creating stream: %s\n", argv[arg_i]);
      return NULL;
    }

    if (expected_stream_name &&
        strcmp(vms_stream_get_name(stream), expected_stream_name) != 0) {
        fprintf(stderr,
                "A wrong source was specified for this monitor.\n"
                "Got '%s' but expected '%s'",
                vms_stream_get_name(stream), expected_stream_name);
        vms_stream_destroy(stream);
        return NULL;
    }

    return stream;
}

static int buffer_manager_thrd(void *data) {
    vms_arbiter_buffer *buffer = (vms_arbiter_buffer *)data;
    vms_stream *stream = vms_arbiter_buffer_stream(buffer);

    // wait for buffer->active
    while (!vms_arbiter_buffer_active(buffer)) _mm_pause();

    printf("Running fetch & autodrop for stream %s\n",
           vms_stream_get_name(stream));

    const size_t ev_size = vms_stream_event_size(stream);
    void *ev, *out;
    while (1) {
        ev = vms_stream_fetch_dropping(stream, buffer);
        if (!ev) {
            break;
        }

        out = vms_arbiter_buffer_write_ptr(buffer);
        assert(out && "No space in the buffer");
        memcpy(out, ev, ev_size);
        vms_arbiter_buffer_write_finish(buffer);
        vms_stream_consume(stream, 1);
    }

    // TODO: we should check if the stream is finished and remove it
    // in that case
    printf("BMM for stream %lu (%s) exits\n", vms_stream_id(stream),
           vms_stream_get_name(stream));
    thrd_exit(EXIT_SUCCESS);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "USAGE: prog source-spec\n");
        return -1;
    }

    vms_stream *stream = create_stream(argc, argv, 1, NULL, NULL);
    assert(stream && "Creating stream failed");

    vms_stream_register_all_events(stream);
    vms_stream_dump_events(stream);

    vms_arbiter_buffer *buffer =
        vms_arbiter_buffer_create(stream, vms_stream_event_size(stream),
                                  /*capacity=*/4 * 4096);
    thrd_t tid;
    thrd_create(&tid, buffer_manager_thrd, (void *)buffer);
    vms_arbiter_buffer_set_active(buffer, true);

    size_t n = 0, tmp, trials = 0;
    while (1) {
        tmp = vms_arbiter_buffer_size(buffer);
        if (tmp > 0) {
            n += vms_arbiter_buffer_drop(buffer, tmp);
            trials = 0;
        } else {
            ++trials;
        }

        if (trials > 1000) {
            if (!vms_stream_is_ready(stream))
                break;
        }
    }
    printf("Processed %lu events\n", n);

    thrd_join(tid, NULL);

    vms_stream_destroy(stream);
    vms_arbiter_buffer_free(buffer);

    return 0;
}
