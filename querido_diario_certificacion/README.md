Querido Diario - Aplicación Web MVC con Flask

Un diario personal web interactivo construido con el patrón de diseño Modelo-Vista-Controlador (MVC), modularizado mediante Flask Blueprints, con autenticación segura de usuarios, validaciones del lado del servidor y gestión completa de entradas (CRUD).

Autor:

Nombre y Apellido: Juan Donoso 4°C 

Proyecto: Querido Diario (Certificación Flask MVC)

Tecnologías y Librerías Utilizadas:

Lenguaje: Python 3.x

Framework Web: Flask

Modularización: Flask Blueprints (Blueprint)

Base de Datos: MySQL

Seguridad y Encriptación: flask-bcrypt (Hashing de contraseñas con Blowfish)

Variables de Entorno: python-dotenv

Entorno de Dependencias: pipenv

Plantillas HTML: Jinja2

Estilos CSS: CSS3 / Bootstrap

Estructura del Proyecto:

querido_diario_certificacion/
│
├── config/
│   ├── __init__.py
│   └── mysqlconnection.py   # Conexión y ejecución de consultas en MySQL
│
├── controllers/
│   ├── __init__.py
│   ├── usuarios.py          # Blueprint 'usuarios_bp': Rutas de inicio, registro, login y logout
│   └── entradas.py          # Blueprint 'entradas_bp': Rutas del dashboard, CRUD de entradas y búsquedas
│
├── models/
│   ├── __init__.py
│   ├── usuario.py           # Clase Usuario: Validaciones, guardado, hashing y búsqueda
│   └── entrada.py           # Clase Entrada: Consultas de la bitácora, actualización y borrado
│
├── static/
│   └── css/
│       └── style.css        # Hojas de estilo personalizadas
│
├── templates/
│   ├── 404.html             # Vista de error 404 personalizada
│   ├── base.html            # Plantilla base con bloques Jinja2
│   ├── dashboard.html       # Vista principal de entradas del usuario
│   ├── editar_entrada.html  # Formulario de edición de notas
│   ├── login.html           # Vista de inicio de sesión y registro
│   ├── nueva_entrada.html   # Formulario de creación de nota
│   └── ver_entrada.html     # Vista detallada de una entrada
│
├── .env                     # Variables de entorno (SECRET_KEY, etc.)
├── .gitignore               # Archivos excluidos de control de versiones
├── Pipfile                  # Gestión de dependencias de Pipenv
├── README.md                # Documentación del proyecto
└── server.py                # Archivo principal de ejecución y registro de Blueprints

:Características Principales

Arquitectura Modular (Blueprints): Desacoplamiento total entre los módulos de autenticación (usuarios_bp) y la gestión del diario (entradas_bp).

Autenticación y Seguridad:

Encriptación de contraseñas mediante Bcrypt.

Gestión de sesiones activas de usuario (session).

Protección de rutas privadas mediante verificación de sesión.

Validación de Datos Robustas:

Verificación de formato de correo electrónico mediante expresiones regulares.

Restricciones de longitud para nombre, apellido y contraseña.

Validación de correo único previa inserción en la base de datos.

Despliegue de mensajes informativos de error mediante flash.

Manejo de Errores Personalizado: Manejador de estado @app.errorhandler(404) que renderiza una vista amigable (404.html).

Gestión Completa de Entradas (CRUD):

Crear, leer, editar y eliminar entradas de diario.

Filtro y búsqueda de entradas por palabras clave.

Instrucciones de Ejecución:

Clonar/Descargar el repositorio y navegar a la carpeta raíz:

cd querido_diario_certificacion


Instalar dependencias con Pipenv:

pipenv install


Configurar el archivo .env:
Crea o verifica que exista el archivo .env en la raíz con la clave secreta:

SECRET_KEY=tu_clave_secreta_aqui


Ejecutar la aplicación:

pipenv run python server.py


Acceder desde el navegador:
Visita http://localhost:5000