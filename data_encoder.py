import amodem.main
import amodem.config
import io
import wave

class DataEncoder:
    def encode(self, data, output_path='output.wav'):
        config = amodem.config.Configuration()
        
        # amodem writes raw samples, so we need to add a WAV header
        raw_audio_io = io.BytesIO()
        amodem.main.send(config, src=io.BytesIO(data), dst=raw_audio_io)
        
        raw_audio = raw_audio_io.getvalue()

        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1) # mono
            wf.setsampwidth(config.sample_size)
            wf.setframerate(config.Fs)
            wf.writeframes(raw_audio)
            
        return output_path
