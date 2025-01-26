from flask import Flask, render_template, request, send_from_directory, url_for
import os

app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html', pdf_url=None)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", pdf_url=None)
    
    file = request.files['file']
    
    # Check if the user selected a file
    if file.filename == '':
        return render_template('index.html', error="No file selected", pdf_url=None)
    
    # Validate and save the file
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        pdf_url = url_for('uploaded_file', filename=file.filename)
        return render_template('index.html', pdf_url=pdf_url)
    
    return render_template('index.html', error="Invalid file format. Please upload a PDF.", pdf_url=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded PDF for preview
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)