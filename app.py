from os import name
from flask_admin import model
from pymongo import MongoClient
from bson.objectid import ObjectId
import flask_admin as admin
from wtforms import form, fields
from flask_admin.form import Select2Widget
from flask_admin.contrib.pymongo import ModelView, filters, view
from bson.json_util import dumps
import json
from bson import json_util
import html
from flask import Flask, render_template, jsonify, request


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create models
conn = MongoClient()
db = conn.bdd
conn = MongoClient('localhost', 27017)
db = conn.bdd


# User admin

class menu_form(form.Form):
    img = fields.StringField('사진')
    menu = fields.StringField('메뉴')
    price = fields.StringField('가격')
    category = fields.SelectField('카테고리', choices= [('김치', '김치'),
                ('마른반찬', '마른반찬'), ('나물', '나물'), ('국/탕/찌개', '국/탕/찌개'), ('조림/구이', '조림/구이'), ('튀김/전', '튀김/전'), ('도시락', '도시락'), ('제사/명절','제사/명절')])
    hide = fields.SelectField('숨김/보임', choices= [('0','보임'), ('1','숨김')] )

    # DB에 저장할때 사용하는 key = fields.StringField('name') < value 값이 저장되는 inputbox

class order_form(form.Form):
    state = fields.SelectField ('주문 상태', choices= [('입금대기','입금대기'),('결제완료', '결제완료'),('상품준비중','상품준비중'),('배송중','배송중'),('배송완료','배송완료')])


class menu_view(ModelView):

    column_list = ('img', 'menu', 'price','category') #db에서 불러올때 사용하는 key값
    

    form = menu_form

class order_view(ModelView):
    column_list = ('name', 'menu', 'number', 'address', 'price', 'state','date' )
    column_sortable_list = ('name', 'menu', 'number', 'address', 'price', 'state','date')
    can_edit = True

    form = order_form

    
    # def on_model_change(self, form, model, is_created):
    #     user_id = model.get('user_id')
    #     model['user_id'] = ObjectId(user_id)
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



    #     return model
    
# Flask views

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/header.html')
def dotest():
    return render_template('header.html')

@app.route('/footer.html')
def do1test():
    return render_template('footer.html')

# 일단 보류
# @app.route('/habit_s', methods=['GET'])
# def show_habit():
#     orders = list(db.user.find({}, {'_id': False}))

#     return jsonify({'all_order': orders})


@app.route('/mypage')
def objetdata():
    return render_template('objectdatap.html')


@app.route('/test')
def test11():
    return render_template('test.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/toto')
def testdo():
    return render_template('cart_test_jin.html')

@app.route('/mypage/do', methods=['GET'])
def post_test():
    test = list(db.menu.find({},{'_id': False}))
    #test = [doc for doc in db.user.find({},{'_id': False})]
    print(test)
    
    

    return jsonify({'data': dumps(test)})
    raise TypeError('타입 에러 확인')

@app.route('/bluenight/check', methods=['POST'])
def admin_pass():
    something = request.form['pass']
    correct = "cha'smom"
    if(something == correct):
       return jsonify({'chk':'true'})
    else:
       return jsonify({'chk':'false','msg':'틀렸습니다'})



if __name__ == '__main__':
    # url 변경할것 
    admin = admin.Admin(app, name='맘스키친', url='/bluenight')
    
    # Add views
    admin.add_view(menu_view(db.menu, '상품관리', url='/Product_management'))
    admin.add_view(order_view(db.user, '주문내역', url='/Order_details'))

    # Start app
    app.run('0.0.0.0', port=5000, debug=True)

    
    