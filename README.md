
# Sistema de Vagas

## 📂 Clonando o Repositório

1. **Clonar o repositório**:  
   ```bash
   git clone https://github.com/gabrielmchlmnn/vagas.git
   cd vagas
   ```

2. **Ativar ambiente virtual**:  
   - **Para Windows**:  
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```  
   - **Para Linux**:  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar as dependências**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o Banco de Dados**:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Rodar o sistema**:  
   ```bash
   python manage.py runserver
   ```

---

### 🔑 **Acesso de Perfil de Empresa**
- **Email**: `admin@teste.com`  
- **Senha**: `admin`

---
