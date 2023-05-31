import json
import pyaudio
from vosk import Model, KaldiRecognizer
# working offline
# download vosk speech
# https://alphacephei.com/vosk/models

# input path to you vosk speech model
model_path = '/home/user/git/SpeechRecognizer/vosk_models/vosk-model-small-ru-0.22'


def offline():

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    def listen():
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(rec.Result())
                if answer['text']:
                    yield answer['text']

    for text in listen():
        if text == 'завершить' or text == 'конец':
            exit()
        elif text == 'запись' or text == 'старт':
            print('Запись начата')


if __name__ == '__main__':
    offline()

