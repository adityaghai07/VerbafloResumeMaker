from flask import Flask, request, render_template, send_file, make_response
import os
from werkzeug.utils import secure_filename
import PyPDF2
from openai import OpenAI
from services.process_pdf import process_pdf
from dotenv import load_dotenv
import io

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        style = request.form.get('style')

        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            
            file_stream = io.BytesIO(file.read())
            
            resume_html = process_pdf(file_stream, style)
            
    
            return render_template('preview.html', resume_html=resume_html)
    
    return render_template('upload.html')

@app.route('/download')
def download_file():
    
    html_content = request.args.get('html', '')
    
    
    response = make_response(html_content)
    
    
    response.headers["Content-Disposition"] = "attachment; filename=resume.html"
    response.headers["Content-Type"] = "text/html"
    
    return response

if __name__ == '__main__':
    app.run(debug=True)