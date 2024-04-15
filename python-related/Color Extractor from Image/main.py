from colorthief import ColorThief
from flask import Flask, render_template, request
import os

app = Flask(__name__)
extracting_folder = app.config['UPLOAD_FOLDER'] = r'static/images/'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/colors', methods=['POST', 'GET'])
def get_colors():
    image = request.files['img_file']
    image.save(os.path.join(extracting_folder, image.filename))
    working_image = f'static/images/{image.filename}'

    color_thief = ColorThief(working_image)
    top_colors = color_thief.get_palette(color_count=11)
    return render_template('colors.html', image=working_image, top_colors=top_colors)


if __name__ == '__main__':
    app.run(debug=True)
