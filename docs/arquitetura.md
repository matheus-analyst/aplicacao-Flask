# Documentação de Arquitetura - OdontoFácil

## 🏗️ Visão Geral

O sistema OdontoFácil é uma aplicação web simples, monolítica, desenvolvida com Flask, para ajudar pequenas clínicas odontológicas a gerenciar pacientes e consultas.

## 🧱 Arquitetura

### Camadas

1. **Apresentação (Frontend)**
   - Templates HTML com Jinja2
   - Bootstrap 5 via CDN
   - CSS personalizado em `static/style.css`

2. **Lógica de Negócio (Backend)**
   - Flask como framework web
   - Rotas definidas em `app.py`
   - Lógica de cadastro, edição, exclusão e listagem

3. **Dados**
   - Banco de dados SQLite (`odonto_facil.db`)
   - ORM SQLAlchemy para abstração
   - Dois modelos principais: `Paciente` e `Consulta`

## 📐 Modelos de Dados

### Paciente

| Campo           | Tipo         | Descrição                     |
|-----------------|--------------|-------------------------------|
| id              | Integer      | Chave primária                |
| nome            | String(100)  | Nome completo do paciente     |
| telefone        | String(20)   | Telefone de contato           |
| email           | String(100)  | E-mail (opcional)             |
| data_cadastro   | DateTime     | Data de cadastro (automático) |

### Consulta

| Campo          | Tipo         | Descrição                                  |
|----------------|--------------|--------------------------------------------|
| id             | Integer      | Chave primária                             |
| data           | Date         | Data da consulta                           |
| hora           | String(10)   | Hora da consulta (ex: 14:30)               |
| paciente_id    | Integer      | Chave estrangeira para Paciente            |
| dentista       | String(100)  | Nome do dentista responsável               |
| procedimento   | String(100)  | Tipo de procedimento (ex: Limpeza)         |
| status         | String(20)   | Status: Marcada, Concluída, Cancelada      |

## 🔗 Relacionamentos

- Um **Paciente** pode ter várias **Consultas** (um-para-muitos)
- A consulta tem uma relação `backref` para acessar o paciente

## 🔄 Fluxo de Dados

1. Usuário acessa uma rota (ex: `/pacientes`)
2. Flask chama a função correspondente
3. A função consulta o banco via SQLAlchemy
4. Os dados são passados para o template HTML
5. O template renderiza a página com Bootstrap

## 🛠️ Padrões Utilizados

- **Factory Pattern**: Função `create_app()` para criar a instância do Flask
- **Single File App**: Tudo em `app.py` para simplicidade (ideal para aprendizado)
- **Flash Messages**: Para feedback ao usuário
- **Context Manager**: Criação do banco com `app.app_context()`

## 📈 Escalabilidade

Apesar de simples, o sistema pode ser expandido com:

- Autenticação de usuários
- Prontuário eletrônico
- Relatórios em PDF
- Integração com SMS/Email

## 🧰 Ferramentas de Desenvolvimento

- VS Code ou qualquer editor de texto
- Navegador web
- Terminal para comandos

---

> Este documento serve como guia para quem deseja entender, modificar ou expandir o sistema.