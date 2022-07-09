import os

from flask import Flask, jsonify, request, render_template 
#session, redirect
from flask_sqlalchemy import SQLAlchemy
import dotenv
from sqlalchemy import create_engine
#, insert, true, update
from sqlalchemy_utils import database_exists, create_database
from marshmallow import Schema, fields


dotenv.load_dotenv()

db_user = os.environ.get('DB_USERNAME')
db_pass = os.environ.get('DB_PASSWORD')
db_hostname = os.environ.get('DB_HOSTNAME')
db_name = os.environ.get('DB_NAME')

DB_URI = 'mysql+pymysql://{db_username}:{db_password}@{db_host}/{database}'.format(db_username=db_user,\
    db_password=db_pass, db_host=db_hostname, database=db_name)

engine = create_engine(DB_URI, echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cellphone = db.Column(db.String(13), unique=True, nullable=False)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()
    age = fields.Integer()
    cellphone = fields.Str()
    
@app.route('/')
def get_root():
    print('sending root')
    return render_template('index.html')

@app.route('/api')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

@app.route('/api/students', methods=['GET'])
def get_all_students():
    students = Student.get_all()
    student_list = StudentSchema(many=True)
    response = student_list.dump(students)
    return jsonify(response), 200

@app.route('/api/students/get/<int:id>', methods = ['GET'])
def get_student(id):
    student_info = Student.get_by_id(id)
    serializer = StudentSchema()
    response = serializer.dump(student_info)
    return jsonify(response), 200

@app.route('/api/students/add', methods = ['POST'])
def add_student():
    json_data = request.get_json()
    new_student = Student(
        name= json_data.get('name'),
        email=json_data.get('email'),
        age=json_data.get('age'),
        cellphone=json_data.get('cellphone')
    )
    new_student.save()
    serializer = StudentSchema()
    data = serializer.dump(new_student)
    return jsonify(data), 201

# Endpoint DELETE
@app.route('/api/students/delete/<int:id>', methods = ['DELETE'])
def delete_student(id):
    del_student = Student.query.get(id)
    Student.delete(del_student)
    db.session.commit()
    return jsonify({'result':'Congrats successfully removed'}), 200

# Endpoint PATCH
@app.route('/api/students/modify/<int:id>', methods = ['PATCH'])
def modify_student(id):
    mod_student = Student.query.get(id)
    print(request.json)
    if 'name' in request.json:
        mod_student.name = request.json['name']
        s = print(mod_student.name)
    if 'email' in request.json:
        mod_student.email = request.json['email']
    if 'age' in request.json:
        mod_student.age = request.json['age']
        ss = print(mod_student.age)
    if 'cellphone' in request.json:
        mod_student.cellphone = request.json['cellphone']
    db.session.commit()
    serializer = StudentSchema()
    data = serializer.dump(mod_student)
    return jsonify(data), 201    
 
# Endpoint PUT  
@app.route('/api/students/change/<int:id>', methods = ['PUT'])
def change_student(id):
    update_student = Student.query.get(id)
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    cellphone = request.json['cellphone']
    update_student.name = name
    update_student.email = email
    update_student.age = age
    update_student.cellphone = cellphone
    db.session.commit()
    serializer = StudentSchema()
    data = serializer.dump(update_student)
    return jsonify(data), 201

# GET health-check 200
@app.route('/api/health-check/ok', methods=['GET'])
def page_found():
    return ('Ok'), 200

# GET health-check 500
@app.route('/api/health-check/bad', methods=['GET'])
def page_not_found():
    return ('Internal Server Error'), 500

if __name__ == '__main__':
    engine = create_engine(DB_URI, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
