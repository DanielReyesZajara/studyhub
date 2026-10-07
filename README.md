# StudyHub - proyecto base para practicar EGC

Simulacro educativo original inspirado en el formato de Examen42 y en las
prácticas de UVLHub. No es un examen oficial ni una copia de UVLHub.

## Empieza aquí

1. Lee ENUNCIADO.md.
2. Este proyecto contiene un fallo funcional y errores de configuración
   deliberados. No esperes que Docker funcione antes del ejercicio D.
3. Para los ejercicios A-C trabaja localmente con SQLite. Docker utilizará MariaDB.
4. Guarda las soluciones aparte para no verlas antes de intentarlo.

## Instalación local (Linux / terminal Bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
flask --app wsgi:app db upgrade
flask --app wsgi:app run --host=0.0.0.0 --port=5000 --debug
```

Abre http://localhost:5000. En Windows: crea el entorno con `py -m venv .venv`,
actívalo con `.venv\Scripts\Activate.ps1` y copia el entorno con
`Copy-Item .env.example .env`. Después los comandos `python` y `flask` son iguales.
Gunicorn se usa en Linux, Docker o Render; no es el servidor local de Windows.

## Pruebas y base de datos

```bash
python -m pytest -q
python -m pytest tests/unit -q
python -m pytest --cov=app --cov-report=term-missing --cov-report=xml
```

Las unitarias no necesitan base de datos. Las de integración usan una SQLite
temporal por test. Para MariaDB, configura TEST_DATABASE_URL con una BD aislada
cuyo nombre termine en `_test`; los tests crean y eliminan sus tablas.

La migración inicial ya está incluida. Usa `flask db upgrade`; no necesitas
`flask db init` ni generar otra migración para arrancar.

## Contrato de la aplicación

- Crear tarea: título de 1 a 120 caracteres después de quitar espacios; descripción
  opcional de hasta 500 caracteres. Una tarea nueva empieza pendiente.
- Completar y reabrir: cada acción debe invertir el estado.
- Eliminar: la tarea desaparece definitivamente.
- No existe edición, registro de usuarios ni autenticación.

API: GET/POST `/api/tasks`, POST `/api/tasks/<id>/toggle`,
DELETE `/api/tasks/<id>`, GET `/health`.
POST de creación devuelve 201; datos inválidos 400; inexistente 404; eliminación 204.

## Estructura

```text
app/                     factoría, modelo, rutas, reglas, HTML y CSS
tests/unit/              reglas puras
tests/integration/       cliente de Flask y base temporal
migrations/              esquema inicial de la base
docker/                  imagen, Compose dev/prod, Nginx y arranque
.github/workflows/ci.yml  workflow inicial que debes ampliar
scripts/                 espera de la base
docs/                    material de ejercicios Git
```

## Docker (después de reparar el ejercicio D)

```bash
docker compose -f docker/docker-compose.dev.yml up -d --build
docker compose -f docker/docker-compose.dev.yml ps
docker compose -f docker/docker-compose.dev.yml logs web --tail=40
```

Abre http://localhost:8080. Usa `down` para cerrar conservando datos; `down -v`
elimina el volumen de esta práctica. Dev y prod tienen nombres distintos y
volúmenes distintos, pero ambos publican 8080: detén uno antes de iniciar el otro.

## Publicar para practicar GitHub

El ZIP incluye `.git`, rama main y un commit inicial. Crea en GitHub un repositorio
vacío (sin README, licencia ni .gitignore) y copia su URL real:

```bash
git remote add origin <URL_REAL_DEL_REPOSITORIO>
git push -u origin main
```

El marcador `<URL_REAL_DEL_REPOSITORIO>` debe sustituirse; no es un comando listo
para pegar. Clona después en una carpeta diferente para empezar el simulacro.
Si estudias sin GitHub, trabaja en esta copia y documenta issues/PR en archivos.
Si el ZIP oculta `.git`, activa la vista de archivos ocultos.

## Alcance

Solo para estudio: sin autenticación, CSRF ni endurecimiento de producción.
Las credenciales del ejemplo son ficticias. No guardes credenciales reales en Git.
No requiere Vagrant, Ansible, Certbot, Watchtower ni Kubernetes.
