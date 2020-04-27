# Servidor de Examenes para Geometría Analítica II
Genera examenes aleatorios para el curso de Geometría Analíticia II (2020-2) impartido por el Dr. Pablo Suárez Serrato en la Facultad de Ciencias de la UNAM.
Ayudantes: Jose Crispín Ruíz Pantaleón, Haydee Contreras Peruyero y Elsa Fernanda Torres Feria

## Caracteristicas
- Examenes aleatorios que se guardan en un Google Sheet
- Es capaz de calificar un examen.

## Desarrollo
- Descargar el repositorio 
- Crear un entorno virtual de Python3
- Ejecutar 
  `pip install -r requirements.txt`
  para instalar todos los mudulos/frameworks necesarios.
- Pedir el archivo de varibles de entorno al admin.
- Create a Django SU
  `python manage.py createsuperuser`
- Ejecutar
  `python manage.py runserver [::]:2000`
- Ir al admin del proyecto [http://127.0.0.1:2000/admin/](http://127.0.0.1:2000/admin/) e ingresar tu usuario y contraseña.
- Crear el primer examen con los datos proporcionados en el archivo `inicial_data.txt`
- Ir a [http://127.0.0.1:2000/](http://127.0.0.1:2000/) para ver el projecto.
