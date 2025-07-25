#include "hydrogen.h"
#include <stdio.h>
#include <string.h>

#define CONTEXT "Examples"

extern void __vamos_public_input(void *ptr, size_t size);
extern void __vamos_public_output(void *ptr, size_t size);

int main(int argc, char const* argv[])
{
    uint8_t key[hydro_secretbox_KEYBYTES];

    size_t mlen = strlen(argv[1]);
    char *message = malloc(mlen+1);
    __vamos_public_input(message, mlen);

    strcpy(message, argv[1]);

    const size_t CIPHERTEXT_LEN = hydro_secretbox_HEADERBYTES + mlen;
    uint8_t *ciphertext = malloc(CIPHERTEXT_LEN);

    __vamos_public_output(ciphertext, CIPHERTEXT_LEN);

   //fseek(fp, 0L, SEEK_SET);
   //fread(message, mlen, 1, fp);

//#pragma tainter taint(key)
//#pragma tainter sinktaint(message)

    hydro_secretbox_keygen(key);
    hydro_secretbox_encrypt(ciphertext, message, mlen, 0, CONTEXT, key);

    char *decrypted = malloc(mlen);
//#pragma tainter sinktaint(ciphertext)
    if (hydro_secretbox_decrypt(decrypted, ciphertext, CIPHERTEXT_LEN, 0, CONTEXT, key) != 0) {
        /* message forged! */
    }
    free(decrypted);
    free(ciphertext);

    return 0;
}
