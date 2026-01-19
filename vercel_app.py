from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['image']
    
    # Check if file is selected
    if file.filename == '':
        return 'No file selected', 400
    
    # Process image
    input_image = file.read()
    output = remove(input_image)
    
    return send_file(
        io.BytesIO(output),
        mimetype='image/png',
        as_attachment=True,
        download_name='background_removed.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
