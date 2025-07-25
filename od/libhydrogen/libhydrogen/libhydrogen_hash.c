#include "hydrogen.h"
#include <stdio.h>
#include <string.h>

#define CONTEXT "Examples"

extern void __vamos_public_input(void *ptr, size_t size);
extern void __vamos_public_output(void *ptr, size_t size);

int main(int argc, char const* argv[])
{
    size_t mlen = strlen(argv[1]);
    char *message = malloc(mlen+1);
    message[mlen] = 0;

    __vamos_public_input(message, mlen);
    memcpy(message, argv[1], mlen);

    uint8_t hash[hydro_hash_BYTES];
    __vamos_public_output(hash, hydro_hash_BYTES);

    printf("---\n");
    hydro_hash_hash(hash, sizeof hash, message, mlen, CONTEXT, NULL);
    printf("---\n");

    for (int i = 0; i < sizeof hash; ++i) {
	    printf("%p: %d\n", hash + i, hash[i]);
    }

    free(message);
    return 0;
}
