# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows
Desde backend, en una terminal Command Prompt de VS Code:
```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger: http://127.0.0.1:8000/docs
En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo
100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación:
utilizar únicamente en la red de laboratorio autorizada.

## Firmware
Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h
a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica
el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.
No publicar config.h, contraseñas ni tokens.

## Reto
Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Antes de la sesión
El docente debe probar el firmware en el hardware real y la red del aula,
precargar las herramientas y validar las dependencias en los equipos.
La guía destina 105 minutos a trabajar con el entorno ya preparado.


Nombre: Ronald Sanmartin

Materia: Programación de Sistemas Telemáticos

Objetivo de la Práctica
Desarrollar y configurar una API REST local utilizando FastAPI en Python para gestionar la recepción de datos de un sensor DHT22 y el control de estado de un actuador (LED RGB), integrándola con un microcontrolador ESP32 simulado mediante la plataforma Wokwi.

Instrucciones de Ejecución
Para iniciar el servidor de desarrollo en local, abrir la terminal en la carpeta raíz del proyecto y ejecutar el siguiente comando:.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Respuestas a Preguntas de Comprensión

Diferencia entre los modelos de datos: En este laboratorio utilizamos Pydantic (en schemas.py) exclusivamente para validar la estructura y los tipos de datos que entran y salen de la API. No usamos modelos de bases de datos relacionales ya que el almacenamiento es temporal en memoria.

Manejo de múltiples rutas: FastAPI permite organizar múltiples rutas creando instancias de APIRouter (como en routes.py), las cuales luego se importan y se incluyen en la aplicación principal en main.py mediante app.include_router().

Separación entre rutas y servicios: Extraer la lógica a services.py mantiene el código limpio y modular. Las rutas solo se encargan de recibir la petición HTTP y devolver la respuesta, mientras que los servicios manejan el procesamiento de los datos, facilitando el mantenimiento y la escalabilidad.

Función de store.py: Actúa como un almacenamiento temporal en memoria (base de datos efímera). Permite persistir la lista de lecturas y el estado actual del LED mientras el proceso del servidor se mantenga en ejecución.

Recorrido de una lectura: El ESP32 emite un POST que viaja por el túnel de VS Code hasta el puerto 8000. El endpoint en routes.py recibe la petición y el modelo en schemas.py la valida. Luego, services.py guarda el registro en store.py y consulta el color del LED. El servidor responde con un código 201 y un JSON. Al recibir esta respuesta, el ESP32 extrae el estado y enciende o apaga el LED físicamente.

Registro de Pruebas de Endpoints (Swagger)

GET / - Esperado: 200 | Obtenido: 200

GET /salud - Esperado: 200 | Obtenido: 200

POST /lecturas (Datos correctos) - Esperado: 201 | Obtenido: 201

POST /lecturas (Datos fuera de rango) - Esperado: 422 | Obtenido: 422

GET /lecturas - Esperado: 200 | Obtenido: 200

GET /led - Esperado: 200 | Obtenido: 200

PUT /led (Comando "rojo") - Esperado: 200 | Obtenido: 200

PUT /led (Comando inválido) - Esperado: 422 | Obtenido: 422

Modificación Manual del Código
Al detener la simulación y modificar la respuesta del endpoint en routes.py para la ruta /salud, el cambio se reflejó inmediatamente en las pruebas de Swagger sin necesidad de apagar y encender el servidor manualmente. Esto ocurre gracias al parámetro --reload de Uvicorn, que detecta los archivos guardados y reinicia el servicio en tiempo real.

Resultados del Reto (Promedio de Lecturas)
Se implementó exitosamente el endpoint GET /lecturas/promedio. Las pruebas demostraron el siguiente comportamiento tras cargar lecturas previas:

Con n=3: Se devolvió HTTP 200 con el cálculo exacto de las últimas tres lecturas registradas.

Con n=2: Se devolvió HTTP 200 actualizando el cálculo para los últimos dos registros.

Con n=101 y n=0: Se devolvió el error HTTP 422 (Validation Error), confirmando que Query limita correctamente el intervalo.

Sin datos en memoria: Se devolvió HTTP 404 con el mensaje "No hay lecturas".

Enlaces del Proyecto

Simulación en Wokwi: https://wokwi.com/projects/479003952937986049



