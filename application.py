# python application.py
from flask import Flask,request,jsonify,render_template,abort,send_file,url_for,redirect
import shutil,os,uuid
from sanitize_filename import sanitize # https://pypi.org/project/sanitize-filename/#description # pip install sanitize_filename
from PDF import pdf
import time

app = Flask(__name__)   
app.config['UPLOAD_FOLDER'] = os.path.join('static','pdf_store')
app.config["DEBUG"] = True

# to send the home page and convert into pdf on post request
@app.route('/', methods=['GET','POST'])
def main() :
    print(request.method)
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # to convert the images to pdf
        # extract file data from the request
        files = request.files.getlist("file[]")
        if files == [] : abort(400, 'Provide at least one image') 

        # use in all the names 
        pdf_name = str(uuid.uuid4())[:18] # save with uuid_name
        folder_to_save = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name)

        # file sanitization check
        for file in files :
            # print(file.filename)
            if sanitize(file.filename).rsplit('.',1)[1].upper() not in ['PNG','JPG','JPEG','JIFF','TIFF'] : abort(400, 'Wrong file type') 

        # creating the folder to save the file 
        if not os.path.exists(folder_to_save) : os.mkdir(folder_to_save)

        # saving the images
        for image in files : image.save(os.path.join(folder_to_save, sanitize(image.filename) ) )
        
        # formation of pdf get_data from - folder_to_save
        pdf_size = pdf.create_compressed_pdf(folder_to_save,pdf_name)
        # save in app.config['UPLOAD_FOLDER']

        # save the pdf and delete the folder
        # if os.path.exists(folder_to_save) : shutil.rmtree(folder_to_save)

        # return send_from_directory(directory = app.config['UPLOAD_FOLDER'] ,filename = pdf_name)
        # (directory = app.config['UPLOAD_FOLDER'] ,filename = pdf_name)
        # try : return send_from_directory(app.config['UPLOAD_FOLDER'],pdf_name, as_attachment=True)
        # return send_file(BytesIO(os.path.join(app.config['UPLOAD_FOLDER'],pdf_name) ),as_attachment=True )
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name+'.pdf')
        try : return send_file(file_path,mimetype='application/pdf',attachment_filename="Your_small_pdf.pdf",as_attachment=True)
        except : return jsonify(pdf_name,pdf_size)

# for cheking the flow of files 
@app.route('/admin/rishi/23092002' , methods = ['GET'])
def all_files():
    # return all the file in the store by date 
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # format [[name ,date,link],[...]]

    # create list of data 
    data_list = [[i,os.stat(os.path.join(app.config['UPLOAD_FOLDER'],i)).st_mtime,f'/download/{i}',f'/delete/{i}'] for i in files ]
    # sorting by time
    data_list = sorted(data_list ,key=lambda a : a[1],reverse=True)
    # create readable data
    data_list = [[i[0],time.ctime(i[1]),i[2],i[3]] for i in data_list]

    return render_template('all_files.html' ,len = len(data_list), data_list = data_list)

# files check download 
@app.route('/download/<pdf_name>')
def download(pdf_name):
    # print("download the file ")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name)
    return send_file(file_path,mimetype='application/pdf',as_attachment=True)

# file check deleter
@app.route('/delete/<pdf_name>')
def delete(pdf_name):
    # print("download the file ")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name)
    os.remove(file_path)
    return redirect(url_for("all_files"))

@app.route('/testing',methods=['POST'])
def testing():
    print(request.form)
    for i in request.form.getlist('files'):
        print(dir(i))
    return ""


if __name__ == "__main__":
    # app.run(host = '0.0.0.0')
    app.run()
    # app.run(threaded=True,use_reloader=True)
    # app.run(debug=True, use_debugger=True, use_reloader=True)


# for unix
# export FLASK_APP=api.py 
# for windows
# SET FLASK_APP=api.py

# to run 
# flask run
