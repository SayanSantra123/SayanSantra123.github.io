"""
Test Script for Data-over-Audio Transceiver
Run this to verify all components are working
"""

import sys
import os
import hashlib

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    modules = [
        ('amodem', 'amodem'),
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('pyaudio', 'PyAudio'),
        ('scipy', 'scipy'),
        ('Crypto', 'pycryptodome'),
        ('tkinter', 'tkinter (built-in)'),
    ]

    missing = []
    for module, name in modules:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            missing.append(name)

    if missing:
        print(f"\nMissing modules: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    print("\n✓ All required modules are installed!\n")
    return True

def test_end_to_end():
    """Test end-to-end encoding and decoding"""
    print("\nTesting end-to-end transmission...")
    try:
        from data_encoder import DataEncoder
        from data_decoder import DataDecoder
        from crypto_handler import CryptoHandler
        from Crypto.Random import get_random_bytes
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad

        # Create random data
        original_data = get_random_bytes(1024)

        # Encrypt
        password = "test_password"
        crypto = CryptoHandler(password)
        iv = get_random_bytes(16)
        cipher = AES.new(crypto.key, AES.MODE_CBC, iv)
        padded_data = pad(original_data, AES.block_size)
        encrypted_data = iv + cipher.encrypt(padded_data)

        # Encode
        encoder = DataEncoder()
        audio_path = encoder.encode(encrypted_data)

        # Decode
        decoder = DataDecoder()
        decoded_data = decoder.decode(audio_path)

        # Decrypt
        iv_dec = decoded_data[:16]
        encrypted_data_dec = decoded_data[16:]
        cipher_dec = AES.new(crypto.key, AES.MODE_CBC, iv_dec)
        decrypted_padded = cipher_dec.decrypt(encrypted_data_dec)
        decrypted_data = unpad(decrypted_padded, AES.block_size)

        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)

        if original_data == decrypted_data:
            print("  ✓ End-to-end test passed!")
            return True
        else:
            print("  ✗ End-to-end test failed: Decrypted data does not match original data.")
            return False

    except Exception as e:
        print(f"  ✗ End-to-end test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("DATA-OVER-AUDIO TRANSCEIVER - SYSTEM TEST")
    print("="*60)
    print()

    tests = [
        test_imports,
        test_end_to_end
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append(False)
        print()

    print("="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")

    if all(results):
        print("\n✓ ALL TESTS PASSED!")
        print("\nYou can now run: python sstv_transceiver_main.py")
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")

    print("="*60)

if __name__ == "__main__":
    main()
