from flask import Flask, render_template, jsonify, request
from flask_admin import Admin
from flask_admin.base import AdminIndexView

from pymongo import MongoClient

app = Flask(__name__)

#set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'

#set flask_admin
admin = Admin(app, name ='bluenight', template_mode='bootstrap3')

# 클라이언트이름은 bluenight? 찬성
client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mypage')
def objetdata():
    return render_template('objectdatap.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
