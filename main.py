# from flask import Flask, render_template , request
# import uuid
# from werkzeug.utils import secure_filename
# import os

# UPLOAD_FOLDER ="user_uploads"
# ALLOWED_EXTENSIONS ={'png','jpg','jpeg'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/create",methods=["GET","POST"])
# def create():
#     myid = uuid.uuid1()
#     if request.method == "POST":
#         print(request.files.keys())
#         rec_id = request.form.get("uuid")
#         desc = request.form.get("text")
#         input_files =[]
#         for key, value in request.files.items():
#             print(key,value)
#             # Upload the file
#             file =request.files[key]
#             if file:
#                 filename =secure_filename(file.filename)
#                 if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],rec_id)))):
#                     os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],rec_id))
#                     file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,filename))
#                     input_files.append(file.filename)
#                     with open(os.path.join(app.config['Upload_FOLDER'],rec_id,"desc.txt"),"w") as f:
#                          f.write(desc)
#                 for fl in input_files:
#                     with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,"input.txt"),"a") as f:
#                         f.write(f"file'{fl}'\nduration 1\n")


#     return render_template("create.html",myid=myid)

# @app.route("/gallery")
# def gallery():
#     reels =os.listdir("static/reels")
#     print(reels)
#     return render_template("gallery.html")

# app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid

# --- settings ---
UPLOAD_FOLDER = "user_uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# make base upload folder if missing
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    # assumes you have templates/index.html
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid4().hex  # unique id for this upload set

    if request.method == "POST":
        rec_id = request.form.get("uuid", myid)
        desc   = request.form.get("text", "")

        # folder for this record
        rec_folder = os.path.join(app.config["UPLOAD_FOLDER"], rec_id)
        os.makedirs(rec_folder, exist_ok=True)

        saved_files = []

        # handle each uploaded file
        for key, file in request.files.items():
            if not file or not file.filename:
                continue
            if not allowed_file(file.filename):
                continue
            filename = secure_filename(file.filename)
            save_path = os.path.join(rec_folder, filename)
            file.save(save_path)
            saved_files.append(filename)

        # save extra text files (example: description & input list)
        with open(os.path.join(rec_folder, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc)

        if saved_files:
            with open(os.path.join(rec_folder, "input.txt"), "w", encoding="utf-8") as f:
                for name in saved_files:
                    f.write(f"{name}\n")

        # assumes you have templates/create.html
        return render_template("create.html", myid=rec_id, files=saved_files)

    # GET
    return render_template("create.html", myid=myid, files=[])


@app.route("/gallery")
def gallery():
    # lists folders inside user_uploads
    records = []
    base = app.config["UPLOAD_FOLDER"]
    if os.path.exists(base):
        for name in os.listdir(base):
            path = os.path.join(base, name)
            if os.path.isdir(path):
                records.append(name)
    # assumes you have templates/gallery.html
    return render_template("gallery.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)