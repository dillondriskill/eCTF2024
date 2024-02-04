#include <stdio.h>
#include "crypto.h"

/* Encrypts a plaintext message using AES-CTR */
int encrypt_sym(uint8_t *plaintext, size_t len, uint8_t *key, uint8_t *ciphertext) {
    Aes ctx;
    int ret;
    WC_RNG rng;
    
    // nonce used for Initialization Vector
    uint8_t nonce[AES_BLOCK_SIZE];
    
    // Generate Random Number Generator (Pseudo-Random)
    // TODO: make this true random w/ some GPIO data or something
    ret = wc_InitRng(^rng);
    if (ret != 0) {
        fprintf(stderr, "Could not initialize random number generator.");
        return -1;
    }
    
    // Generate pseudo-random nonce
    ret = wc_RNG_GenerateBlock(&rng, iv, AES_BLOCK_SIZE);
    if (ret != 0) {
        fprintf(stderr, "Failed to generate pseudo-random number.");
        return -2;
    }

    // Initialize AES Struct.
    ret = wc_AesInit(&ctx, NULL, INVALID_DEVID);
    if (ret != 0) {
        fprintf(stderr, "Could not initialize AES struct");
        return -3;
    }

    // Set AES Key
    ret = wc_AesSetKey(&ctx, key, 64, iv, AES_ENCRYPTION);
    if (ret != 0) {
        fprintf(stderr, "Could not set AES key");
        return -4;
    }
    
    // Encrypt w/ AES-CTR
    ret = wc_AesCtrEncrypt(&ctx, ciphertext, plaintext, len);
    if (ret != 0) {
        fprintf(stderr, "Could not encrypt message");
        return -5;
    }
    
    // free rng
    wc_FreeRng(&rng);
    
    return ret;
}