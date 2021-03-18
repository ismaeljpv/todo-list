Instrucciones para iniciar servidor Flask.

Dentro de la carpeta del proyecto, seguir los siguientes pasos:

1) Iniciar ambiente de desarrollo virtual con el comando   
    `$ python3 -m venv venv`
2) Una vez iniciado el ambiente virtual, activarlo con el comando   
    `$ . venv/bin/activate`
3) Instalar flask localmente    
    `$ pip3 install Flask`
4) Instalar driver de postgreSQL   
    `$ pip3 install psycopg2`   
5) Instalar libreria de seguridad   
    `$ pip3 install werkzeug`   
6) Identificar las variables de entorno   
    `$ export FLASK_APP= {nombre_del_archivo}`  
    `$ export FLASK_ENV= {ambiente}`  
    `$ export FLASK_DATABASE= {nombre_database}`  
    `$ export FLASK_DATABASE_HOST= {host_database}`  
    `$ export FLASK_DATABASE_USER= {user_database}`  
    `$ export FLASK_DATABASE_PASSWORD= {clave_database}`  
7) Ejecutar la aplicación   `$ flask run`  