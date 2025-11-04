"""
Data-over-Audio Transceiver - Main Application
Encrypts and transmits files via audio signals
Receives and decrypts audio signals back to files

Author: Created for Data-over-Audio Communication Project
Date: November 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from data_encoder import DataEncoder
from data_decoder import DataDecoder
from crypto_handler import CryptoHandler
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import pyaudio
import wave


class DataTransceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSTV Encoder/Decoder")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialize handlers
        self.encoder = DataEncoder()
        self.decoder = DataDecoder()
        self.crypto = None

        # Variables
        self.mode = tk.StringVar(value="sender")
        self.selected_file = None
        self.encryption_key = tk.StringVar()
        self.use_encryption = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="SSTV Encoder and Decoder", 
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)

        # Mode Selection Frame
        mode_frame = tk.LabelFrame(self.root, text="Select Mode", font=("Arial", 12, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Radiobutton(
            mode_frame, 
            text="Sender Mode", 
            variable=self.mode, 
            value="sender",
            command=self.switch_mode,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=20)

        tk.Radiobutton(
            mode_frame, 
            text="Receiver Mode", 
            variable=self.mode, 
            value="receiver",
            command=self.switch_mode,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=20)

        # Main content frame (will switch based on mode)
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Initially show sender interface
        self.setup_sender_ui()

    def switch_mode(self):
        """Switch between sender and receiver modes"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.mode.get() == "sender":
            self.setup_sender_ui()
        else:
            self.setup_receiver_ui()

    def toggle_encryption_fields(self):
        """Enable or disable encryption fields based on checkbox"""
        if self.use_encryption.get():
            self.key_entry.config(state=tk.NORMAL)
        else:
            self.key_entry.config(state=tk.DISABLED)

    def browse_file(self):
        """Browse and select a file"""
        filename = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg"),
                ("Text Files", "*.txt"),
                ("All files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename), fg="black")
            self.log_sender(f"Selected file: {os.path.basename(filename)}")

    def setup_sender_ui(self):
        """Setup sender interface"""
        # File Selection Frame
        file_frame = tk.LabelFrame(
            self.content_frame, 
            text="Select File", 
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.file_label = tk.Label(file_frame, text="No file selected", fg="gray", font=("Arial", 10))
        self.file_label.pack(pady=5)

        tk.Button(
            file_frame,
            text="Browse File",
            command=self.browse_file,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5,
            cursor="hand2"
        ).pack(pady=5)

        # Encryption Frame
        encrypt_frame = tk.LabelFrame(
            self.content_frame, 
            text="Encryption", 
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        encrypt_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Checkbutton(
            encrypt_frame,
            text="Enable Encryption",
            variable=self.use_encryption,
            font=("Arial", 10),
            command=self.toggle_encryption_fields
        ).pack(anchor=tk.W)

        tk.Label(encrypt_frame, text="Enter encryption key:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))

        self.key_entry = tk.Entry(
            encrypt_frame, 
            textvariable=self.encryption_key, 
            show="*",
            font=("Arial", 10),
            width=50
        )
        self.key_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            encrypt_frame, 
            text="⚠ Remember this key - you'll need it to decrypt!", 
            fg="red",
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W)

        # Action Buttons Frame
        action_frame = tk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            action_frame,
            text="🔊 Generate & Play Audio",
            command=self.generate_and_play,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Button(
            action_frame,
            text="💾 Save Audio File",
            command=self.save_audio,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Status Display
        self.sender_status = scrolledtext.ScrolledText(
            self.content_frame,
            height=8,
            font=("Courier", 9),
            bg="#ecf0f1",
            state=tk.DISABLED
        )
        self.sender_status.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.toggle_encryption_fields()

    def setup_receiver_ui(self):
        """Setup receiver interface"""
        # Input Source Selection
        source_frame = tk.LabelFrame(
            self.content_frame, 
            text="Audio Source", 
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        source_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            source_frame,
            text="🎤 Record from Microphone",
            command=self.record_audio,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        tk.Button(
            source_frame,
            text="📁 Load Audio File",
            command=self.load_audio_file,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # Decryption Key Frame
        decrypt_frame = tk.LabelFrame(
            self.content_frame, 
            text="Decryption", 
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        decrypt_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Checkbutton(
            decrypt_frame,
            text="Enable Decryption",
            variable=self.use_encryption,
            font=("Arial", 10),
            command=self.toggle_encryption_fields
        ).pack(anchor=tk.W)

        tk.Label(decrypt_frame, text="Enter decryption key:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))

        self.key_entry = tk.Entry(
            decrypt_frame, 
            textvariable=self.encryption_key, 
            show="*",
            font=("Arial", 10),
            width=50
        )
        self.key_entry.pack(fill=tk.X)

        # Decode Button
        tk.Button(
            self.content_frame,
            text="🔓 Decode Audio Signal",
            command=self.decode_audio,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=15,
            cursor="hand2"
        ).pack(fill=tk.X, pady=10)

        # Status Display
        self.receiver_status = scrolledtext.ScrolledText(
            self.content_frame,
            height=8,
            font=("Courier", 9),
            bg="#ecf0f1",
            state=tk.DISABLED
        )
        self.receiver_status.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.toggle_encryption_fields()

    def generate_and_play(self):
        """Generate audio and play it"""
        if not self.validate_sender_inputs():
            return

        self.log_sender("Starting audio generation...")

        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._generate_and_play_thread)
        thread.daemon = True
        thread.start()

    def _generate_and_play_thread(self):
        """Thread function for generating and playing audio"""
        try:
            # Read file data
            with open(self.selected_file, 'rb') as f:
                file_data = f.read()

            if self.use_encryption.get():
                # Initialize crypto
                self.crypto = CryptoHandler(self.encryption_key.get())

                # Encrypt file
                self.log_sender("Encrypting data...")
                iv = get_random_bytes(16)
                cipher = AES.new(self.crypto.key, AES.MODE_CBC, iv)
                padded_data = pad(file_data, AES.block_size)
                encrypted_data = cipher.encrypt(padded_data)
                final_data = iv + encrypted_data
                self.log_sender("✓ Data encrypted successfully")
            else:
                final_data = file_data
                self.log_sender("Encryption skipped")

            # Generate audio
            self.log_sender("Generating audio...")
            audio_path = self.encoder.encode(final_data)
            self.log_sender(f"✓ Audio generated: {audio_path}")

            # Play audio
            self.log_sender("Playing audio...")
            self.play_audio(audio_path)
            self.log_sender("✓ Playback complete")

        except Exception as e:
            self.log_sender(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate audio: {str(e)}")

    def save_audio(self):
        """Generate and save audio file"""
        if not self.validate_sender_inputs():
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )

        if not save_path:
            return

        self.log_sender("Starting audio generation...")

        # Run in thread
        thread = threading.Thread(target=self._save_audio_thread, args=(save_path,))
        thread.daemon = True
        thread.start()

    def _save_audio_thread(self, save_path):
        """Thread function for saving audio"""
        try:
            # Read file data
            with open(self.selected_file, 'rb') as f:
                file_data = f.read()

            if self.use_encryption.get():
                # Initialize crypto
                self.crypto = CryptoHandler(self.encryption_key.get())

                # Encrypt file
                self.log_sender("Encrypting data...")
                iv = get_random_bytes(16)
                cipher = AES.new(self.crypto.key, AES.MODE_CBC, iv)
                padded_data = pad(file_data, AES.block_size)
                encrypted_data = cipher.encrypt(padded_data)
                final_data = iv + encrypted_data
                self.log_sender("✓ Data encrypted successfully")
            else:
                final_data = file_data
                self.log_sender("Encryption skipped")

            # Generate audio
            self.log_sender("Generating audio...")
            audio_path = self.encoder.encode(final_data, output_path=save_path)
            self.log_sender(f"✓ Audio saved: {save_path}")

            messagebox.showinfo("Success", f"Audio saved successfully!")

        except Exception as e:
            self.log_sender(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to save audio: {str(e)}")

    def record_audio(self):
        """Record audio from microphone"""
        self.log_receiver("🎤 Starting microphone recording...")
        self.log_receiver("Recording will stop after 10 seconds...")

        # Run in thread
        thread = threading.Thread(target=self._record_audio_thread)
        thread.daemon = True
        thread.start()

    def _record_audio_thread(self):
        """Thread function for recording audio"""
        try:
            audio_path = 'recorded_audio.wav'
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=1024)
            frames = []
            for i in range(0, int(48000 / 1024 * 10)):
                data = stream.read(1024)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(audio_path, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(48000)
            wf.writeframes(b''.join(frames))
            wf.close()

            self.log_receiver(f"✓ Recording saved: {audio_path}")
            self.selected_file = audio_path
        except Exception as e:
            self.log_receiver(f"✗ Recording error: {str(e)}")
            messagebox.showerror("Error", f"Recording failed: {str(e)}")

    def load_audio_file(self):
        """Load audio file for decoding"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            )
        )
        if filename:
            self.selected_file = filename
            self.log_receiver(f"Loaded audio file: {os.path.basename(filename)}")

    def decode_audio(self):
        """Decode audio"""
        if not self.selected_file:
            messagebox.showwarning("No Audio", "Please record or load an audio file first!")
            return

        if self.use_encryption.get() and not self.encryption_key.get():
            messagebox.showwarning("No Key", "Please enter the decryption key!")
            return

        self.log_receiver("Starting audio decoding...")

        # Run in thread
        thread = threading.Thread(target=self._decode_audio_thread)
        thread.daemon = True
        thread.start()

    def _decode_audio_thread(self):
        """Thread function for decoding audio"""
        try:
            # Decode audio
            self.log_receiver("Decoding audio...")
            decoded_data = self.decoder.decode(self.selected_file)
            self.log_receiver(f"✓ Audio decoded")

            if self.use_encryption.get():
                # Decrypt data
                self.crypto = CryptoHandler(self.encryption_key.get())
                self.log_receiver("Decrypting data...")
                
                iv = decoded_data[:16]
                encrypted_data = decoded_data[16:]
                cipher = AES.new(self.crypto.key, AES.MODE_CBC, iv)
                decrypted_padded = cipher.decrypt(encrypted_data)
                final_data = unpad(decrypted_padded, AES.block_size)

                self.log_receiver("✓ Data decrypted successfully")
            else:
                final_data = decoded_data
                self.log_receiver("Decryption skipped")

            # Ask user where to save the decrypted file
            save_path = filedialog.asksaveasfilename(
                title="Save Decoded File",
                defaultextension=".png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("Text File", "*.txt"),
                    ("All files", "*.*")]
            )
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(final_data)
                self.log_receiver(f"✓ Decoded file saved: {save_path}")
                messagebox.showinfo("Success", f"File saved successfully!")

        except Exception as e:
            self.log_receiver(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

    def validate_sender_inputs(self):
        """Validate sender inputs"""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file first!")
            return False
        if self.use_encryption.get() and not self.encryption_key.get():
            messagebox.showwarning("No Key", "Please enter an encryption key!")
            return False
        return True

    def log_sender(self, message):
        """Log message to sender status"""
        if hasattr(self, 'sender_status'):
            self.sender_status.config(state=tk.NORMAL)
            self.sender_status.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
            self.sender_status.see(tk.END)
            self.sender_status.config(state=tk.DISABLED)

    def log_receiver(self, message):
        """Log message to receiver status"""
        if hasattr(self, 'receiver_status'):
            self.receiver_status.config(state=tk.NORMAL)
            self.receiver_status.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
            self.receiver_status.see(tk.END)
            self.receiver_status.config(state=tk.DISABLED)

    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def play_audio(self, wav_path):
        """Play WAV audio file"""
        # Open WAV file
        wf = wave.open(wav_path, 'rb')

        # Create PyAudio instance
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Read and play data
        chunk = 1024
        data = wf.readframes(chunk)

        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataTransceiverApp(root)
    root.mainloop()
