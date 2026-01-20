#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# --------- GET ROUTES (Already Provided in Starter Code) ---------

@app.route('/')
def index():
    return "Bakery API"

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return make_response(bakery.to_dict(), 200)
    return make_response({"error": "Bakery not found"}, 404)

@app.route('/baked_goods')
def baked_goods():
    goods = [good.to_dict() for good in BakedGood.query.all()]
    return make_response(goods, 200)

@app.route('/baked_goods/<int:id>')
def baked_good_by_id(id):
    good = BakedGood.query.filter_by(id=id).first()
    if good:
        return make_response(good.to_dict(), 200)
    return make_response({"error": "Baked good not found"}, 404)


# --------- REQUIRED LAB TASKS ---------

# TASK 1 – POST /baked_goods
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():

    new_good = BakedGood(
        name=request.form.get('name'),
        price=request.form.get('price'),
        bakery_id=request.form.get('bakery_id')
    )

    db.session.add(new_good)
    db.session.commit()

    return make_response(new_good.to_dict(), 201)


# TASK 2 – PATCH /bakeries/<int:id>
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):

    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)

    for key in request.form:
        setattr(bakery, key, request.form.get(key))

    db.session.commit()

    return make_response(bakery.to_dict(), 200)


# TASK 3 – DELETE /baked_goods/<int:id>
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):

    good = BakedGood.query.filter_by(id=id).first()

    if not good:
        return make_response({"error": "Baked good not found"}, 404)

    db.session.delete(good)
    db.session.commit()

    return make_response({
        "delete_successful": True,
        "message": "Baked good deleted."
    }, 200)


# --------- EXTRA ROUTE (Often in Lab) ---------

@app.route('/baked_goods/most_expensive')
def most_expensive():

    good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if good:
        return make_response(good.to_dict(), 200)

    return make_response({"error": "No baked goods found"}, 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
