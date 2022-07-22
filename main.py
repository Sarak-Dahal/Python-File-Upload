# importing required libraries
import os
from flask import Flask, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from moviepy.editor import VideoFileClip
from flask_bootstrap import Bootstrap

# Adding config file of extension and max upload size
app = Flask(__name__)
# Adding secret key for security
app.config['SECRET_KEY'] = '_wde5#y2L"F4qwqQ8z\n\xec]/'
# Only making upload type .mp4 and .mkv
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.mkv']
# Limiting upload size to be 1024 MB == 1 GB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

# Using bootstrap as simple frontend
bootstrap = Bootstrap(app)


class UploadForm(FlaskForm):
    video_file = FileField('Video file')
    submit = SubmitField('Submit')


# Error Handler for File size over 1 GB
@app.errorhandler(413)
def request_entity_too_large(e):
    form = UploadForm()
    msg = "File Size too large. Please only upload file up to 1GB."
    return render_template('index.html', msg=msg, form=form)


# Routing to home root
@app.route('/')
def home():
    form = UploadForm()
    return render_template('index.html', form=form, charge=0, msg="")


# Routing with POST from index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    # Setting value of charge 0$
    charge = 0
    form = UploadForm()

    # If else clause to validate
    if form.validate_on_submit():
        video = 'uploads/' + form.video_file.data.filename
        # Separating filename and filetype using splitext
        file_ext = os.path.splitext(video)[1]

        # Validation for Upload Extensions
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            msg = "Please only upload .mp4 or .mkv files."
            form = UploadForm()
            return render_template('index.html', form=form, msg=msg)
        else:
            # Saving file into storage
            form.video_file.data.save(os.path.join(app.static_folder, video))
            filename = os.path.join(app.static_folder, video)
            # Getting actual size of file
            sample = VideoFileClip(filename)
            size = os.stat(filename).st_size / 1000000
            # If else to calculate charge on basis of size and duration
            if size < 500:
                charge = charge + 5
            else:
                charge = charge + 12.5
            if sample.duration < 378:
                charge = charge + 12.5
            else:
                charge = charge + 20
        # Using jsonify library to store file
        jsonify({'name': video, 'size': size, 'duration': sample.duration, 'type': file_ext, 'charge': charge, })
    return render_template('index.html', form=form, charge=charge)


if __name__ == '__main__':
    app.run(debug=True)
