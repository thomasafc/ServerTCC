import os

from flask import Flask, request
from flask.helpers import send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from main import convertVideo
from main import convertImage


app = Flask("__name__", template_folder='templates')
IMAGE_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'imageUpload')
VIDEO_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'videoUpload')


#Upload de imagem
@app.route('/imageUpload', methods=['POST'])
def imageUpload():
    # Pega a imagem, nome e extensão
    file = request.files['image']
    nameImage, extensionImage = os.path.splitext(file.filename)

    # Renomeia a imagem
    now = datetime.now()
    nameImage += '_' + str(datetime.timestamp(now))
    file.filename = nameImage + extensionImage

    # Salva a imagem
    savePath = os.path.join(IMAGE_UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)

    # Chama função para converter a imagem
    frames = convertImage(file.filename)
    print(frames)

    # Exclui o arquivo
    os.path.dirname(os.path.abspath(__file__))
    os.chdir('imageUpload')
    os.unlink(file.filename)

    # Retorna resposta de sucesso!
    return getResponse(200, "Imagem enviada e convertida!")

#Upload de Video
@app.route('/videoUpload', methods=['POST'])
def videoUpload():
    # Pega o video, nome e extensão
    file = request.files['video']
    nameVideo, extensionVideo = os.path.splitext(file.filename)

    # Renomeia o video
    now = datetime.now()
    nameVideo += '_' + str(datetime.timestamp(now))
    file.filename = nameVideo + extensionVideo

    # Salva o video
    savePath = os.path.join(VIDEO_UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)

    # Chama função para converter o video
    frames = convertVideo(file.filename)
    print(frames)

    # Exclui o arquivo
    os.path.dirname(os.path.abspath(__file__))
    os.chdir('videoUpload')
    os.unlink(file.filename)

    # Retorna resposta de sucesso!
    return getResponse(200, "Video enviado e convertido com sucesso!")


#CRIA RESPONSE
def getResponse(status, message, recordName=False, record=False):
    response = {}
    response["status"] = status
    response["message"] = message

    if (recordName and record):
        response[recordName] = record
    
    return response

#RUN
app.run()