from flask import Flask, render_template, request, redirect, url_for 
import os #lets you interact with the operating system (like handling files, folders, paths, etc.).
from werkzeug.utils import secure_filename #Cleans the filename uploaded by the user.


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "❌ No file part in the form ❌"
    
    file = request.files['file']
    code = request.form.get('code')

    if file.filename == '':
        return "❌ No selected file ❌"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("✅ File saved at:", filepath)
        print("✅ Selected code:", code)

        # For now, just render result.html with dummy info
        return render_template('result.html', code=code, filename=filename)

    return "❌ Invalid file type. Only .xls/.xlsx allowed. ❌"
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True)