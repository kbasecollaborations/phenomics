
#!/usr/bin/python
"""The primary router for the data service for API"""
import os
from re import findall
from  annotate_ontology import annotate_ontology
import requests
from flask import Flask, request, Response, render_template , flash, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import uuid

# TODO: space that has enough space to host files
FILE_SERVER_LOCATION = './data'
UPLOAD_FOLDER = "./data/uploads"
# Setup Flask app.
app = Flask(__name__, static_folder=FILE_SERVER_LOCATION)
app.debug = True
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
@app.route('/index')
def index():
    url ={'string': 'data/cities.tsv'}
    return render_template('index.html', title='home', url=url)

ALLOWED_EXTENSIONS=['txt','xlsx']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def annotate_file(filename, filename2):
   #from shutil import copyfile
   #copyfile(filename, filename2)
   a = annotate_ontology()
   a.annotate_phenotypes(filename,filename2)


@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            filename2 = filename + str(uuid.uuid4()) + "_annotated"  
            save_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2) 
            annotate_file(save_path, save_path2)
            url ={'string': save_path2}
            return render_template('index.html', title='Home', url=url)


            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
    return render_template('upload.html')
    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/data/<path:path>')
def static_proxy(path):
    """
    This is used to support Jbrowse sessions.
    Each jbrowse session is a new directory that serves
    static javascript files
    :param path: path to the file on the system
    :return: content of the file
    """
    # print (path)
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)










if __name__ == '__main__':
    app.run(host= '0.0.0.0')

