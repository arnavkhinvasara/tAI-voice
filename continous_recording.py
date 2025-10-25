import pyaudio
import speech_recognition as sr


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024


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


   frames = []
   # Use non-blocking check for stop signal
   import threading


   stop_flag = False


   def wait_for_stop():
       global stop_flag
       input()  # Wait for ENTER
       stop_flag = True


   threading.Thread(target=wait_for_stop, daemon=True).start()


   while not stop_flag:
       try:
           data = stream.read(CHUNK, exception_on_overflow=False)
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


   raw_data = b"".join(frames)


   recognizer = sr.Recognizer()
   audio_data = sr.AudioData(raw_data, RATE, 2)


   text = recognizer.recognize_google(audio_data)


   print("You said:", text)