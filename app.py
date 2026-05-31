from flask import Flask
from routes import bp
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

db.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
