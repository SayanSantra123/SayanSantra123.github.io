"""
Cryptography Handler Module
Handles AES-256 encryption and decryption of images
"""

import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io


class CryptoHandler:
    """Handles encryption and decryption operations"""

    def __init__(self, password):
        """
        Initialize crypto handler with password

        Args:
            password: Password for encryption/decryption
        """
        # Derive 256-bit key from password using SHA-256
        self.key = hashlib.sha256(password.encode('utf-8')).digest()

    def encrypt_image(self, image_path, output_path=None):
        """
        Encrypt an image file

        Args:
            image_path: Path to input image
            output_path: Path for encrypted output (optional)

        Returns:
            Path to encrypted image file
        """
        # Generate output path if not provided
        if output_path is None:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_encrypted.png" # force png

        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Generate random IV (Initialization Vector)
        iv = get_random_bytes(16)

        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Pad and encrypt data
        padded_data = pad(image_data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        # Combine IV and encrypted data
        final_data = iv + encrypted_data

        # Prepend the length of the data
        final_data = len(final_data).to_bytes(4, 'big') + final_data

        # Convert data to a binary image
        encrypted_image = self._data_to_image_binary(final_data)
        encrypted_image.save(output_path)

        return output_path

    def decrypt_image(self, encrypted_path, output_path=None):
        """
        Decrypt an encrypted image file

        Args:
            encrypted_path: Path to encrypted image
            output_path: Path for decrypted output (optional)

        Returns:
            Path to decrypted image file
        """
        # Generate output path if not provided
        if output_path is None:
            base, ext = os.path.splitext(encrypted_path)
            output_path = f"{base}_decrypted{ext}"

        # Read encrypted image
        encrypted_image = Image.open(encrypted_path)
        
        # Convert binary image to data
        encrypted_bytes = self._image_to_data_binary(encrypted_image)

        # Extract the length of the data
        try:
            data_len = int.from_bytes(encrypted_bytes[:4], 'big')
            
            # Extract the actual data
            final_data = encrypted_bytes[4:4+data_len]

            # Extract IV (first 16 bytes)
            iv = final_data[:16]
            encrypted_data = final_data[16:]
        except (IndexError, ValueError) as e:
            raise ValueError("Decryption failed. Corrupted data.") from e


        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Decrypt and unpad
        try:
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
        except ValueError as e:
            raise ValueError("Decryption failed. Wrong key or corrupted data.") from e

        # Write decrypted image
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        return output_path

    def decrypt_data(self, encrypted_data, output_path=None):
        """
        Decrypt encrypted data

        Args:
            encrypted_data: Encrypted data as bytes
            output_path: Path for decrypted output (optional)

        Returns:
            Path to decrypted image file
        """
        # Extract the length of the data
        try:
            data_len = int.from_bytes(encrypted_data[:4], 'big')
            
            # Extract the actual data
            final_data = encrypted_data[4:4+data_len]

            # Extract IV (first 16 bytes)
            iv = final_data[:16]
            encrypted_data_payload = final_data[16:]
        except (IndexError, ValueError) as e:
            raise ValueError("Decryption failed. Corrupted data.") from e


        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Decrypt and unpad
        try:
            decrypted_padded = cipher.decrypt(encrypted_data_payload)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
        except ValueError as e:
            raise ValueError("Decryption failed. Wrong key or corrupted data.") from e

        # Generate output path if not provided
        if output_path is None:
            output_path = 'decrypted_output.png'

        # Write decrypted image
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        return output_path

    def _data_to_image_binary(self, data):
        """
        Convert bytes to a binary PIL Image

        Args:
            data: Bytes to convert

        Returns:
            PIL Image object
        """
        # Convert data to a string of bits
        bits = ''.join(format(byte, '08b') for byte in data)

        width, height = 320, 256
        total_pixels = width * height

        # Create a new image
        image = Image.new('1', (width, height))
        pixels = image.load()

        # Set pixels based on bits
        for i in range(total_pixels):
            if i < len(bits):
                if bits[i] == '1':
                    pixels[i % width, i // width] = 255
                else:
                    pixels[i % width, i // width] = 0
            else:
                pixels[i % width, i // width] = 0
        
        return image.convert('RGB')


    def _image_to_data_binary(self, image):
        """
        Convert binary PIL Image back to bytes

        Args:
            image: PIL Image object

        Returns:
            Bytes representation
        """
        # Convert image to black and white
        image = image.convert('1', dither=Image.NONE)
        pixels = image.load()
        width, height = image.size

        bits = ""
        for y in range(height):
            for x in range(width):
                if pixels[x, y] > 0:
                    bits += '1'
                else:
                    bits += '0'

        # Convert bits to bytes
        data = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                try:
                    data.append(int(byte, 2))
                except ValueError:
                    # This can happen if the bits string is not a valid binary representation
                    # For simplicity, we'll just append a 0 byte
                    data.append(0)

        return bytes(data)

    def _bytes_to_image(self, data):
        """
        Convert bytes to PIL Image

        This creates a visual representation of encrypted data
        that can be transmitted via SSTV.

        Args:
            data: Bytes to convert

        Returns:
            PIL Image object
        """
        # Calculate image dimensions
        # Standard SSTV resolution
        width, height = 320, 256
        total_pixels = width * height

        # We need 3 bytes per pixel (RGB)
        required_bytes = total_pixels * 3

        # Pad or truncate data to fit
        if len(data) < required_bytes:
            # Pad with zeros
            data = data + bytes(required_bytes - len(data))
        else:
            # Truncate
            data = data[:required_bytes]

        # Convert to numpy array and reshape
        import numpy as np
        arr = np.frombuffer(data, dtype=np.uint8)
        arr = arr.reshape((height, width, 3))

        # Create image
        image = Image.fromarray(arr, 'RGB')

        return image

    def _image_to_bytes(self, image):
        """
        Convert PIL Image back to bytes

        Args:
            image: PIL Image object

        Returns:
            Bytes representation
        """
        import numpy as np

        # Convert image to array
        arr = np.array(image)

        # Flatten and convert to bytes
        data = arr.flatten().tobytes()

        return data

    @staticmethod
    def generate_random_key(length=32):
        """
        Generate a random encryption key

        Args:
            length: Key length in bytes (default: 32 for AES-256)

        Returns:
            Random key as hex string
        """
        key = get_random_bytes(length)
        return key.hex()