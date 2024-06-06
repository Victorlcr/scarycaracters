from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spookyCaracters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Personagens(db.Model):
    __tablename__ = 'personagens'

    idPersonagem = db.Column(db.Integer, primary_key=True)
    nomePersonagem = db.Column(db.String(50))
    dataNascimento = db.Column(db.Date)
    dataCadastro = db.Column(db.Date)
    aparicao = db.Column(db.String(50))
    imagem = db.Column(db.String(200))

    def __init__(self, nomePersonagem, dataNascimento, dataCadastro, aparicao, imagem):
        self.nomePersonagem = nomePersonagem
        self.dataNascimento = dataNascimento
        self.dataCadastro = dataCadastro
        self.aparicao = aparicao
        self.imagem = imagem

@app.route('/teste')
def teste():
    # Adiciona um novo registro à tabela Personagens
    data_nascimento = datetime.strptime('19/4/1987', '%d/%m/%Y').date()
    novo_exemplo = Personagens(nomePersonagem="Exemplo de string", dataNascimento=data_nascimento, dataCadastro=date.today(), aparicao='123', imagem='foto')
    
    db.session.add(novo_exemplo)
    db.session.commit()

    # Recupera todos os registros da tabela Exemplo e os passa para o template
    personagens = Personagens.query.all()

    return render_template('teste.html', personagens=personagens)


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)