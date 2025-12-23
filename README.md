# 💈 Sistema de Gestão para Barbearia 💈

Este projeto é uma solução completa para gestão de barbearias, permitindo que clientes realizem agendamentos via web e que o barbeiro gerencie sua agenda em tempo real através de um aplicativo conectado a uma API Django.

## Funcionalidades

### Para o Cliente (Interface Web)
- **Agendamento Online:** Escolha de serviço, data e horário disponível.
- **Interface Intuitiva:** Sistema responsivo para marcação rápida.

### Para o Barbeiro (App/Gestão)
- **Agenda Centralizada:** Visualização de nome, horário e serviço de todos os clientes.
- **Bloqueio de Agenda:** Possibilidade de lançar dias de folga ou horários de descanso, impedindo agendamentos nessas datas.
- **Sincronização em Tempo Real:** API robusta para garantir que não haja choque de horários.

## Tecnologias Utilizadas

- **Backend:** [Python 3.x](https://www.python.org/) & [Django 5.2.8](https://www.djangoproject.com/)
- **API:** [Django REST Framework](https://www.django-rest-framework.org/)
- **Banco de Dados:** SQLite (Desenvolvimento)
- **Segurança:** Middleware do Django para proteção de dados.

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
- Python 3.10 ou superior
- Git

## Instalação e Execução

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
   cd nome-do-repositorio
   
3. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv

4. **Ative o ambiente virtual:**

   ```bash
   Windows: .\venv\Scripts\activate

   Linux/Mac: source venv/bin/activate

5. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt

6. **Execute as migrações do banco de dados:**
   
   ```bash
   python manage.py migrate

7. **Inicie o servidor:**

   ```bash
   python manage.py runserver

O servidor estará rodando em: http://127.0.0.1:8000/

## 📡 API Endpoints
Abaixo estão alguns dos principais endpoints disponíveis:

* GET /api/agendamentos/ - Lista todos os horários marcados.

* POST /api/agendamentos/ - Cria um novo agendamento.

* POST /api/folgas/ - Define um período de bloqueio na agenda.

## 🗺️ Roadmap de Desenvolvimento

### Fase 1: MVP (Mínimo Produto Viável) - 🟢 Concluído
- [x] Configuração do ambiente Django e DRF.
- [x] Criação do modelo de Banco de Dados para Agendamentos.
- [x] Implementação da API de reserva de horários.
- [x] Lógica de bloqueio de agenda para folgas do barbeiro.

### Fase 2: Interface e Experiência - 🟡 Em Progresso
- [x] Estruturação do front-end web para clientes.
- [ ] Implementação de sistema de login para clientes.
- [ ] Validação para impedir agendamentos duplicados no mesmo horário.
- [ ] Painel administrativo para o barbeiro visualizar a agenda do dia.

### Fase 3: Expansão e Mobile - ⚪ Planejado
- [ ] Desenvolvimento do aplicativo mobile (React Native/Flutter) para o barbeiro.
- [ ] Sistema de notificações via WhatsApp ou E-mail para confirmar reservas.
- [ ] Relatórios de ganhos mensais e estatísticas de serviços mais pedidos.
- [ ] Suporte a múltiplos barbeiros na mesma unidade.

## Autores
* **Breno Luiz** - [Bren0-lz](https://github.com/Bren0-lz)
