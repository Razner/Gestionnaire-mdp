from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
from GeneratePassword import generate_mdp 

app = Flask(__name__, template_folder='../Front/template', static_folder='../Front/static')
base_de_donnees = os.path.join(app.root_path, '../BDD/DB.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + base_de_donnees
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    idPassword = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    site = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)  
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prénom = db.Column(db.String(255), nullable=False)  
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mdp = db.Column(db.String(255), nullable=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/get_plain_password/<int:post_id>')
def get_plain_password(post_id):
    post = Post.query.get_or_404(post_id)  
    return jsonify({'password': post.password})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generatePassword')
def generate_password_page():
    posts = Post.query.all()  
    return render_template('generatePassword.html', posts=posts)  

@app.route('/Login')
def Login_page():
    return render_template('Login.html')

@app.route('/Register')
def Register_page():
    return render_template('Register.html')

@app.route('/generatePassword/generate', methods=['POST'])
def generate_password():
    longueur = request.form.get('longueur', 10)
    longueur = int(longueur)
    password = generate_mdp(longueur)
    return password

@app.route('/createPost', methods=['POST'])
def create_post():
    site = request.form.get('site')
    password = request.form['password']

    user_id = 1

    if site and password:
        password = hash_password(password)  
        new_post = Post(idUser=user_id, site=site, password=password)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('generate_password_page'))
    else:
        return render_template('generatePassword.html', error="Veuillez fournir un nom de site et un mot de passe.")

if __name__ == '__main__':
    app.run(debug=True)
