from flask import Flask, render_template
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto')
bcrypt = Bcrypt(app)

from controllers.usuarios import usuarios_bp
from controllers.entradas import entradas_bp

app.register_blueprint(usuarios_bp)
app.register_blueprint(entradas_bp)

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)