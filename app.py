# https://realpython.com/flask-by-example-part-1-project-setup/

from flask import Flask, request, render_template, url_for, redirect, send_file
from pytube import YouTube
import os

# Flask app object
app = Flask(__name__)

# Scret key to used CRSF token
app.config['SECRET_KEY'] = '7b8e6eb59551ca29c481045ef383c0cf'


@app.route("/", methods=['GET', 'POST'])
def main():
    # forms = MyForm()  # Form object
    if(request.method == 'POST'):
        link = request.form['vid_url']
        return redirect(url_for('download'))

    return render_template('index.html')


@app.route("/download", methods=['GET', 'POST'])
def download():
    #if(request.method == 'POST'):
    link = request.form['vid_url']
    
    yt = YouTube(link)  # YouTube object
    
    audio_streams = list(yt.streams.filter(only_audio=True, file_extension='mp4'))
    video_streams = list(yt.streams.filter(progressive=True, file_extension='mp4'))

    return render_template('download.html', yt = yt, audio_streams=audio_streams, video_streams=video_streams, link=link)


@app.route("/download/video", methods=['GET', 'POST'])
def vid_download():
    res = request.form.get('res')
    link = request.form.get('l')
    yt = YouTube(link)

    # Downloading the file in .mp4 format
    path = yt.streams.filter(progressive=True,
                            file_extension='mp4', resolution=res).first().download()

    return send_file(path, as_attachment=True)


@app.route("/download/audio", methods=['GET', 'POST'])
def aud_download():
    #if(request.method == 'POST'):
    abr = request.form.get('a')
    link = request.form.get('l')
    yt = YouTube(link)
    path = yt.streams.filter(only_audio=True,
                             file_extension='mp4', abr=abr).first().download()
    # spliting the name of the file
    base, ext = os.path.splitext(path)
    # Changing extension
    new_path = base + '.mp3'
    # Renaming the file
    os.rename(path, new_path)

    return send_file(new_path, as_attachment=True)


@app.route("/feedback")
def feedback():
    return render_template('feedback.html')


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('Error404.html'), 404


if __name__ == "__main__":
    app.run(debug = True) # run object
