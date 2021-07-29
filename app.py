
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
from wtforms.fields.simple import FileField
import datetime

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create models
# 로컬환경 테스트시 DB연결 코드
conn = MongoClient()
# 서버측 DB연결 코드
#conn = MongoClient('mongodb://test:test@localhost', 27017)
db = conn.bdd



# User admin
# author 배성현
class menu_form(form.Form):
    img = fields.StringField('사진')
    menu = fields.StringField('메뉴')
    price = fields.StringField('가격')
    category = fields.SelectField('카테고리', choices= [('김치', '김치'),
                ('기본반찬/나물', '기본반찬/나물'), ('국/탕/찌개', '국/탕/찌개'), ('조림/구이', '조림/구이'), ('튀김/전', '튀김/전'), ('도시락', '도시락'), ('제사/명절','제사/명절')])
    hide = fields.SelectField('숨김/보임 (1/0)', choices= [('0','보임'), ('1','숨김')] )

    # DB에 저장할때 사용하는 key = fields.StringField('name') < value 값이 저장되는 inputbox


# User admin
# author 배성현
class order_form(form.Form):
    state = fields.SelectField ('주문 상태', choices= [('입금확인중','입금확인중'),('결제완료', '결제완료'),('상품준비중','상품준비중'),('배송중','배송중'),('배송완료','배송완료')])
    deliverynum = fields.StringField('송장번호')
    deliverycompany = fields.SelectField ('택배 회사', choices= [('kr.chunilps','천일택배'),('kr.cjlogistics', 'CJ대한통운'),('kr.cupost','CU 편의점택배'),('kr.cvsnet','GS Postbox 택배'),('kr.cway','CWAY (Woori Express)'),('kr.daesin','대신택배'),('kr.epost','우체국 택배'),('kr.hanips','한의사랑택배'),('kr.hanjin','한진택배'),('kr.hdexp','합동택배'),('kr.homepick','홈픽'),('kr.honamlogis','한서호남택배'),('kr.ilyanglogis','일양로지스'),('kr.kdexp','경동택배'),('kr.kunyoung','건영택배'),('kr.logen','로젠택배'),('kr.lotte','롯데택배')])
    

class origin_form(form.Form):
    name = fields.StringField ('재료명')
    origin = fields.StringField ('원산지')

# User admin
# author 배성현
class menu_view(ModelView):

    column_list = ('img', 'menu', 'price','category','hide') #db에서 불러올때 사용하는 key값
    

    form = menu_form

# User admin
# author 배성현
class order_view(ModelView):
    column_list = ('name', 'menu', 'phone', 'address','postcode', 'price', 'state' , 'date','postmsg' , 'today', 'deliverycompany', 'deliverynum')
    column_sortable_list = ('name', 'menu', 'phone', 'address','postcode', 'price', 'state' , 'date','postmsg' , 'today' ,'deliverycompany', 'deliverynum')
    can_edit = True

    form = order_form

# User admin
# author 배성현
class origin_view(ModelView):

    column_list = ('name', 'origin')

    form = origin_form

# User admin
# author 배성현
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
def header():
    return render_template('header.html')

@app.route('/footer.html')
def footer():
    return render_template('footer.html')

# 일단 보류
# @app.route('/habit_s', methods=['GET'])
# def show_habit():
#     orders = list(db.user.find({}, {'_id': False}))

#     return jsonify({'all_order': orders})


@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/orderlist')
def orderlist():
    return render_template('orderlist.html')

@app.route('/orderlist/dele',methods=['POST'])
def dele_orderlist():
    id = request.form['id']
    msg = ''
    deleid = list(db.order.find({'_id':ObjectId(id)}))
    print(deleid[0]['state'])
    if deleid[0]['state'] == '입금확인중':
        db.order.delete_one({'_id':ObjectId(id)})
        msg = '삭제완료!'
    else:
        msg = '결제가 완료되어 삭제가 불가능합니다. 전화 문의부탁드립니다.'

    return jsonify({'msg':msg})


@app.route('/orderlist/find', methods=['POST'])
def find_orderlist():
    phone = request.form['phone']
    orderlist = list(db.order.find({'phone':phone}))
    
    return jsonify({'orderlist':dumps(orderlist), 'msg':'조회완료!'})


@app.route('/details')
def details():
    return render_template('details.html')


@app.route('/maps')
def kakaomaps():
    return render_template('maps.html')
    

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
    correct = "cha"
    if(something == correct):
       return jsonify({'chk':'true'})
    else:
       return jsonify({'chk':'false','msg':'틀렸습니다'})

@app.route('/order/do', methods=['POST'])
def ordersave():

    name_receive = html.escape(request.form['name'])
    addr_receive = html.escape(request.form['addr'])
    code_receive = html.escape(request.form['code'])
    phone_receive = html.escape(request.form['phone'])
    orderlist_receive = request.form.getlist('orderlist[]')
    date_receive = html.escape(request.form['date'])
    postmsg_receive = html.escape(request.form['ero'])
    pricefinal_receive = html.escape(request.form['price_final'])
    doc = {
        'name':name_receive,
        'address':addr_receive,
        'postcode':code_receive,
        'phone':phone_receive,
        'menu':orderlist_receive,
        'date':date_receive,
        'postmsg':postmsg_receive,
        'price':pricefinal_receive,
        'state': '입금확인중',
        'today': datetime.datetime.now(),
        'deliverycompany': '입력대기중.',
        'deliverynum': '입력해주세요~'
    }
    # 오더 리스트의 0:매뉴이름 1:가격 2:수량
    print(doc)
    db.order.insert_one(doc)

    return jsonify({'msg': name_receive+'님의 주문이 완료되었습니다. 계좌입금 부탁드립니다!'})




if __name__ == '__main__':
    # url 변경할것 
    admin = admin.Admin(app, name='맘스키친', url='/bluenight')
    
    # Add views
    admin.add_view(menu_view(db.menu, '상품관리', url='/Product_management'))
    admin.add_view(order_view(db.order, '주문내역', url='/Order_details'))
    admin.add_view(origin_view(db.origin, '원산지표기', url='/Country_of_origin'))
    
    # Start app
    app.run('0.0.0.0', port=5000, debug=True)

    
    