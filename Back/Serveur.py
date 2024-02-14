from flask import Flask, render_template, request
import os
from GeneratePassword import generate_mdp 

app = Flask(__name__, template_folder='../Front/template')

base_de_donnees = os.path.join(app.root_path, 'BDD/DB.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + base_de_donnees
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prénom = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mdp = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User('{self.prénom}', '{self.nom}', '{self.email}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generatePassword')
def generate_password_page():
    return render_template('generatePassword.html')

@app.route('/generatePassword/generate', methods=['POST'])
def generate_password():
    longueur = request.form.get('longueur', 10)
    longueur = int(longueur)
    mot_de_passe = generate_mdp(longueur)
    return mot_de_passe

if __name__ == '__main__':
    app.run(debug=True)
