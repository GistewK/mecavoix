import os 
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from audio_router import find_mic_id
SAMPLE_RATE = 16000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR,"models","vosk-model-small-en-us-0.15")
audio_queue = queue.Queue()
def audio_callback(indata, frames, time, status):
    if status:
        print(f"[Aduio Status]: {status}")
    audio_queue.put(bytes(indata))
def start_listening(mic_id=None, model_path=MODEL_PATH):
    mic_id = mic_id or find_mic_id()
    if mic_id is None:
        print("Error: No physical microphone found!")
        return
    if not os.path.exists(model_path):
        print(f"Error: Vosk model not found at {model_path}")
        return
    print(f"Error: Vosk model not found at {model_path}...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    print(f"Listening on Mic ID {mic_id}... Speak now! (Ctrl+C to stop)\n")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        device=mic_id,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result_dict = json.loads(recognizer.Result())
                final_text = result_dict.get("text","")
                if final_text:
                    print(f"\r[FINAL]: {final_text}                       ")
            else:
                partial_dict = json.loads(recognizer.PartialResult())
                partial_text = partial_dict.get("partial","")
                if partial_text:
                    print(f"\r[LIVE]: {partial_text}", end="", flush=True)
if __name__ == "__main__":
    try:
        start_listening()
    except KeyboardInterrupt:
        print("\nStopped listening.")