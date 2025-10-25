import numpy as np
import pyaudio
import speech_recognition as sr
import threading


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 0.01


audio = pyaudio.PyAudio()
stream = None


try:
    input("Press ENTER to start recording...")
    print("Recording... press ENTER again to stop.")


    stream = audio.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

   # Use non-blocking check for stop signal
    import threading

    stop_flag = False


    def wait_for_stop():
       global stop_flag
       input()  # Wait for ENTER
       stop_flag = True
    
    frames = []

    threading.Thread(target=wait_for_stop, daemon=True).start()
    while not stop_flag:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32)/32768.0
            rms = np.sqrt(np.mean(audio_np**2))
            if rms >= THRESHOLD:
                frames.append(data)

        except OSError as e:
           print("Audio error:", e)
           break


finally:
    print("Stopping...")
    if stream and stream.is_active():
        stream.stop_stream()
    if stream:
        stream.close()
    audio.terminate()

    recognizer = sr.Recognizer()

    raw_data = b"".join(frames)
    audio_data = sr.AudioData(raw_data, RATE, 2)
    text = recognizer.recognize_google(audio_data)
    print(text)