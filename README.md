Sistema de Vagas
📂 Clonando o Repositório
Clonar o repositório:

bash
Copiar código
git clone https://github.com/gabrielmchlmnn/vagas.git
cd vagas
Ativar ambiente virtual:

Para Windows:
bash
Copiar código
python -m venv venv
venv\Scripts\activate
Para Linux:
bash
Copiar código
python3 -m venv venv
source venv/bin/activate
Instalar as dependências:

bash
Copiar código
pip install -r requirements.txt
Configurar o Banco de Dados:

bash
Copiar código
python manage.py makemigrations
python manage.py migrate
Rodar o sistema:

bash
Copiar código
python manage.py runserver
🔑 Acesso de Perfil de Empresa
Email: admin@teste.com
Senha: admin
