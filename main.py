# from flask import Flask, request, render_template
# import os
# from werkzeug.utils import secure_filename
# import PyPDF2
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = Flask(__name__)

# # Configuration
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No file part'
#         file = request.files['file']
#         if file.filename == '':
#             return 'No selected file'
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Process the PDF and generate HTML resume
#             resume_html = process_pdf(filepath)
            
#             return resume_html
#     return render_template('upload.html')

# def process_pdf(filepath):
#     # Extract text from PDF
#     with open(filepath, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
    
#     # Use OpenAI API to process the text
#     # openai.api_key = os.getenv("OPENAI_API_KEY")
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that generates HTML resumes from LinkedIn profile information."},
#             {"role": "user", "content": f"Generate an HTML resume from this LinkedIn profile information: {text}"}
#         ]
#     )
    
#     prediction = response.choices[0].message.content.strip()
#     return prediction

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['GENERATED_FOLDER'] = 'generated/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure generated folder exists
if not os.path.exists(app.config['GENERATED_FOLDER']):
    os.makedirs(app.config['GENERATED_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the PDF and generate HTML resume
            resume_html = process_pdf(filepath)
            
            # Save the generated HTML to a file
            output_filename = 'resume_output.html'
            output_filepath = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
            with open(output_filepath, 'w') as html_file:
                html_file.write(resume_html)
            
            return render_template('preview.html', resume_html=resume_html, download_link=output_filename)
    
    return render_template('upload.html')

def process_pdf(filepath):
    # Extract text from PDF
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    # Use OpenAI API to process the text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates HTML resumes from LinkedIn profile information."},
            {"role": "user", "content": f"Generate an HTML resume from this LinkedIn profile information: {text}"}
        ]
    )
    
    prediction = response.choices[0].message.content.strip()
    return prediction

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
