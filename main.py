# Imports
from enum import unique
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, datetime

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'bd.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Account model
class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)
    is_alive = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

def __init__(self, email, password, token, is_alive, created_at):
    self.email = email
    self.password = password
    self.token = token
    self.is_alive = is_alive
    self.created_at = created_at

# Account achema
class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'token', 'is_alive', 'created_at')

# Init account schema
account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

# Create an account
@app.route('/account', methods=['POST'])
def add_account():
    email = request.json['email']
    password = request.json['password']
    token = request.json['token']
    is_alive = request.json['is_alive']
    created_at = request.json['created_at']

    new_account = Account(email, password, token, is_alive, created_at)

    db.session.add(new_account)
    db.session.commit()

    return account_schema.jsonify(new_account)

# Update an account
@app.route('/account/<id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)

    email = request.json['email']
    password = request.json['password']
    token = request.json['token']
    is_alive = request.json['is_alive']

    account.email = email
    account.password = password
    account.token = token
    account.is_alive = is_alive

    db.session.commit()
    return account_schema.jsonify(account)

# Get all accounts
@app.route('/accounts', methods=['GET'])
def get_accounts():
    all_accounts = Account.query.all()
    result = accounts_schema.dump(all_accounts)
    return jsonify(result.data)

# Get account by id
@app.route('/account<id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return account_schema.jsonify(account)

# Delete account by id
@app.route('/delete<id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return account_schema.jsonify(account)

# Run server
if __name__ == '__main__':
    app.run(debug=True)