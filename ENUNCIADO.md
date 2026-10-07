# Simulacro práctico de EGC - StudyHub

Proyecto original para estudiar con las tecnologías de UVLHub. No es un examen oficial ni una predicción de lo que entrará.

## 0. Antes de empezar

**Objetivo:** reparar, probar y desplegar una aplicación pequeña de tareas de estudio. Tecnología: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, MariaDB, pytest, GitHub Actions, Docker Compose y Nginx.

**Formato:** parte principal de 3 horas aproximadamente, con 10 puntos de autoevaluación. Las ampliaciones son independientes y pueden hacerse otro día. Los tiempos y puntos son orientativos.

**Archivos:** proyecto base con errores, este enunciado y soluciones en un paquete distinto. Extrae el ZIP base en una carpeta nueva. No uses la copia corregida durante el simulacro.

**Preparación fuera del tiempo de examen:** instala Git, Python 3.12 y Docker con Compose. Sigue README.md para crear el entorno, instalar dependencias, copiar .env.example a .env y aplicar la migración inicial. En A-C se utiliza SQLite local; en D se utilizará MariaDB dentro de Docker.

El ZIP incluye un repositorio Git con rama main y un commit inicial. Para practicar GitHub, publica esa copia en un repositorio vacío de tu cuenta siguiendo README.md. Después clónalo en otra carpeta. Si alguien publica primero el proyecto base, puedes hacer fork de ese repositorio, como en el examen de referencia. No hay un repositorio StudyHub remoto creado de antemano.

Trabaja de forma secuencial. Cada paso marcado **[CAPTURA]** requiere una imagen con el comando y su salida, o la pantalla web correspondiente. Nombra las capturas A.01.png, C.03.png, etc. Usa mensajes de commit en inglés con formato `tipo: descripción`.

Para estudiar sin conexión a GitHub: sustituye issues y PR por documentos con su descripción y un registro de las fusiones locales. Esto permite practicar Git, pero no demuestra haber usado GitHub ni Actions.

## 1. Conoce la aplicación

StudyHub permite crear, completar, reabrir y eliminar tareas. Cada tarea tiene título, descripción y estado pendiente/completada.

- El título es texto de 1 a 120 caracteres después de quitar espacios de los extremos.
- La descripción es opcional, de hasta 500 caracteres.
- Cada tarea nueva empieza pendiente. Completar/reabrir debe invertir su estado.
- Eliminar una tarea la quita de la base de datos.
- No se pide añadir usuarios, autenticación ni nuevas funciones.

Para A-C abre `http://localhost:5000`. Tras arreglar D abre `http://localhost:8080`.

Arquitectura objetivo de Docker: navegador → Nginx:80 → web:5000 → db:3306. El equipo accede por el puerto 8080. Solo necesitas los servicios web, db y nginx. Compose crea su red compartida automáticamente.

El proyecto conserva la forma de trabajar de UVLHub, pero reduce su tamaño y dependencias. SQLite es una ayuda local para estudiar; MariaDB es la base objetivo de Docker. No se evalúan formatos UVL ni integración con Zenodo.

## A. Git y corrección de un error - 2,5 puntos / 40 min

**A.01 [CAPTURA]** Clona tu repositorio publicado. Comprueba el remoto, la rama main y el historial inicial. Si estudias solo en local, comprueba el repositorio incluido en el ZIP.

**A.02 [CAPTURA]** Crea la rama `fix/reopen-task`, cambia a ella y comprueba en qué rama estás.

**A.03 [CAPTURA]** Ejecuta StudyHub. Crea una tarea, complétala e intenta reabrirla. Registra lo esperado y lo observado. Ejecuta las pruebas iniciales y explica por qué pueden pasar aunque exista el error.

**A.04 [CAPTURA]** Abre una issue con título, pasos de reproducción, resultado esperado, resultado real y entorno. No basta con escribir «no funciona».

**A.05 [CAPTURA]** Añade una prueba de regresión que falle por ese comportamiento. Muestra primero el fallo. Corrige el código de la aplicación y ejecuta de nuevo las pruebas. No cambies el comportamiento esperado del test para ocultar el error.

**A.06** Confirma únicamente los archivos del arreglo y la prueba con un mensaje que explique el cambio. Publica la rama.

**A.07 [CAPTURA]** Abre una PR hacia main, referencia la issue con `Closes #N`, describe el arreglo y cómo se comprobó. Fusiona la PR y actualiza tu main local. En GitHub se cerrará la issue al fusionar en la rama por defecto.

**A.08 [CAPTURA]** Muestra el historial de todas las ramas. Explica brevemente qué hicieron add, commit, push y pull en este flujo.

**Criterios:** reproducción e issue 0,5; rama/commits/PR 0,75; arreglo y prueba de regresión 1; explicación del historial 0,25.

## B. Pruebas automatizadas - 2,5 puntos / 45 min

Crea la rama `test/task-behaviour` desde main actualizado. Puedes añadir tests, pero no eliminar las pruebas iniciales ni las de regresión.

**B.01 [CAPTURA]** Añade pruebas unitarias de títulos: válido, espacios alrededor, vacío, solo espacios y límite 120/121. Comprueba también completar y reabrir. Puedes usar parametrización.

**B.02 [CAPTURA]** Añade pruebas de integración con el cliente de Flask: crear una tarea devuelve 201 y la persiste; título inválido devuelve 400 y no inserta nada; completar y reabrir se guardan; eliminar devuelve 204; actuar sobre un identificador inexistente devuelve 404.

**B.03** Comprueba que las pruebas usan una base temporal/aislada y no la base local de estudio. La fixture inicial ya está preparada para ello. Incluye una comprobación del registro almacenado, además del código HTTP.

**B.04 [CAPTURA]** Ejecuta toda la batería y mide cobertura con pytest-cov. Genera `coverage.xml` y muestra las líneas sin cubrir. Amplía las pruebas hasta alcanzar al menos un 80 % de cobertura de líneas del paquete app.

**B.05** En `docs/pruebas.md`, explica la diferencia entre prueba unitaria, integración y regresión usando un ejemplo real de tus tests. La cobertura indica qué código se ejecutó, no si comprobaste bien sus resultados.

**B.06 [CAPTURA]** Confirma los cambios, publica la rama y fusiónala en main mediante PR. Actualiza tu main local antes de pasar a C.

**Criterios:** casos unitarios 0,75; integración y persistencia 1; aislamiento/cobertura 0,5; explicación e integración en Git 0,25.

## C. GitHub Actions y cobertura - 2 puntos / 35 min

Crea la rama `ci/tests-and-coverage`. Parte del archivo `.github/workflows/ci.yml` incluido; no crees un workflow que finja un resultado correcto sin ejecutar las pruebas.

**C.01 [CAPTURA]** Configura el workflow para ejecutarse en push a las ramas de trabajo, pull_request hacia main y manualmente mediante workflow_dispatch.

**C.02 [CAPTURA]** El job `pruebas` debe usar una matriz de Python 3.11 y 3.12, instalar requirements-dev.txt y ejecutar tanto las unitarias como las de integración. SQLite temporal basta para este apartado.

**C.03 [CAPTURA]** Crea un job separado `cobertura`. Debe preparar su propio entorno, ejecutar pytest-cov, generar coverage.xml, fallar si la cobertura es inferior al 80 % y guardar el XML como artefacto descargable.

**C.04 [CAPTURA]** Haz commit y push. Comprueba en Actions las dos ejecuciones de la matriz y el job de cobertura. Descarga el artefacto y localiza una línea útil del log.

**C.05 [CAPTURA]** Demuestra que CI detecta una regresión: en una rama temporal cambia el comportamiento de reabrir para que sea incorrecto, haz push y muestra una ejecución roja. Restaura el comportamiento mediante un commit y muestra la ejecución verde. No integres la rama rota en main.

**C.06** Fusiona la PR del workflow. En `docs/ci.md`, identifica evento, workflow, job, step, runner y artefacto en tu archivo. Explica por qué un job no hereda las dependencias instaladas en otro.

**Criterios:** eventos y matriz 0,75; cobertura separada y artefacto 0,75; evidencias de fallo/éxito y explicación 0,5.

## D. Docker, Compose y servicios básicos - 3 puntos / 60 min

Crea la rama `fix/docker`. El Dockerfile prepara una imagen Python; Compose debe organizar web, MariaDB y Nginx. Trabaja desde la raíz del proyecto y conserva los nombres de servicio.

**D.01 [CAPTURA]** Comprueba las versiones de Docker y Compose. Examina Dockerfile y el archivo de desarrollo. Identifica base, carpeta de trabajo, instalación, copia de código, puerto y arranque.

**D.02 [CAPTURA]** Intenta construir y levantar desarrollo. Diagnostica y corrige los errores de configuración hasta conseguir: imagen construida desde la raíz del proyecto, web conectando a MariaDB por su nombre de servicio y Nginx enviando las peticiones al puerto correcto de web. Guarda evidencia de los errores y de su reparación. No necesitas modificar la configuración interna de MariaDB.

**D.03 [CAPTURA]** Comprueba los tres servicios con ps, revisa logs de web y nginx y abre la aplicación en el navegador. En los logs debe verse la aplicación de migraciones y el arranque de Flask.

**D.04 [CAPTURA]** Usa config --services para listar servicios y exec para ejecutar una orden en web. Comprueba con `flask db current` que existe una revisión aplicada. Explica para qué sirve `flask db upgrade` y por qué no tienes que crear otra migración inicial.

**D.05 [CAPTURA]** Crea una tarea con un título reconocible. Ejecuta down y vuelve a levantar el mismo archivo de desarrollo. La tarea debe seguir allí. Explica cuál es el volumen de datos y cuál es el bind mount del código.

**D.06** En `docs/docker.md`, explica: imagen/contenedor; servicio/contenedor; EXPOSE/publicar un puerto; dirección db/localhost dentro de web; down/down -v. No ejecutes down -v antes de guardar la evidencia de persistencia.

**D.07 [CAPTURA]** Detén desarrollo. Revisa el archivo de producción y su entrypoint. Configúralos para usar Gunicorn, escuchar en 5000 y mantener debug desactivado. Conserva la espera a la base y la aplicación de migraciones. Levanta producción y verifica los tres servicios y la web.

**D.08 [CAPTURA]** Confirma, publica y fusiona los cambios mediante PR. Si sigues usando producción, recuerda que sus datos y volúmenes son diferentes de los de desarrollo. Ambos usan 8080 en el equipo: no los levantes a la vez.

**Criterios:** diagnóstico y desarrollo 1; uso de comandos y persistencia 1; producción sin debug 0,75; explicaciones y Git 0,25.

## E. Ampliación de Git - fuera de los 10 puntos

Haz estos ejercicios en ramas nuevas, partiendo siempre de main actualizado. Usa archivos en docs para que no dependan de los fallos de la aplicación.

**E.01 [CAPTURA] Cherry-pick:** crea una rama ch1 con tres commits. Cada commit debe añadir un archivo distinto: docs/c1.txt, docs/c2.txt y docs/c3.txt. En otra rama, basada en main, incorpora únicamente el segundo commit. Demuestra que existe c2.txt y no existen c1.txt ni c3.txt.

**E.02 [CAPTURA] Rebase interactivo:** crea una rama rbs con cinco commits a, b, c, d y e sobre docs/rebase.txt. Antes de publicarla, combina b, c y d en uno. El historial añadido a main debe quedar a, bcd, e. Muestra antes y después.

**E.03 [CAPTURA] Conflicto:** crea dos ramas desde el mismo main y modifica la misma línea de docs/equipo.txt con responsables distintos. Fusiona una en la otra y resuelve conservando ambos nombres. No te limites a elegir una versión.

**E.04 [CAPTURA] Stash y revert:** guarda con stash un cambio sin confirmar, cambia de rama y vuelve a recuperarlo. Por separado, crea un commit de prueba y deshazlo mediante revert; demuestra que el historial conserva ambos commits.

**E.05 [CAPTURA] Hook:** añade un commit-msg que rechace mensajes sin el formato tipo: descripción, actívalo mediante core.hooksPath y muestra un rechazo y un commit válido. Explica que un hook local no se activa automáticamente al clonar.

## F. Ampliación de CI/CD - fuera de los 10 puntos

**F.01 [CAPTURA] MariaDB:** añade un workflow que ejecute las pruebas de integración con MariaDB 10.11 y 11.4. Cada ejecución debe usar una BD exclusiva studyhub_test y esperar a que el servicio esté disponible.

**F.02 [CAPTURA] Release:** configura una release automática al subir un tag v*. Antes de crearla, ejecuta las pruebas del mismo tag. Crea una etiqueta anotada v0.1.0 y demuestra la release. No basta con crear el tag local.

**F.03 [CAPTURA] Render:** prepara un despliegue de StudyHub con Gunicorn y una MariaDB externa accesible. Usa variables de entorno; el filesystem local efímero no es la persistencia objetivo. Añade un workflow que, solo tras superar las pruebas del tag, solicite desplegar ese mismo commit mediante un deploy hook guardado como secret. Desactiva el despliegue automático independiente para no saltarte el control de pruebas.

La solicitud HTTP aceptada no demuestra por sí sola que la aplicación esté desplegada. Comprueba el estado final del proveedor y la URL/health. Si no tienes servicio o base externa disponibles, entrega la configuración y explica qué falta; no inventes evidencias. La disponibilidad y el coste dependen de tus cuentas. No es necesario contratar un plan para practicar la parte principal.

**F.04 opcional:** vincula Codacy y sube el informe XML del job cobertura usando un token como secret. Distingue análisis de calidad y porcentaje de cobertura. Puedes practicar además listado de dependencias desactualizadas y pip-audit.

## G. Ampliación de pruebas y entorno - fuera de los 10 puntos

**G.01 [CAPTURA] Selenium:** crea una prueba de interfaz que añada una tarea, la complete, la reabra y la elimine. Usa esperas explícitas y un título único. Ejecuta sobre una instancia de estudio, sin datos importantes.

**G.02 [CAPTURA] Locust:** prueba GET /api/tasks con 10 usuarios, aparición de 2 usuarios/segundo y duración de 30 segundos. Informa de peticiones, fallos y tiempos de respuesta. No se exige una cifra universal de rendimiento.

**G.03 [CAPTURA] Dev container:** configura VS Code para abrir el servicio web de Compose y trabajar en /workspace. Comprueba que Python y Flask se encuentran dentro del contenedor.

## Entrega y autoevaluación

Entrega un ZIP denominado `studyhub-<uvus>.zip` con el repositorio trabajado (incluida .git), carpeta screenshots y un README_entrega.txt. Este último debe indicar repositorio, PR/issues, apartados realizados, comandos de prueba, cobertura, incidencias y URL desplegada si procede. No incluyas .venv, .env, cachés ni credenciales reales.

Lista final: arreglo reproducible; tests con resultados comprobados; CI ejecutándose; tres servicios Docker; tarea persistente tras down/up; Gunicorn sin debug; historial y evidencias coherentes. Las ampliaciones no sustituyen la parte principal.

## Referencias y adaptación

Formato de referencia: Examen42.md y https://github.com/EGCETSII/EGC-2324-1830. Se conserva la secuencia de tareas y evidencias, con enunciados nuevos y código original. Se sustituye Django/PostgreSQL por Flask/MariaDB y el bloque Vagrant/Ansible por pruebas, ajustándose a las prácticas entregadas.

Material consultado: EGC_2026-27_P1.pdf (CI/CD, pp. 8-16, 18-22, 27-37), EGC_2026-27_P2.pdf (ramas y Git, pp. 15-44), EGC_2026-27_P3.pdf (pytest, cobertura, Selenium y Locust, pp. 6-18), EGC_2025-26_P5.pdf (Docker/Compose/dev containers, pp. 10-33) y p2_usuario_B.pdf (flujo y ejercicios Git, pp. 4-17). La mezcla de cursos se conserva como material de estudio; no se infiere un temario oficial nuevo.

Stack de referencia: https://github.com/EGCETSII/uvlhub, requirements.txt y docker/docker-compose.dev.yml. Para este simulacro se utilizan dependencias reducidas y versiones de Python 3.11/3.12; la matriz 3.13/3.14 propuesta en P1 puede practicarse como extensión tras revisar compatibilidad.
