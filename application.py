# python application.py
from flask import Flask,request, jsonify,render_template,abort
import os,uuid
from sanitize_filename import sanitize # https://pypi.org/project/sanitize-filename/#description # pip install sanitize_filename
import shutil
from PDF import pdf

app = Flask(__name__)   
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = 'static\\pdf_store'

# to send the home page
@app.route('/', methods=['GET'])
def home() :
    return render_template('index.html')

# to convert the images to pdf
@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    # extract file data from the request
    files = request.files.getlist("file[]")
    if files == [] : abort(400, 'Provide at least one image') 

    # use in all the names 
    pdf_name = str(uuid.uuid4())[:18] # save with uuid_name
    folder_to_save = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name)

    # file sanitization check
    for file in files :
        if sanitize(file.filename).rsplit('.',1)[1].upper() not in ['PNG','JPG','JPEG','JIFF','TIFF'] : abort(400, 'Wrong file type') 

    # creating the folder to save the file 
    if not os.path.exists(folder_to_save) : os.mkdir(folder_to_save)

    # saving the images
    for image in files : image.save(os.path.join(folder_to_save, sanitize(image.filename) ) )
    
    # formation of pdf get_data from - folder_to_save
    pdf_size = pdf.create_compressed_pdf(folder_to_save,pdf_name)
    # save in app.config['UPLOAD_FOLDER']

    # save the pdf and delete the folder
    if os.path.exists(folder_to_save) : shutil.rmtree(folder_to_save)

    return jsonify(pdf_name,pdf_name)

@app.route('/download')
def download():
    print("download the file ")
    file_name = request.args.get("name")
    # check if the file exists in the pdf directory
    if exists : return 1
    else : return 0
# add route to see all the saved files and download them 
# add route to see and delete it  

if __name__ == "__main__":
    app.run()


# for unix
# export FLASK_APP=api.py 
# for windows
# SET FLASK_APP=api.py

# to run 
# flask run
