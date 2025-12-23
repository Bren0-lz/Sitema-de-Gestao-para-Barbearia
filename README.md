# 💈 Sistema de Gestão para Barbearia

Este projeto é uma solução completa para gestão de barbearias, permitindo que clientes realizem agendamentos via web e que o barbeiro gerencie sua agenda em tempo real através de um aplicativo conectado a uma API Django.

## 🚀 Funcionalidades

### 📱 Para o Cliente (Interface Web)
- **Agendamento Online:** Escolha de serviço, data e horário disponível.
- **Interface Intuitiva:** Sistema responsivo para marcação rápida.

### ✂️ Para o Barbeiro (App/Gestão)
- **Agenda Centralizada:** Visualização de nome, horário e serviço de todos os clientes.
- **Bloqueio de Agenda:** Possibilidade de lançar dias de folga ou horários de descanso, impedindo agendamentos nessas datas.
- **Sincronização em Tempo Real:** API robusta para garantir que não haja choque de horários.

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Python 3.x](https://www.python.org/) & [Django 5.2.8](https://www.djangoproject.com/)
- **API:** [Django REST Framework](https://www.django-rest-framework.org/)
- **Banco de Dados:** SQLite (Desenvolvimento)
- **Segurança:** Middleware do Django para proteção de dados.

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
- Python 3.10 ou superior
- Git

## 🔧 Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
   cd nome-do-repositorio
   
2. **Crie um ambiente virtual:**

```bash
python -m venv venv
Ative o ambiente virtual:

Windows: .\venv\Scripts\activate

Linux/Mac: source venv/bin/activate
```

**Instale as dependências:**

```bash
pip install -r requirements.txt
Execute as migrações do banco de dados:
```

```bash
python manage.py migrate
Inicie o servidor:
```

```bash
python manage.py runserver
```
O servidor estará rodando em: http://127.0.0.1:8000/

## 📡 API Endpoints
Abaixo estão alguns dos principais endpoints disponíveis:

GET /api/agendamentos/ - Lista todos os horários marcados.

POST /api/agendamentos/ - Cria um novo agendamento.

POST /api/folgas/ - Define um período de bloqueio na agenda.

Desenvolvido por Seu Nome
