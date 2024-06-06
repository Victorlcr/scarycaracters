from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spookyCaracters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Banco de dados
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


#Rotas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lista_personagens')
def lista_personagens():
    # Recupera todos os registros da tabela Exemplo e os passa para o template
    personagens = Personagens.query.all()

    return render_template('lista_personagens.html', personagens=personagens)


@app.route('/adicionar_personagem', methods=['GET', 'POST'])
def adicionar_personagem():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
        aparicao = request.form['aparicao']
        imagem = request.form['imagem']

        # Obtém a data e hora atual em UTC
        data_cadastro = datetime.now(timezone.utc)

        novo_personagem = Personagens(nomePersonagem=nome, dataNascimento=data_nascimento, dataCadastro=data_cadastro, aparicao=aparicao, imagem=imagem)
        db.session.add(novo_personagem)
        db.session.commit()

        return redirect(url_for('lista_personagens'))
    else:
        return render_template('adicionar_personagem.html')
    

@app.route('/editar_personagem/<int:id>', methods=['GET', 'POST'])
def editar_personagem(id):
    personagem = Personagens.query.get(id)
    if request.method == 'POST':
        personagem.nomePersonagem = request.form['nome']
        personagem.dataNascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
        personagem.aparicao = request.form['aparicao']
        personagem.imagem = request.form['imagem']
        db.session.commit()
        return redirect(url_for('lista_personagens'))
    else:
        return render_template('editar_personagem.html', personagem=personagem)


@app.route('/excluir_personagem/<int:id>')
def excluir_personagem(id):
    personagem = Personagens.query.get(id)

    db.session.delete(personagem)
    db.session.commit()
    return redirect(url_for('lista_personagens'))


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)