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
        print(Error: "VB-Cable input not found")
        return
    sample_rate = 44100
    letter_count = 0
    for char in text:
        in char in ".!?":