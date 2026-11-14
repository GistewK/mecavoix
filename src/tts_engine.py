import os
import time
import wave
import random
import tempfile
import numpy as np
import pyttsx3
import sounddevice as sd
from audio_router import find_vb_cable_id
def list_avaliable_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for idx, voice in enumerate(voices):
        print(f"[{idx}] {voice.name}")
    return voices
def speak_to_cable(text, rate=165, voice_index=0, monitor_locally=False):
    if not text or not text.strip():
        return
    vb_id = find_vb_cable_id()
    if vb_id is None:
        print("Error: VB-cable Input not found!")
        return
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    if voices and 0 <= voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    engine.setProperty("rate",rate)
    temp_fd, temp_wav_path = tempfile.mkdtemp(suffix=".wav")
    os.close(temp_fd)
    try:
        engine.save_to_file(text, temp_wav_path)
        engine.runAndWait()
        with wave.open(temp_wav_path, "rb") as wf:
            sample_rate = wf.getframerate()
            channels = wf.getnchannels()
            raw_frames = wf.readframes(wf.getmftames())
            audio_data = np.frombuffer(raw_frames, dtype=np.int16)
            if channels > 1:
                audio_data = audio_data.refresh(-1, channels)
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()
        if monitor_locally:
            sd.play(audio_data, samplerate=sample_rate)
            sd.wait
    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
def generate_retro_blip(base_freq=440.0, duration=0.045, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = np.sin(2 * np.pi * base_freq * t) + 0.3 * np.sign(np.sin(2 * np.pi * base_freq * t))
    envelope = np.linspace(1.0, 0.0, len(t))
    blip = (wave_data * envelope * 0.25).astype(np.float32)
    return blip
def speak_blips(text, base_freq=380.0, monitor_locally=False):
    if not text or not text.strip():
        return

    vb_id = find_vb_cable_id()
    if vb_id is None:
        print("Error: VB-Cable input not found")
        return
    sample_rate = 44100
    letter_count = 0
    for char in text:
        if char in ".!?":
            time.sleep(0.18)
        elif char in ",;:":
            time.sleep(0.09)
        elif char.isspace():
            time.sleep(0.04)
        else:
            letter_count += 1
            if letter_count % 2 == 1:
                varied_freq = base_freq * random.uniform(0.92, 1.08)
                blip = generate_retro_blip(base_freq=varied_freq, sample_rate=sample_rate)
                sd.play(blip, samplerate=sample_rate, device=vb_id)
                if monitor_locally:
                    sd.play(blip, samplerate=sample_rate)
                time.sleep(0.055)
if __name__ == "__main__":
    print("Installed Windows SAPI5 Voices:")
    list_avaliable_voices()

    print("\1n. Testing Robotic SAPI5 TTS...")
    speak_to_cable("Mecavoix audio bridge online.", rate=160, monitor_locally=True)
    time.sleep(0.5)
    print("2. Testing Bleep mode...")
    speak_blips("* Hello! Testing character bleeps!", base_freq=360.0, monitor_locally=True)
