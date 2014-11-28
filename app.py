from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from time import time
from hashlib import md5
from io import StringIO
import csv

app = Flask(__name__)
Bootstrap(app)

def link_or_default(path):
    if path.startswith("http"):
        return path
    else:
        return "http://u.dini.es/buttons/%s.png" % path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    buttons = []

    csv_content = StringIO(request.files['file'].read().decode("utf-8"))
    links = csv.reader(csv_content, delimiter=",")

    for link in links:
        button = {
            'image': {
                'rest': link_or_default(link[0]),
                'hover': link_or_default(link[1])
            },
            'link': link[2]
        }

        buttons.append(button)

    m = md5()
    m.update(str(time()).encode('utf-8'))
    id = m.hexdigest()[:12]

    return render_template("buttons.html", id=id, buttons=buttons)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
