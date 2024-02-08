#include <stdio.h>
#include "../inc/crypto.h"

/* Encrypts a plaintext message using AES-CTR */
int encrypt_sym(uint8_t *plaintext, size_t len, uint8_t *key, uint8_t *ciphertext) {
    Aes ctx;
    int ret;
    WC_RNG rng;
    
    // nonce used for Initialization Vector
    uint8_t nonce[AES_BLOCK_SIZE];

    // Generate Random Number Generator (Pseudo-Random)
    // TODO: make this true random w/ some GPIO data or something
    ret = wc_InitRng(&rng);
    if (ret != 0) {
        fprintf(stderr, "Could not initialize random number generator.");
        return -1;
    }

    // Generate pseudo-random nonce
    ret = wc_RNG_GenerateBlock(&rng, nonce, AES_BLOCK_SIZE);
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
    ret = wc_AesSetKey(&ctx, key, 64, nonce, AES_ENCRYPTION);
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
    
    // Cleanup
    memset(key, 0, 64);
    wc_FreeRng(&rng);
    
    return ret;
}

int decrypt_sym(uint8_t *iv_cipher, size_t len, uint8_t *key, uint8_t *plaintext) {
    Aes ctx;
    int ret;
    
    uint8_t iv = iv_cipher;
    uint8_t ciphertext = iv_cipher + BLOCK_SIZE;
    
    // Initialize AES struct
    ret = wc_AesInit(&ctx, NULL, INVALID_DEVID);
    if (ret != 0) {
        fprintf(stderr, "Could not initialize AES Struct");
        return -1;
    }
    
    // Set the key
    // Decryption for CTR still uses the AES_ENCRYPTION
    ret = wc_AesSetKey(&ctx, key, 64, iv, AES_ENCRYPTION);
    if (ret != 0) {
        fprintf(stderr, "Could not set key");
        return -2;
    }

    // Decrypt
    // note: AesCtrEncrypt both encrypts and decrypts
    ret = wc_AesCtrDecrypt(&ctx, plaintext, ciphertext, len);
    if (ret != 0) {
        fprintf(stderr, "Could not decrypt");
        return -3;
    }

    // Cleanup
    memset(key, 0, 64);
}