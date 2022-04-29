
from controller.upload import fileUpload
from flask import *
import os

app = Flask(__name__,static_url_path='/',static_folder='static')
app.secret_key = os.urandom(24)


app.register_blueprint(fileUpload)



@app.route('/')
def index():
    return render_template('index.html')


app.run(host='0.0.0.0')