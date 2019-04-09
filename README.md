# App Bike Stgo Backend
## Entorno
El proyecto realizado se encuentra ejecutado con las siguientes herramientas generales. Para mayor detalles de las librerias y/o frameworks visualizar archivo requirements.txt.
- Lenguaje: Python 3.x.y
- Framework: Django 2.x.y
- Base de Datos: sqlite3

## Requisitos
Es necesario tener instalado en el sistema operativo (windows, linux, unix) las siguientes librerias.
- Python, version 3.6 o superior. [instalacion](https://www.python.org/)
- Virtualenv, última version. [instalacion](https://virtualenv.pypa.io/en/latest/)

## Levantar proyecto
Seguir las siguientes instrucciones para poder levantar el proyecto backend.
``` python
# IMPORTANTE: Siempre estar dentro de la carpeta del proyecto.

# 1. Creación de entorno virtual.
virtualenv .envs -p python3

# 2. Activación del entorno virtual. dependiendo el sistema operativo elegir una opción:
source .envs/bin/activate   # linux / unix
.envs/Scripts/activate.bat  # windows cmd
.envs/Scripts/activate.ps1  # windows powershell

# 3. Instalación de requerimientos de la plataforma
pip install -r requirements.txt

# 4. Creación de carpetas log y cache para registrar eventos y cache de la plataforma.
mkdir log cache

# 5. Generación de la base de datos.
python manage.py migrate

# 6. Creación de un usuario staff para poder visualizar el administrador de la plataforma.
python manage.py createsuperuser

# 7. Activación de cron por primera vez ya que se demora más de un minuto ya que determina la comuna
python manage.py runcrons
# luego es necesario registrar en el sistema operativo la funcion que ejecutará el cron. con el siguiente comando:
crontab -e
# y luego agregando la linea
*/1 * * * * cd /ruta/donde/esta-el-proyecto/ && source .envs/bin/activate && python manage.py runcrons
# donde "/ruta/donde/esta-el-proyecto/" es la ruta donde se encuentra el proyecto descargado

# 8. Arrancar servidor local del proyecto. el parametro --insecure se agrega para el correcto funcionamiento de la plataforma en un ambiente de prueba.
python manage.py runserver --insecure
```

## Visualizaciones

### A. Administrador
Para entrar al administrador se solicitara el usuario y contraseña creada en el punto 6 del levantamiento del proyecto.  
URL: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### B. API estaciones
Vista donde se podrán visualizar los datos de las estaciones.  
URL: [http://127.0.0.1:8000/api/store/stations/](http://127.0.0.1:8000/api/store/stations/)
