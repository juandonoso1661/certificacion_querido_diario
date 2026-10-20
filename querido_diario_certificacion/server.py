from flask import Flask
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto')
bcrypt = Bcrypt(app)

from controllers import usuarios, entradas

if __name__ == "__main__":
    app.run(debug=True)