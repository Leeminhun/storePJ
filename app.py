from os import name
from pymongo import MongoClient
from bson.objectid import ObjectId
import flask_admin as admin
from wtforms import form, fields
from flask_admin.form import Select2Widget
from flask_admin.contrib.pymongo import ModelView, filters

from flask import Flask, render_template, jsonify, request


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create models
conn = MongoClient()
db = conn.test


# User admin

class menuForm(form.Form):
    img = fields.StringField('사진')
    menu = fields.StringField('메뉴')
    price = fields.StringField('가격')
    category = fields.SelectField('카테고리', choices= [('김치', '김치'),
                ('마른반찬', '마른반찬'), ('나물', '나물'), ('국/탕/찌개', '국/탕/찌개'), ('조림/구이', '조림/구이'), ('튀김/전', '튀김/전'), ('도시락', '도시락'), ('제사/명절','제사/명절')])
    hide = fields.SelectField('숨김/보임', choices= [('0','보임'), ('1','숨김')] )
    # DB에 저장할때 사용하는 key = fields.StringField('name') < value 값이 저장되는 inputbox



class menuView(ModelView):

    column_list = ('img', 'menu', 'price','category') #db에서 불러올때 사용하는 key값

    # column_sortable_list = ('img', 'menu', 'price') # list 정렬가능한 컬렉션

    form = menuForm

    # def on_model_change(self, form, model, is_created):
    #     user_id = model.get('user_id')
    #     model['user_id'] = ObjectId(user_id)

    #     return model



# Flask views

@app.route('/')
def main():
    return render_template('index.html')

# 일단 보류
# @app.route('/habit_s', methods=['GET'])
# def show_habit():
#     orders = list(db.user.find({}, {'_id': False}))

#     return jsonify({'all_order': orders})


@app.route('/mypage')
def objetdata():
    return render_template('objectdatap.html')

@app.route('/mypage/do', methods=['POST'])
def post_test():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'like 연결되었습니다!'})



if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, name='맘 스 키 친')

    # Add views
    admin.add_view(menuView(db.user, '상품관리'))
    # admin.add_view(orderView(db.order, '주문내역'))
    

    # Start app
    app.run(debug=True)

    
    