import os, io
from fpdf import FPDF 
from flask import Flask
from google.cloud import vision_v1
# from google.cloud.vision import types
from google.cloud.vision_v1 import types
from flask import request,redirect,render_template,url_for
from werkzeug.utils import secure_filename
import os
# import pytesseract
from PIL import ImageFilter
from PIL import Image
from importlib import reload
import sys
reload(sys)

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision_v1.ImageAnnotatorClient()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/',methods=['POST',])
def submitImage():
    image = request.files['ocrImage']
    text = ''
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    
    
    with io.open(img2, 'rb') as image_file:
        content = image_file.read()
    
    
    image = vision_v1.types.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    text = docText
    print(docText)
    
    file = open('log.txt', 'w')
    print(docText, file = file)

    file.close()


    pdf = FPDF() 
  
    pdf.add_page() 
 
    pdf.set_font("Arial", size = 10) 
 
    # create a cell 
    file = open("log.txt", "r") 
   
    # insert the texts in pdf 
    for g in file: 
        pdf.cell(200, 10, txt = g, ln = 1, align = 'C') 
    
 
    pdf.output("PDF.pdf") 

    
    # text = pytesseract.image_to_string(img)
    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
    f.write(docText)
    f.close()
    return render_template('textFile.html',text=text,filename=f)


if __name__ == '__main__':
#     app.run('0.0.0.0',8000)
    app.run(host='0.0.0.0', port=8000)
# app.run(host='0.0.0.0')
