from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    
    # Relacionamento com consultas
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    profissional = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='aguardando')
    
    # Chave estrangeira para paciente
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    # Garantir que não haja duplicidade de horário
    __table_args__ = (db.UniqueConstraint('data', 'hora', name='unique_data_hora'),)
    
    def __repr__(self):
        return f'<Consulta {self.paciente.nome} em {self.data} às {self.hora}>'
