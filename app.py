# app.py
# Sistema de gestão para clínicas odontológicas - OdontoFácil
# Desenvolvido para facilitar o dia a dia de pequenas clínicas
# Ideal para estudantes de Python com cerca de 1 ano de experiência
# Sistema de gestão para clínicas odontológicas

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuração da aplicação Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///odonto_facil.db'
    """
    Cria e configura a aplicação Flask.

    Esta função implementa o padrão Factory para facilitar testes futuros.
    Configura o banco de dados SQLite e inicializa o SQLAlchemy.
    """

    db = SQLAlchemy(app)

    # Modelo: Paciente
    class Paciente(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100), nullable=False)
        telefone = db.Column(db.String(20))
        email = db.Column(db.String(100))
        data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f'<Paciente {self.nome}>'

    # Modelo: Consulta
    class Consulta(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        data = db.Column(db.Date, nullable=False)
        hora = db.Column(db.String(10), nullable=False)
        paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
        dentista = db.Column(db.String(100), nullable=False)
        procedimento = db.Column(db.String(100), nullable=False)
        status = db.Column(db.String(20), default='Marcada')  # Marcada, Concluída, Cancelada

        paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))

        def __repr__(self):
            return f'<Consulta {self.procedimento} - {self.data}>'

    # Rotas da aplicação
    @app.route('/')
    def index():
        total_pacientes = Paciente.query.count()
        consultas_marcadas = Consulta.query.filter_by(status='Marcada').count()
        consultas_concluidas = Consulta.query.filter_by(status='Concluída').count()
        consultas_canceladas = Consulta.query.filter_by(status='Cancelada').count()

        # Últimas consultas
        ultimas_consultas = Consulta.query.order_by(Consulta.data.desc()).limit(5).all()

        return render_template('index.html',
                               total_pacientes=total_pacientes,
                               consultas_marcadas=consultas_marcadas,
                               consultas_concluidas=consultas_concluidas,
                               consultas_canceladas=consultas_canceladas,
                               ultimas_consultas=ultimas_consultas)

    # Pacientes
    @app.route('/pacientes')
    def lista_pacientes():
        busca = request.args.get('busca', '')
        if busca:
            pacientes = Paciente.query.filter(Paciente.nome.contains(busca)).all()
        else:
            pacientes = Paciente.query.order_by(Paciente.nome).all()
        return render_template('pacientes.html', pacientes=pacientes, busca=busca)

    @app.route('/paciente/novo', methods=['GET', 'POST'])
    def novo_paciente():
        if request.method == 'POST':
            nome = request.form['nome']
            telefone = request.form['telefone']
            email = request.form['email']

            if not nome:
                flash('O nome do paciente é obrigatório.', 'error')
                return render_template('novo_paciente.html')

            novo = Paciente(nome=nome, telefone=telefone, email=email)
            try:
                db.session.add(novo)
                db.session.commit()
                flash('Paciente cadastrado com sucesso!', 'success')
                return redirect(url_for('lista_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao cadastrar paciente.', 'error')
                print(e)

        return render_template('novo_paciente.html')

    @app.route('/paciente/editar/<int:id>', methods=['GET', 'POST'])
    def editar_paciente(id):
        paciente = Paciente.query.get_or_404(id)
        if request.method == 'POST':
            paciente.nome = request.form['nome']
            paciente.telefone = request.form['telefone']
            paciente.email = request.form['email']

            if not paciente.nome:
                flash('O nome do paciente é obrigatório.', 'error')
                return render_template('editar_paciente.html', paciente=paciente)

            try:
                db.session.commit()
                flash('Paciente atualizado com sucesso!', 'success')
                return redirect(url_for('lista_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao atualizar paciente.', 'error')
                print(e)

        return render_template('editar_paciente.html', paciente=paciente)

    @app.route('/paciente/excluir/<int:id>', methods=['POST'])
    def excluir_paciente(id):
        paciente = Paciente.query.get_or_404(id)
        try:
            # Remove todas as consultas associadas
            Consulta.query.filter_by(paciente_id=id).delete()
            db.session.delete(paciente)
            db.session.commit()
            flash('Paciente excluído com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao excluir paciente.', 'error')
            print(e)

        return redirect(url_for('lista_pacientes'))

    # Consultas
    @app.route('/consultas')
    def lista_consultas():
        filtro_status = request.args.get('status', '')
        busca_paciente = request.args.get('busca_paciente', '')

        consultas = Consulta.query.join(Paciente)

        if filtro_status:
            consultas = consultas.filter(Consulta.status == filtro_status)
        if busca_paciente:
            consultas = consultas.filter(Paciente.nome.contains(busca_paciente))

        consultas = consultas.order_by(Consulta.data.desc()).all()
        return render_template('consultas.html',
                               consultas=consultas,
                               filtro_status=filtro_status,
                               busca_paciente=busca_paciente)

    @app.route('/consulta/nova', methods=['GET', 'POST'])
    def nova_consulta():
        pacientes = Paciente.query.order_by(Paciente.nome).all()
        if request.method == 'POST':
            data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
            hora = request.form['hora']
            paciente_id = request.form['paciente_id']
            dentista = request.form['dentista']
            procedimento = request.form['procedimento']
            status = request.form['status']

            nova_consulta = Consulta(data=data, hora=hora, paciente_id=paciente_id,
                                   dentista=dentista, procedimento=procedimento, status=status)
            try:
                db.session.add(nova_consulta)
                db.session.commit()
                flash('Consulta agendada com sucesso!', 'success')
                return redirect(url_for('lista_consultas'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao agendar consulta.', 'error')
                print(e)

        return render_template('nova_consulta.html', pacientes=pacientes)

    @app.route('/consulta/editar/<int:id>', methods=['GET', 'POST'])
    def editar_consulta(id):
        consulta = Consulta.query.get_or_404(id)
        pacientes = Paciente.query.order_by(Paciente.nome).all()
        if request.method == 'POST':
            consulta.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
            consulta.hora = request.form['hora']
            consulta.paciente_id = request.form['paciente_id']
            consulta.dentista = request.form['dentista']
            consulta.procedimento = request.form['procedimento']
            consulta.status = request.form['status']

            try:
                db.session.commit()
                flash('Consulta atualizada com sucesso!', 'success')
                return redirect(url_for('lista_consultas'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao atualizar consulta.', 'error')
                print(e)

        return render_template('editar_consulta.html',
                               consulta=consulta,
                               pacientes=pacientes)

    @app.route('/consulta/excluir/<int:id>', methods=['POST'])
    def excluir_consulta(id):
        consulta = Consulta.query.get_or_404(id)
        try:
            db.session.delete(consulta)
            db.session.commit()
            flash('Consulta excluída com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao excluir consulta.', 'error')
            print(e)

        return redirect(url_for('lista_consultas'))

    return app

# Cria a aplicação
app = create_app()

# Cria as tabelas no banco de dados
with app.app_context():
    from sqlalchemy import text
    # Verifica se o banco já existe para não recriar dados
    try:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'echo': False}
        from sqlalchemy.exc import OperationalError
        db.create_all()
        # Verifica se já existem pacientes
        if Paciente.query.first() is None:
            # Adiciona um paciente de exemplo
            exemplo = Paciente(nome="Ana Silva", telefone="(11) 99999-8888", email="ana@email.com")
            db.session.add(exemplo)
            db.session.commit()
            print("Banco de dados criado e paciente de exemplo adicionado.")
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")

if __name__ == '__main__':
    app.run(debug=True)
