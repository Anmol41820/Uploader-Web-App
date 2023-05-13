from io import BytesIO

from flask import Flask, render_template, request, redirect, send_file
# from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anmol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Upload(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.filename}"

# UPLOAD_FOLDER = 'C:\\Users\\Anmol\\Desktop\\Flask(Code With Harry)\\uploadedFiles'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template("index.html")

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return redirect('/files')
    else:
        return render_template('admin.html', error='Invalid login credentials.')


@app.route('/files', methods=['GET','POST'])
def files():
    filess = Upload.query.all()
    return render_template("adminpage.html",filess=filess)
    







# uploading file on folder ---->>>>

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f = request.files['upload-file']

        # filename=request.form['upload-file']

        upload = Upload(filename=f.filename, data=f.read())
        db.session.add(upload)
        db.session.commit()


        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        f.save(os.path.join(
            'uploadedFiles/',
            f.filename))

    filess = Upload.query.all()
    # return f'Uploaded: {f.filename}'
    # return redirect('/login')
    return render_template("admin.html", filess=filess)
        
        
    

# download a file --->>>>
@app.route('/download/<filename>')
def download(filename):
   return send_file(os.path.join('uploadedFiles/', filename), as_attachment=True)





# open the file -->>>>>

# @app.route('/open/<filename>')
# def open(filename):
#    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#    if filename.endswith('.csv'):
#       df = pd.read_csv(file_path)
#    elif filename.endswith('.xlsx'):
#       df = pd.read_excel(file_path)
#    else:
#       return "Invalid File Format"
#    html_table = df.to_html()
   
#    return html_table


@app.route('/open/<filename>')
def open(filename):
#     file = request.form['upload-file']
    file = Upload.query.filter_by(filename=filename).first()
    data = pd.read_excel(file)
    return render_template('data.html', data=data.to_html())
    



if __name__ == "__main__":
    app.run(debug=True, port=8000)