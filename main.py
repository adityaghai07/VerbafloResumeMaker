from flask import Flask, request, render_template, send_file
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


app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['GENERATED_FOLDER'] = 'generated/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


if not os.path.exists(app.config['GENERATED_FOLDER']):
    os.makedirs(app.config['GENERATED_FOLDER'])

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
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     file.save(filepath)

        if file and allowed_file(file.filename):
            # Read file into memory
            file_stream = io.BytesIO(file.read())
            
            
            resume_html = process_pdf(file_stream, style)
            
            
            output_filename = 'resume_output.html'
            output_filepath = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
            with open(output_filepath, 'w') as html_file:
                html_file.write(resume_html)
            
            return render_template('preview.html', resume_html=resume_html, download_link=output_filename)
    
    return render_template('upload.html')



@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
