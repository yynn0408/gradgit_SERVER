import io
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def run_quickstart():
    client=speech.SpeechClient()

    file_name=os.path.join(os.path.dirname(__file__),'.','file.wav')

    t1=10*1000
    t2=t1*1000
    newAudio=AudioSegment.from_wav("file.wav")
    chunk_length_ms=500#숫자 작을수록 잘게 쪼개짐
    chunks=make_chunks(newAudio,chunk_length_ms)
  #  for i,chunk in enumerate(chunks):
  #      chunk_name="chunk{0}.wav".format(i)
  #      print("exporting",chunk_name)
  #      chunk.export(chunk_name,format="wav")

    with io.open(file_name,'rb') as audio_file:#file_name
        content=audio_file.read()
        audio=types.RecognitionAudio(content=content)
     #   audio = speech.types.RecognitionAudio(content=content)

  #  config=types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=44100,language_code='ko-KR')

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='ko-KR',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True)
    response=client.recognize(config,audio)

    for result in response.results:
        print('Transcript:{}'.format(result.alternatives[0].transcript))



if __name__=='__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\82109\\Downloads\\My Project-4ef0f093ea0d.json"
    run_quickstart()
