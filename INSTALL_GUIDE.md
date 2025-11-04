# Installation & Setup Guide

## Quick Start

### Windows

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install PyAudio** (requires special steps on Windows)
   ```cmd
   pip install pipwin
   pipwin install pyaudio
   ```

3. **Install Other Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```cmd
   python sstv_transceiver_main.py
   ```

### macOS

1. **Install Python 3.8+**
   ```bash
   brew install python3
   ```

2. **Install PortAudio** (required for PyAudio)
   ```bash
   brew install portaudio
   ```

3. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python3 sstv_transceiver_main.py
   ```

### Linux (Ubuntu/Debian)

1. **Install Python 3.8+** (usually pre-installed)
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install PortAudio**
   ```bash
   sudo apt-get install portaudio19-dev
   ```

3. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python3 sstv_transceiver_main.py
   ```

## Detailed Usage Guide

### Sending Encrypted Messages

#### Step-by-Step: Image Transmission

1. Launch the application
2. Ensure "Sender Mode" is selected
3. Click "Browse Image" and select your image file
4. Enter a strong encryption key (e.g., "MySecretPassword123!")
5. Click "Generate & Play SSTV Audio"
6. The audio will play automatically - this is your encoded, encrypted image!
7. Optional: Click "Save SSTV Audio File" to save for later

#### Step-by-Step: Text Transmission

1. Launch the application
2. Select "Sender Mode"
3. Click "Enter Text"
4. Type your message in the text box
5. Click "Use This Text"
6. Enter your encryption key
7. Click "Generate & Play SSTV Audio"

### Receiving Encrypted Messages

#### Step-by-Step: Microphone Reception

1. Launch the application
2. Select "Receiver Mode"
3. Click "Record from Microphone"
4. Play the SSTV audio near your microphone
5. Wait for recording to finish (60 seconds max)
6. Enter the decryption key (same as sender used)
7. Click "Decode & Decrypt SSTV Signal"
8. View the decoded image in the output display

#### Step-by-Step: File Reception

1. Launch the application
2. Select "Receiver Mode"
3. Click "Load Audio File"
4. Select the WAV file containing SSTV audio
5. Enter the decryption key
6. Click "Decode & Decrypt SSTV Signal"
7. View the decoded result

## Tips for Best Results

### For Transmission
- Use clear, high-contrast images
- Avoid very detailed or noisy images
- Keep text messages short (under 1000 characters)
- Use a quiet environment when playing audio

### For Reception
- Use a good quality microphone
- Minimize background noise
- Keep microphone close to speaker
- Ensure good volume level (not too loud or too quiet)

### For Encryption
- Use strong, unique passwords
- Remember or securely store your encryption keys
- Different keys = different encrypted outputs
- Share keys securely with recipients

## Common Issues & Solutions

### "Module not found" Error
**Problem**: A required library is not installed
**Solution**: Run `pip install -r requirements.txt` again

### PyAudio Installation Fails
**Problem**: PyAudio requires system-level audio libraries
**Solution**:
- Windows: Use `pipwin install pyaudio`
- Mac: Install portaudio first with `brew install portaudio`
- Linux: Install portaudio19-dev first

### No Audio Plays
**Problem**: Audio output not working
**Solution**:
- Check system volume
- Verify default audio output device
- Try saving to file first, then play manually

### Microphone Not Recording
**Problem**: Can't record from microphone
**Solution**:
- Grant microphone permissions to Python
- Check default input device in system settings
- Test microphone with other applications first

### Decryption Fails
**Problem**: "Decryption failed" error
**Solution**:
- Verify you're using the correct encryption key
- Check that audio file is not corrupted
- Ensure complete audio was recorded

### Poor Decoded Image Quality
**Problem**: Decoded image looks noisy or distorted
**Solution**:
- Use cleaner audio source
- Reduce background noise during recording
- Try using a direct audio file instead of microphone
- Consider using the AI enhancement feature (when available)

## Testing the Application

### Quick Test

1. **Test Sender**:
   - Use a simple test image (e.g., a smiley face)
   - Key: "test123"
   - Save audio to "test_output.wav"

2. **Test Receiver**:
   - Load "test_output.wav"
   - Key: "test123"
   - Decode and verify output

### Audio Loop Test
- Connect speaker output to microphone input (carefully!)
- Generate and play SSTV audio
- Simultaneously record with receiver
- Decode and verify

## Advanced Configuration

### Changing SSTV Mode
Edit `sstv_encoder.py`:
```python
def __init__(self, mode='MartinM1'):  # Change to MartinM2, ScottieS1, etc.
```

### Adjusting Recording Duration
Edit `sstv_decoder.py`:
```python
def record_from_microphone(self, duration=60):  # Change duration
```

### Custom Image Resolution
Edit both encoder and decoder to match custom dimensions.

## Performance Notes

- **Encoding Time**: 1-5 seconds per image
- **Audio Duration**: 1-2 minutes depending on SSTV mode
- **Decoding Time**: 5-15 seconds
- **File Sizes**: WAV files are typically 5-10 MB

## Next Steps

1. Experiment with different images and text
2. Try different SSTV modes for speed vs quality
3. Share encrypted messages with friends
4. Integrate with radio equipment for long-distance communication
5. Contribute AI enhancement features

Enjoy your SSTV adventures! 🎉
