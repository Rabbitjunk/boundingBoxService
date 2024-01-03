import os
from threading import Thread
from flask import Flask, request, redirect, flash
from src.ProcessController import process_file



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'



@app.route("/process", methods=['POST'])
async def process():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    filename = file.filename
    if os.path.exists(f"{app.config['UPLOAD_FOLDER']}")== False:
        os.makedirs(f"{app.config['UPLOAD_FOLDER']}")
    file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")

    # Verarbeite die Datei asynchron
    thread = Thread(target=process_file, args=(f"{app.config['UPLOAD_FOLDER']}/{filename}",))
    thread.start()
    print(f"Thread for {filename} startet")
    return "success"

    

if __name__ == '__main__':
    print("Program starten")
    app.run(debug=True)
