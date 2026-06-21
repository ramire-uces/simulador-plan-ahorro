# Simulador de Plan de Ahorro Automotriz

Proyecto desarrollado con Django como simulador de plan de ahorro automotriz.

## Funcionalidades principales

- Simulación de financiamiento según modelo de vehículo y plan seleccionado.
- Formulario con validaciones mediante Django Forms y JavaScript.
- Registro de solicitudes en base de datos PostgreSQL.
- Panel interno para visualizar solicitudes recibidas.
- API interna desarrollada con Django REST Framework.
- Envío de correo electrónico de confirmación.

## Enlaces de entrega

Repositorio GitHub:

https://github.com/ramire-uces/simulador-plan-ahorro

URL pública en Render:

https://simulador-plan-ahorro.onrender.com/

## Panel interno

URL local:

http://127.0.0.1:8000/panel/solicitudes/

URL en Render:

https://simulador-plan-ahorro.onrender.com/panel/solicitudes/

Credenciales:

Usuario: admin  
Contraseña: Admin1234

## API interna

URL local:

http://127.0.0.1:8000/api/solicitudes/

URL en Render:

https://simulador-plan-ahorro.onrender.com/api/solicitudes/

La API requiere autenticación mediante Basic Auth usando las mismas credenciales del panel interno.

## Despliegue

El proyecto será desplegado en Render utilizando PostgreSQL.

## Nota sobre envío de correos en Render

El sistema registra correctamente las solicitudes en la base de datos PostgreSQL de Render y estas pueden visualizarse desde el panel interno y desde la API interna.

El envío de correos funciona mediante SMTP en entorno local. En Render Free, el envío por SMTP puede verse limitado por el bloqueo de puertos SMTP salientes del plan gratuito.