import amodem.main
import amodem.config
import io

class DataDecoder:
    def decode(self, audio_path):
        config = amodem.config.Configuration()
        
        dst = io.BytesIO()
        with open(audio_path, 'rb') as src:
            amodem.main.recv(config, src=src, dst=dst)
            
        return dst.getvalue()