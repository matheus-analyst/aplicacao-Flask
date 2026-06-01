# OdontoFácil

Sistema simples de gestão para clínicas odontológicas, desenvolvido com Flask e SQLite.

## 🌟 Funcionalidades

- Cadastro, edição e exclusão de pacientes
- Agenda de consultas com filtros
- Dashboard com estatísticas
- Busca e filtragem inteligente
- Interface responsiva com Bootstrap

## 📦 Tecnologias

- Python 3.8+
- Flask (Framework web)
- SQLAlchemy (ORM)
- SQLite (Banco de dados)
- Bootstrap 5 (Interface)

## 🚀 Como instalar

### No SPCK (Android)

1. Abra o SPCK
2. Instale o Python
3. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/odonto-facil.git
   cd odonto-facil
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Execute a aplicação:
   ```bash
   python app.py
   ```
6. Abra no navegador: `http://localhost:5000`

### No Termux (Android)

1. Instale o Termux
2. Atualize os pacotes:
   ```bash
   pkg update && pkg upgrade
   pkg install git python
   ```
3. Clone e execute igual ao SPCK:
   ```bash
   git clone https://github.com/seu-usuario/odonto-facil.git
   cd odonto-facil
   pip install -r requirements.txt
   python app.py
   ```

### No PC (Windows, Linux, Mac)

```bash
git clone https://github.com/seu-usuario/odonto-facil.git
cd odonto-facil
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

## 📂 Estrutura do Projeto

```
OdontoFácil/
├── app.py               # Aplicação principal
├── requirements.txt     # Dependências
├── README.md            # Este arquivo
├── docs/
│   └── arquitetura.md   # Documentação técnica
├── templates/           # Páginas HTML
│   ├── base.html
│   ├── index.html
│   ├── pacientes.html
│   ├── novo_paciente.html
│   ├── editar_paciente.html
│   ├── consultas.html
│   ├── nova_consulta.html
│   └── editar_consulta.html
└── static/
    └── style.css        # Estilos personalizados
```

## 🧪 Testes

Os testes estão em desenvolvimento. Para rodar:

```bash
pip install pytest
python -m pytest testes/
```

## 🔄 CI/CD

GitHub Actions configurado para testar a cada push.

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

> Desenvolvido com ❤️ para estudantes de Python e clínicas pequenas.