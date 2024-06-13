import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image

app = Flask(__name__)

# Ensure the temporary folder exists
TEMP_FOLDER = os.path.join(os.getcwd(), 'temp')
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Ensure the static folder exists (for serving images)
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image1' not in request.files or 'image2' not in request.files:
        return 'No file part'

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return 'No selected file'

    img1 = Image.open(image1)
    img2 = Image.open(image2)

    result = add_frame(img1, img2)

    result_filename = os.path.join(TEMP_FOLDER, 'result.png')
    result.save(result_filename)

    # Save result image to static folder to serve it
    static_result_filename = os.path.join(STATIC_FOLDER, 'result.png')
    result.save(static_result_filename)

    return redirect(url_for('result', filename='result.png'))

@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(STATIC_FOLDER, filename), as_attachment=True)

def add_frame(main_image, frame_image):
    main_image = main_image.convert("RGBA")
    frame_image = frame_image.convert("RGBA")
    frame_image = frame_image.resize(main_image.size)

    result = Image.alpha_composite(main_image, frame_image)

    return result

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , debug=True)
