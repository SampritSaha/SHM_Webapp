from flask import Flask, render_template, request, redirect, url_for 
import os 
from werkzeug.utils import secure_filename
from utils.plot import plot_acceleration_time, plot_amplitude_frequency, plot_velocity_peak_to_peak
from utils.preprocessing import load_excel, label_data_by_code
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------- HOME PAGE ----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------------------- FILE UPLOAD + PLOTS + LABELING ---------------------------------------
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('error.html', message="❌ No file part in the form ❌")
    
    file = request.files['file']
    code = request.form.get('code')

    if file.filename == '':
        return render_template('error.html', message="❌ No selected file ❌")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("✅ File saved at:", filepath)
        print("✅ Selected code:", code)

        try:
            # ✅ Load Excel
            df = load_excel(filepath)

            # ✅ Compute vpeaktopeak before labeling
            df['vpeaktopeak'] = df['accelerationmsec2'] * df['timesec'] * 0.0393701

            # ✅ Generate plots
            acc_chart = plot_acceleration_time(df, filename.rsplit('.', 1)[0])
            amp_chart = plot_amplitude_frequency(df, filename.rsplit('.', 1)[0])
            vpp_chart = plot_velocity_peak_to_peak(df, filename.rsplit('.', 1)[0])

            # ✅ Apply rule-based labeling
            df["label"] = label_data_by_code(df, code)

        except ValueError as ve:
            return render_template('error.html', message=str(ve))
        
        return render_template('result.html',
                               code=code,
                               filename=filename,
                               acc_chart=acc_chart,
                               amp_chart=amp_chart,
                               vpp_chart=vpp_chart,
                               table_data=df)

    return render_template('error.html', message="❌ Invalid file type. Only .xls/.xlsx allowed. ❌")

# ---------------------------------------------------- RUN ----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
