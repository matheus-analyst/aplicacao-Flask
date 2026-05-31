from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, time
from models import db, Paciente, Consulta

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """Página inicial com resumo da clínica"""
    total_pacientes = Paciente.query.count()
    consultas_hoje = Consulta.query.filter_by(data=datetime.now().date()).count()
    consultas_ativas = Consulta.query.filter(Consulta.status.in_(['aguardando', 'em_atendimento'])).count()
    
    return render_template('index.html', 
                         total_pacientes=total_pacientes,
                         consultas_hoje=consultas_hoje,
                         consultas_ativas=consultas_ativas)

@bp.route('/pacientes')
def listar_pacientes():
    """Listar todos os pacientes"""
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    return render_template('pacientes.html', pacientes=pacientes)

@bp.route('/paciente/novo', methods=['GET', 'POST'])
def criar_paciente():
    """Cadastrar novo paciente"""
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        telefone = request.form['telefone'].strip()
        
        if not nome or not telefone:
            flash('Nome e telefone são obrigatórios.', 'error')
            return render_template('paciente_form.html')
        
        # Verificar se já existe paciente com mesmo nome e telefone
        existente = Paciente.query.filter_by(nome=nome, telefone=telefone).first()
        if existente:
            flash('Já existe um paciente com este nome e telefone.', 'warning')
            return render_template('paciente_form.html')
        
        paciente = Paciente(nome=nome, telefone=telefone)
        db.session.add(paciente)
        db.session.commit()
        
        flash('Paciente cadastrado com sucesso!', 'success')
        return redirect(url_for('routes.listar_pacientes'))
    
    return render_template('paciente_form.html')

@bp.route('/consultas')
def listar_consultas():
    """Listar todas as consultas"""
    consultas = Consulta.query.join(Paciente).order_by(Consulta.data.desc(), Consulta.hora).all()
    return render_template('consultas.html', consultas=consultas)

@bp.route('/consultas/hoje')
def listar_consultas_hoje():
    """Listar consultas do dia"""
    hoje = datetime.now().date()
    consultas = Consulta.query.filter_by(data=hoje).join(Paciente).order_by(Consulta.hora).all()
    return render_template('consultas_hoje.html', consultas=consultas, data=hoje)

@bp.route('/consulta/nova', methods=['GET', 'POST'])
def criar_consulta():
    """Criar nova consulta"""
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        data_str = request.form['data']
        hora_str = request.form['hora']
        profissional = request.form['profissional'].strip()
        observacao = request.form['observacao'].strip() if request.form['observacao'] else None
        
        # Validar campos obrigatórios
        if not paciente_id or not data_str or not hora_str or not profissional:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
            return render_template('consulta_form.html', pacientes=pacientes)
        
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            flash('Data ou hora em formato inválido.', 'error')
            return render_template('consulta_form.html', pacientes=pacientes)
        
        # Não permitir agendamentos no passado
        agora = datetime.now()
        data_hora = datetime.combine(data, hora)
        if data_hora < agora:
            flash('Não é possível agendar consultas para datas/horas passadas.', 'error')
            return render_template('consulta_form.html', pacientes=pacientes)
        
        # Verificar se já existe consulta no mesmo horário
        conflito = Consulta.query.filter_by(data=data, hora=hora).first()
        if conflito:
            flash(f'Já existe uma consulta marcada para este horário ({hora_str}). Escolha outro horário.', 'error')
            return render_template('consulta_form.html', pacientes=pacientes)
        
        consulta = Consulta(
            paciente_id=paciente_id,
            data=data,
            hora=hora,
            profissional=profissional,
            observacao=observacao,
            status='aguardando'
        )
        
        db.session.add(consulta)
        db.session.commit()
        
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('routes.listar_consultas'))
    
    return render_template('consulta_form.html', pacientes=pacientes)

@bp.route('/consulta/<int:id>')
def detalhes_consulta(id):
    """Ver detalhes de uma consulta"""
    consulta = Consulta.query.get_or_404(id)
    return render_template('detalhes_consulta.html', consulta=consulta)

@bp.route('/consulta/<int:id>/editar', methods=['GET', 'POST'])
def editar_consulta(id):
    """Editar uma consulta"""
    consulta = Consulta.query.get_or_404(id)
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        data_str = request.form['data']
        hora_str = request.form['hora']
        profissional = request.form['profissional'].strip()
        observacao = request.form['observacao'].strip() if request.form['observacao'] else None
        status = request.form['status']
        
        # Validar campos obrigatórios
        if not paciente_id or not data_str or not hora_str or not profissional or not status:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
            return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)
        
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            flash('Data ou hora em formato inválido.', 'error')
            return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)
        
        # Não permitir agendamentos no passado
        agora = datetime.now()
        data_hora = datetime.combine(data, hora)
        if data_hora < agora and data_hora.date() != agora.date():
            flash('Não é possível agendar consultas para datas/horas passadas.', 'error')
            return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)
        
        # Verificar conflito de horário, exceto a própria consulta
        conflito = Consulta.query.filter(
            Consulta.id != id,
            Consulta.data == data,
            Consulta.hora == hora
        ).first()
        
        if conflito:
            flash(f'Já existe uma consulta marcada para este horário ({hora_str}). Escolha outro horário.', 'error')
            return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)
        
        # Atualizar os dados
        consulta.paciente_id = paciente_id
        consulta.data = data
        consulta.hora = hora
        consulta.profissional = profissional
        consulta.observacao = observacao
        consulta.status = status
        
        db.session.commit()
        
        flash('Consulta atualizada com sucesso!', 'success')
        return redirect(url_for('routes.detalhes_consulta', id=id))
    
    return render_template('editar_consulta.html', consulta=consulta, pacientes=pacientes)

@bp.route('/consulta/<int:id>/cancelar', methods=['POST'])
def cancelar_consulta(id):
    """Cancelar uma consulta"""
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'cancelado'
    db.session.commit()
    
    flash('Consulta cancelada com sucesso!', 'success')
    return redirect(request.referrer or url_for('routes.listar_consultas'))
