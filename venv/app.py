from flask import Flask,render_template,request,url_for,redirect
from flask import jsonify
from flask import send_from_directory
import os
import io
import subprocess
import shutil
import wave
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
tosend=''
######나중에 경로 하나의 변수로 나타내기#####

@app.route('/')
def index():
    d='hello'
    print("hello")
    return render_template('index.html')

@app.route('/admin')
def hello_admin():
   print("hello")
   return 'Hello Admin'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/handle_form',methods=['POST','GET'])
def handle_data():#파일 받아와서 저장
    file = request.files['file']
    print("hihi")
    print(file)
    file2 = request.files['file2']
    print("hihi")
    print(file2)
    filename="temp.jpg"
    filename2="temp2.jpg"
    print(filename)
    file.save(os.path.join(r'C:\Users\82109\grad',filename))
    file2.save(os.path.join(r'C:\Users\82109\grad', filename2))

    shutil.copy('C:/Users/82109/grad/temp.jpg', 'C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/IVCL_FaceData/image/001.jpg')
    shutil.copy('C:/Users/82109/grad/temp2.jpg',
                'C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/IVCL_FaceData/images_profile/001.jpg')

    return 'Hello Admin'

@app.route('/pic',methods=['POST','GET'])
def hello_model():
    print("gotpic")
    if request.method=='POST':
        print("POSTED file:{}".format(request.files['file']))
        file=request.files['file']
        file2=request.files['file'][1]
        return ""
    else:
        user=request.args.get('myName')
        print("hi")
        return redirect(url_for('success',name=user))


@app.route('/sendobj')
def sendobj():#obj 파일 전송
    f=open('C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/aobjhair3/001.obj','r')
    s=f.read()
    print(s)
    return s


@app.route('/sendpic2', methods = ['GET', 'POST'])
def sendpic2():#pic 파일 전송 절대경로
    if request.method=='GET':
        print('getget')
        uploads = os.path.join('C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/refined_result',
                               '001t.png')  # 보내려는 파일
        print(uploads)
        shutil.copy(uploads, 'C:/Users/82109/PycharmProjects/flask/venv/static/001t.png')
        return send_from_directory('C:/Users/82109/PycharmProjects/flask/venv/static','001t.png')
    elif request.method=='POST':
        print("postpost")
        uploads = os.path.join('C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/refined_result', '001t.png')#보내려는 파일
        print(uploads)
        shutil.copy(uploads, 'C:/Users/82109/PycharmProjects/flask/venv/static/001t.png')
        return render_template('img.html')

@app.route('/guest')#실행프로그램# 조건 명시하기 가정 다양한 데모 보여주기 proposal 업무분담 전체 계획표 중에서 얼마나 되어있는지 모델러 있던거 씀
def hello_guest():
    print("hihhi")
    p = subprocess.Popen(
        ["C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/x64/release/3DFaceModeler_BFM.exe"],
        shell=True).wait()  # 잘 되는지 확인
    f = open('C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/refined_result/o.obj', 'r')#실제 obj 불러오기 #obj저장 경로도 바꾸기 in visual
    s = f.read()
    return s

@app.route('/guestobj')#실행프로그램# 조건 명시하기 가정 다양한 데모 보여주기 proposal 업무분담 전체 계획표 중에서 얼마나 되어있는지 모델러 있던거 씀
def hello_obj():
    f = open('C:/Users/82109/source/repos/RBF_Modeling_integrated_190213/texturemap/refined_result/o.obj', 'r')#실제 obj 불러오기 #obj저장 경로도 바꾸기 in visual
    s = f.read()
    return "complete"




def is_wav(f):
    res = True
    try:
        wave.open(f)
    except wave.Error as e:
        res = False
    return res
#음성 입력 받으면 text로 변환
#변환된 text parameter에 대응시켜 client로 보내기
@app.route('/param',methods=['POST','GET'])
def param():
    file = request.files['file']
    print("hivoice")
    print(file)
    filename="appvoice.pcm"
    file.save(os.path.join(r'C:\Users\82109\grad', filename))
    if is_wav(file):
        raise ValueError('"' + str(file) + '"' +
                         " is a wav file, not pcm file! ")
    dirname="C:/Users/82109/grad/appvoice.pcm"
    pcmf = open(dirname, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()
    if 16 % 8 != 0:#16=bits
        raise ValueError("bits % 8 must == 0. now bits:" + str(16))

    wavfile_ = wave.open('C:/Users/82109/grad/appvoice.wav', 'wb')
    wavfile_.setnchannels(1)#channel
    wavfile_.setsampwidth(16 // 8)#16: bits
    wavfile_.setframerate(44100)#samplerate
    print('here?')
    wavfile_.writeframes(pcmdata)
    wavfile_.close()

    return "hihi"



def run_quickstart():
    client=speech.SpeechClient()

    file_name=os.path.join(os.path.dirname(__file__),'.','C:/Users/82109/grad/appvoice.wav')

    t1=10*1000
    t2=t1*1000
  #  newAudio=AudioSegment.from_wav("C:/Users/82109/grad/appvoice.wav")
  #  chunk_length_ms=500#숫자 작을수록 잘게 쪼개짐
  #  chunks=make_chunks(newAudio,chunk_length_ms)
  #  for i,chunk in enumerate(chunks):
  #      chunk_name="chunk{0}.wav".format(i)
  #      print("exporting",chunk_name)
  #      chunk.export(chunk_name,format="wav")

    with io.open(file_name,'rb') as audio_file:#file_name
        content=audio_file.read()
        audio=types.RecognitionAudio(content=content)
     #   audio = speech.types.RecognitionAudio(content=content)

    config=types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=44100,language_code='ko-KR')

 #   config = speech.types.RecognitionConfig(
 #       encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
 #       sample_rate_hertz=3200,
 #       language_code='ko-KR',
 #       audio_channel_count=1,
 #       enable_separate_recognition_per_channel=True)
    response=client.recognize(config,audio)

    print('transcript')
    global tosend
    for result in response.results:
        transtring=result.alternatives[0].transcript
        tosend=transtring
        print('Transcript:{}'.format(transtring))

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

@app.route('/sendparam')
def defineparam():
    run_quickstart()
    global tosend
    length=len(tosend)
    print(length)
    flag =0
    paramsend=''
    paramsend += '1 0 /'
    for i in range(0,length):#param4는 보낼때 10나눠서 보내기(text에서)
        strtmp=tosend[i]
        if strtmp in ['가','자','다','아','하','사','랑','락','하','학','자']:
            if flag==1:
                paramsend+=' 1 -6 /'
            paramsend+=' 1 -27 /'#27
            flag=1
       #     paramsend += ' 1 -27 /'
        elif strtmp in ['감','남','담','합']:
            paramsend+=' 1 -27 / 4 -9 /'#에 원래는 9였음
            if flag==2:
                paramsend+=' 1 -27 /'
            flag=2
        #    paramsend += ' 1 -46 / 4 -26 /'
        elif strtmp in ['방','바']:
            paramsend+=' 4 -9 / 1 -27 /'
            flag=3
        elif strtmp in ['에','네','애','세','내','해','대','뎅','케','백']:
            paramsend+=' 1 -19  2 2 /'
            flag=4
        elif strtmp in ['안','간','찬']:
            paramsend+=' 1 -27 / 1 -2 20 -4 /'#3->4
            flag=5
        elif strtmp in ['이','니','지','인','킨','피']:
            paramsend+=' 1 -35 2 24 /'
            flag=6
        elif strtmp in ['저','정','어','엉','녕','여']:
            paramsend+=' 1 -1 2 -36 4 25 /'#79
            flag=7
        elif strtmp in ['오','요','통','졸','교']:
            paramsend+=' 2 -35 1 26 8 7 20 8 4 28 /'#' 2 -35 1 26 8 7 20 10 4 39 /'
            flag=8
  #  paramsend=replace_str_index(paramsend,0)
    print(paramsend)
    return paramsend
#으 , 우
#안녕하세요 # 정통 # 가방 #사랑합니다 #가방 # 안녕 #이오 #
#오뎅


if __name__ == '__main__':
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\82109\\Downloads\\My Project-4ef0f093ea0d.json"
   app.run(host='0.0.0.0', port='8887', debug=True)#나중에 debug끄기
   app.config['UPLOAD_FOLDER'] = MAT_FOLDER
