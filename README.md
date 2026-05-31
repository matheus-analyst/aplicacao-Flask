# Sistema de Agendamento Odontológico

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

Um sistema simples e profissional para agendamento e controle de consultas em clínicas odontológicas. Desenvolvido com Flask, este projeto resolve o problema comum de clínicas que ainda usam papel ou planilhas para gerenciar seus pacientes e horários.

## 🎯 Problema Resolvido

Muitas clínicas odontológicas pequenas ainda organizam seus agendamentos com cadernos ou planilhas, o que gera:
- Erros de digitação
- Duplicação de horários
- Dificuldade em visualizar consultas do dia
- Falta de controle sobre o status das consultas
- Baixa profissionalização do atendimento

Este sistema digitaliza todo o processo, trazendo organização, confiabilidade e uma interface limpa para a recepção da clínica.

## ✅ Funcionalidades

| Funcionalidade | Descrição |
|----------------|---------|
| 📝 Cadastrar Pacientes | Registra nome e telefone do paciente |
| 🗓️ Agendar Consultas | Define data, hora, dentista e observações |
| ⏳ Status de Consulta | Controla: aguardando, em atendimento, finalizado, cancelado |
| 📅 Listar Consultas do Dia | Visualiza todas as consultas do dia atual |
| 🔍 Ver Detalhes | Mostra informações completas de cada consulta |
| ✏️ Editar Consultas | Permite ajustar dados após o agendamento |
| ❌ Cancelar Consultas | Marca consulta como cancelada |
| ⚠️ Validações | Não permite horários duplicados ou datas passadas |

## 🖼️ Exemplos de Uso

### Página Inicial
![Página Inicial](assets/screenshots/home.png)

### Agendamento de Consulta
![Agendamento](assets/screenshots/agendar.png)

### Lista de Consultas do Dia
![Lista de Consultas](assets/screenshots/lista.png)

## 📁 Estrutura do Projeto

```
.
├── app.py                 # Ponto de entrada da aplicação
├── models.py              # Definição das entidades (Paciente, Consulta)
├── routes.py              # Rotas da aplicação
├── templates/             # Templates HTML com Jinja2
│   ├── base.html          # Layout principal
│   ├── index.html         # Página inicial
│   ├── pacientes.html     # Lista de pacientes
│   ├── agendar.html       # Formulário de agendamento
│   ├── consultas.html     # Lista de consultas diárias
│   └── detalhes.html      # Detalhes de uma consulta
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos principais
│   └── assets/
│       └── screenshots/   # Imagens para o README
├── tests/                 # Testes automatizados
│   └── test_app.py        # Testes com pytest
├── .github/workflows/
│   └── ci.yml             # Configuração de CI/CD com GitHub Actions
├── requirements.txt       # Dependências do Python
└── README.md              # Este arquivo
```

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/sistema-odontologico.git
cd sistema-odontologo
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

No Linux/Mac:
```bash
source venv/bin/activate
```

No Windows:
```bash
venv\\Scripts\\activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação
```bash
python app.py
```

Acesse no navegador: [http://localhost:5000](http://localhost:5000)

## 🧪 Como Executar os Testes

Com o ambiente virtual ativado:
```bash
pytest tests/
```

Ou com cobertura de código:
```bash
pytest tests/ --cov=.
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**: Linguagem principal
- **Flask**: Framework web leve
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados embutido
- **Jinja2**: Templates HTML
- **pytest**: Testes automatizados
- **GitHub Actions**: Integração contínua
- **HTML/CSS**: Interface do usuário

## 📝 Observações

- Todo o código, mensagens e comentários estão em **português**.
- O sistema não permite agendamentos em datas passadas ou horários conflitantes.
- O banco de dados é criado automaticamente na primeira execução.
- Ideal para clínicas pequenas ou consultórios individuais.

## 🌟 Objetivo do Projeto

Este projeto foi criado como parte de um portfólio profissional, demonstrando habilidades em:
- Desenvolvimento web com Flask
- Modelagem de banco de dados
- Validação de dados e regras de negócio
- Interface simples e funcional
- Boas práticas: testes, CI/CD, documentação

> Desenvolvido por um programador júnior com foco em código limpo, funcional e útil.
