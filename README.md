# Sistema de Vagas
## 📂 Clonando o Repositório
1. Clonar o repositório:
  git clone https://github.com/gabrielmchlmnn/vagas.git
2. Ativar ambiente virtual
  Para Windows:
    python -m venv venv
    venv\Scripts\activate
  Para Linux:
    python3 -m venv venv
    venv\Scripts\activate
3. Instalar as dependências
  cd sistemaVagas
  pip install -r requirements.txt
4. Configurar o Banco de Dados
  python manage.py makemigrations
  python manage.py migrate
5. Rodar o sistema
  python manage.py runserver

* Acesso de perfil de empresa:
Email:admin@teste.com 
Senha: admin
