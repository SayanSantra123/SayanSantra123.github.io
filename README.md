# SSTV Audio Transceiver with Encryption

A Python application for transmitting and receiving images and text via **SSTV (Slow-Scan Television)** audio signals with **AES-256 encryption**.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### 🔐 Security
- **AES-256 encryption** for all transmitted data
- Password-based key derivation using SHA-256
- Secure encryption before SSTV encoding

### 📡 SSTV Transmission
- Multiple SSTV modes supported (Martin M1/M2, Scottie S1/S2)
- Encode images and text to SSTV audio
- Real-time audio playback
- Save SSTV audio files for later transmission

### 🎤 Reception & Decoding
- Record audio from microphone
- Load pre-recorded audio files
- Automatic SSTV decoding
- Decrypt received data with key

### 🎨 User-Friendly Interface
- Clean and intuitive GUI built with Tkinter
- Separate sender and receiver modes
- Real-time status updates
- Visual output display

### 🤖 Future AI Enhancement
- Framework for AI-powered image enhancement
- Placeholder for super-resolution integration
- Noise reduction capabilities
- Artifact correction support

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone (for receiving mode)
- Audio output device (for transmitting mode)

### Step 1: Clone or Download
```bash
# Download the project files to your computer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Note for PyAudio Installation
PyAudio may require additional system dependencies:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Usage

### Starting the Application
```bash
python sstv_transceiver_main.py
```

### Sender Mode

1. **Select Mode**: Choose "Sender Mode"

2. **Choose Data Type**:
   - **Image**: Browse and select an image file (PNG, JPG, etc.)
   - **Text**: Enter text message (will be converted to image)

3. **Enter Encryption Key**: 
   - Type a strong password
   - Remember this key - you'll need it to decrypt!

4. **Generate SSTV Audio**:
   - Click "Generate & Play SSTV Audio" to play immediately
   - Or "Save SSTV Audio File" to save for later

5. **Transmission**:
   - Play the audio near a radio transmitter
   - Or send the audio file to someone

### Receiver Mode

1. **Select Mode**: Choose "Receiver Mode"

2. **Capture Audio**:
   - **Record from Microphone**: Click to record SSTV audio (60 seconds max)
   - **Load Audio File**: Select a pre-recorded WAV file

3. **Enter Decryption Key**:
   - Enter the same password used for encryption

4. **Decode**:
   - Click "Decode & Decrypt SSTV Signal"
   - View the decoded image/text in the output display

## Project Structure

```
sstv-transceiver/
│
├── sstv_transceiver_main.py   # Main application GUI
├── sstv_encoder.py             # SSTV encoding module
├── sstv_decoder.py             # SSTV decoding module
├── crypto_handler.py           # Encryption/decryption module
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Technical Details

### SSTV Encoding
- Uses PySSTV library for SSTV signal generation
- Supports standard SSTV modes (Martin M1 default)
- Resolution: 320x256 pixels
- Audio format: WAV, 48kHz, 16-bit

### Encryption
- Algorithm: AES-256-CBC
- Key derivation: SHA-256 hash of password
- Encrypted data is converted to image format for SSTV transmission
- IV (Initialization Vector) prepended to encrypted data

### Decoding
- Bandpass filtering (1100-2500 Hz) for noise reduction
- FFT-based frequency detection
- Converts audio frequencies back to pixel values
- Frequency mapping: 1500 Hz (black) to 2300 Hz (white)

## Future Enhancements

### AI Image Enhancement (Coming Soon)
The application includes hooks for future AI integration:

- **Super-Resolution**: Upscale low-resolution decoded images
- **Denoising**: Remove transmission noise using neural networks
- **Artifact Correction**: Fix SSTV decoding artifacts
- **Quality Enhancement**: Improve overall image quality

To add AI enhancement in the future:
1. Install PyTorch or TensorFlow
2. Download pre-trained models (ESRGAN, Real-ESRGAN, etc.)
3. Implement in `sstv_decoder.apply_ai_enhancement()`

## Troubleshooting

### No Audio Output
- Check audio output device is working
- Verify volume is not muted
- Try a different SSTV mode

### Microphone Not Recording
- Grant microphone permissions to Python
- Check default audio input device
- Test with a longer recording duration

### Decryption Fails
- Ensure the same key is used for encryption and decryption
- Verify the audio file is not corrupted
- Check that the SSTV mode matches

### PyAudio Installation Issues
- Refer to PyAudio documentation for platform-specific installation
- Consider using alternative audio libraries if issues persist

## Known Limitations

1. **Decoder Accuracy**: The built-in SSTV decoder is simplified. For production use, consider integrating specialized libraries like slowrx or QSSTV.

2. **Noise Sensitivity**: Audio quality significantly affects decoding accuracy. Use in quiet environments or with clean audio files.

3. **Transmission Speed**: SSTV is slow by design (1-2 minutes per image). This is intentional for radio transmission.

4. **Image Quality**: Due to SSTV's limited bandwidth, expect some quality loss compared to original images.

## Security Considerations

- **Strong Passwords**: Use complex, unique passwords for encryption
- **Key Management**: Store encryption keys securely
- **Transmission Security**: SSTV audio can be intercepted; encryption is essential
- **No Perfect Security**: This is a hobbyist/educational project, not certified for high-security applications

## Contributing

Contributions are welcome! Areas for improvement:
- Better SSTV decoding algorithms
- Additional SSTV modes
- AI enhancement integration
- Error correction codes
- Improved noise reduction

## License

MIT License - feel free to use, modify, and distribute

## Acknowledgments

- **PySSTV**: For SSTV encoding functionality
- **PyCryptodome**: For encryption capabilities
- **Amateur Radio Community**: For SSTV specifications

## References

- [SSTV Information](http://www.barberdsp.com/downloads/Dayton%20Paper.pdf)
- [PySSTV GitHub](https://github.com/dnet/pySSTV)
- [SSTV Handbook](https://www.sstv-handbook.com/)

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Enjoy your SSTV adventures! 📡🔐📻**
