import pyaudio
import wave
import list_of_microphones

chunk = 1024 
sample_format = pyaudio.paInt16  
channels = 1
fs = 16000
seconds = 5
def record_audio(filename = "output.wav"):
    p = pyaudio.PyAudio()  # Створення об'єкту PyAudio


    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True,
                    input_device_index=list_of_microphones.choice)

    frames = []

    
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    
    stream.stop_stream()
    stream.close()
    
    p.terminate()
    
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()