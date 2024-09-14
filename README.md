# VerbaFlo Resume Maker

This web application converts LinkedIn PDF profiles into HTML resumes using OpenAI's GPT model.




### Deployed on Vercel: [link](https://verbaflo-resume-maker.vercel.app/)

Create and download professional resumes easily.


## Features

- Upload LinkedIn PDF profiles
- Extract text from PDF files
- Generate HTML resumes using OpenAI's GPT model
- Choose from various styles.
- Simple and intuitive user interface

## Requirements

- Python 3.7+
- Flask
- PyPDF2
- OpenAI Python library
- python-dotenv

## Installation (local setup)

1. Clone this repository:
   ```
   git clone https://github.com/adityaghai07/VerbafloResumeMaker.git
   cd VerbafloResumeMaker
   ```

2. Install the required packages with poetry:
   ```
   poetry install

   ```

3. Set up your OpenAI API key:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Flask application:
   ```
   poetry run python main.py
   ```

2. Open a web browser and go to `http://localhost:5000`

3. Upload a LinkedIn PDF profile and click "Upload and Convert"

4. The application will generate an HTML resume from the uploaded PDF

## Deployment

This application is deployed on Vercel. [VerbaFlo Resume Maker](https://verbaflo-resume-maker.vercel.app/)

## License

This project is licensed under the MIT License.
