from flask import Flask, request, redirect, url_for, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
from flask import render_template
from convert import *
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/NO', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Delete old doc files and images
        docfilelist = os.listdir("docs/")
        for df in docfilelist:
            os.remove("docs/" + df)
        imfilelist = os.listdir("static/images/")
        for imf in imfilelist:
            os.remove("static/images/" + imf)
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            slide_path = os.path.join('slides', filename)
            file.save(slide_path)
            doc_file = filename.split('.')[0]+ '.docx'
            doc_path = os.path.join('docs', doc_file)
            convert(slide_path, doc_path)
            os.remove(slide_path)
            return redirect(url_for('converted_file', filename=doc_file))
    return render_template('home.html')

@app.route('/home/ENG', methods=['GET', 'POST'])
def home_eng():
    if request.method == 'POST':
        # Delete old doc files and images
        docfilelist = os.listdir("docs/")
        for df in docfilelist:
            os.remove("docs/" + df)
        imfilelist = os.listdir("static/images/")
        for imf in imfilelist:
            os.remove("static/images/" + imf)
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            slide_path = os.path.join('slides', filename)
            file.save(slide_path)
            doc_file = filename.split('.')[0]+ '.docx'
            doc_path = os.path.join('docs', doc_file)
            convert(slide_path, doc_path)
            os.remove(slide_path)
            return redirect(url_for('converted_file', filename=doc_file))
    return render_template('home_eng.html')

@app.route('/download/<filename>')
def converted_file(filename):
    return send_from_directory('docs',
                               filename)

@app.route('/about')
@app.route('/about/NO')
def about():
    return render_template('about.html')

@app.route('/about/ENG')
def about_eng():
    return render_template('about_eng.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()