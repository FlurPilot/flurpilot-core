/**
 * FlurPilot Crypto Library (Zero Knowledge)
 * Implements "Werner's Digital Sticky Note" Encryption.
 * 
 * Standards:
 * - Data Encryption: AES-GCM-256
 * - Key Derivation: PBKDF2 (SHA-256, 100k iterations)
 * - Key Wrapping: AES-KW or RSA-OAEP (for Recovery Key)
 */

export interface EncryptedNotePacket {
    ciphertext: string;       // Base64
    iv: string;              // Base64
    wrappedKeyUser: string;   // Base64 (Wrapped with User Pwd)
    wrappedKeyOrg?: string;   // Base64 (Wrapped with Org Public Key)
    salt: string;            // Base64 (PBKDF2 Salt)
}

// 1. Generate a random Note Key (AES-GCM)
export async function generateNoteKey(): Promise<CryptoKey> {
    return window.crypto.subtle.generateKey(
        {
            name: "AES-GCM",
            length: 256
        },
        true,
        ["encrypt", "decrypt"]
    );
}

// 2. Derive User Key from Password
export async function deriveKeyFromPassword(password: string, salt: Uint8Array): Promise<CryptoKey> {
    const enc = new TextEncoder();
    const keyMaterial = await window.crypto.subtle.importKey(
        "raw",
        enc.encode(password),
        "PBKDF2",
        false,
        ["deriveBits", "deriveKey"]
    );

    return window.crypto.subtle.deriveKey(
        {
            name: "PBKDF2",
            salt: salt as BufferSource,
            iterations: 100000,
            hash: "SHA-256"
        },
        keyMaterial,
        { name: "AES-GCM", length: 256 },
        true,
        ["encrypt", "decrypt", "wrapKey", "unwrapKey"]
    );
}

// 3. Encrypt the Note Text
export async function encryptNoteText(text: string, noteKey: CryptoKey): Promise<{ ciphertext: string, iv: string }> {
    const enc = new TextEncoder();
    const iv = window.crypto.getRandomValues(new Uint8Array(12));

    const encrypted = await window.crypto.subtle.encrypt(
        {
            name: "AES-GCM",
            iv: iv
        },
        noteKey,
        enc.encode(text)
    );

    return {
        ciphertext: arrayBufferToBase64(encrypted),
        iv: arrayBufferToBase64(iv.buffer as ArrayBuffer)
    };
}

// 4. Wrap the Note Key (Virtual Envelope)
export async function wrapNoteKey(noteKey: CryptoKey, wrappingKey: CryptoKey): Promise<string> {
    // We use AES-GCM for wrapping in this simple architecture
    // AES-GCM wrap requires IV.

    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const wrapped = await window.crypto.subtle.wrapKey(
        "raw",
        noteKey,
        wrappingKey,
        { name: "AES-GCM", iv: iv }
    );

    // Concat IV + Wrapped Key for storage
    const combined = new Uint8Array(iv.length + wrapped.byteLength);
    combined.set(iv);
    combined.set(new Uint8Array(wrapped), iv.length);

    return arrayBufferToBase64(combined.buffer);
}

// 5. Decrypt Note (The Reverse)
export async function decryptNotePacket(packet: EncryptedNotePacket, password: string): Promise<string> {
    // A. Derive User Key
    const salt = base64ToArrayBuffer(packet.salt);
    const userKey = await deriveKeyFromPassword(password, new Uint8Array(salt));

    // B. Unwrap Note Key
    const wrappedData = base64ToArrayBuffer(packet.wrappedKeyUser);
    const iv = wrappedData.slice(0, 12);
    const ciphertextKey = wrappedData.slice(12);

    try {
        const noteKey = await window.crypto.subtle.unwrapKey(
            "raw",
            ciphertextKey,
            userKey,
            { name: "AES-GCM", iv: new Uint8Array(iv) },
            { name: "AES-GCM", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );

        // C. Decrypt Content
        const contentIV = base64ToArrayBuffer(packet.iv);
        const contentCipher = base64ToArrayBuffer(packet.ciphertext);

        const decrypted = await window.crypto.subtle.decrypt(
            { name: "AES-GCM", iv: new Uint8Array(contentIV) },
            noteKey,
            contentCipher
        );

        return new TextDecoder().decode(decrypted);

    } catch {
        throw new Error("Decryption failed. Wrong password or corrupted data.");
    }
}


// Check if Recovery Public Key is present (Mock for now)
export const ORG_PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...mock...
-----END PUBLIC KEY-----`;


// Helpers
function arrayBufferToBase64(buffer: ArrayBuffer): string {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

function base64ToArrayBuffer(base64: string): ArrayBuffer {
    const binary_string = window.atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer as ArrayBuffer;
}

export function generateSalt(): string {
    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    return arrayBufferToBase64(salt.buffer as ArrayBuffer);
}
