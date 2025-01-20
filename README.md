# API de Insignias Educativas

## Descripción General
Esta API de Python proporciona un backend para gestionar insignias educativas, permitiendo la creación, recuperación y asignación de insignias a usuarios en función de sus logros. El sistema también incluye un sistema de progresión basado en niveles, donde los usuarios pueden ganar experiencia para desbloquear nuevas insignias.

## Arquitectura
La API sigue una arquitectura hexagonal, separando la lógica de negocio del núcleo de las preocupaciones externas como bases de datos, frameworks web y servicios de terceros. Esto promueve el acoplamiento débil, la testabilidad y el mantenimiento.

- **Dominio Central**: Contiene la lógica de negocio para insignias, usuarios y niveles.
- **Adaptadores**: Proporcionan interfaces a sistemas externos como bases de datos, AWS S3 y Amazon Cognito.
- **Aplicación**: Maneja solicitudes entrantes, coordina el dominio central y delega tareas a los adaptadores.
- **Framework**: Proporciona el framework web FastAPI y maneja enrutamiento, ciclos de solicitud/respuesta y manejo de errores.

## Instalación y Ejecución

### 1. Clonar el repositorio:
```bash
git clone https://github.com/JuanDAC/insignias-api.git
```

### 2. Configurar variables de entorno:
Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables de entorno:
```
SQLALCHEMY_DATABASE_URI=postgresql://usuario:contraseña@host:puerto/base_de_datos
AWS_ACCESS_KEY_ID=tu_clave_de_acceso
AWS_SECRET_ACCESS_KEY=tu_clave_secreta
AWS_S3_BUCKET_NAME=tu_nombre_de_bucket
COGNITO_USER_POOL_ID=tu_id_de_pool_de_usuarios
COGNITO_CLIENT_ID=tu_id_de_cliente
```

### 3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor de desarrollo:
```bash
pyrun -a dev
```

## Utilizando el script pyrun
El script `pyrun` proporciona una forma conveniente de automatizar diversas tareas:

- **Desarrollo**: Inicia el servidor de desarrollo.
- **Despliegue**: Despliega la aplicación en AWS o un servidor físico.
- **Gestión de bases de datos**: Crea o migra la base de datos.
- **Docker**: Construye y ejecuta un contenedor Docker.

### Ejemplo de uso:
```bash
# Iniciar el servidor de desarrollo
pyrun -a dev

# Desplegar en AWS
pyrun -a deploy:aws

# Crear la base de datos
pyrun -a start:aws:db
```

## Endpoints de la API

### Insignias:
- `POST /api/insignias/`: Crear una nueva insignia.
- `GET /api/insignias/`: Listar todas las insignias.
- `GET /api/insignias/{id}/`: Obtener una insignia específica.
- `PUT /api/insignias/{id}/imagen/`: Subir una imagen para una insignia.

### Usuarios:
- `POST /api/usuarios/register/`: Registrar un nuevo usuario.
- `POST /api/usuarios/login/`: Iniciar sesión de un usuario existente.
- `GET /api/usuarios/{id}/nivel/`: Obtener el nivel y la experiencia de un usuario.
- `POST /api/usuarios/{id}/experiencia/`: Agregar experiencia a un usuario.

### Asignaciones:
- `POST /api/insignias/{id}/asignar/`: Asignar una insignia a un usuario.

## Manejo de Errores
La API devuelve códigos de estado HTTP apropiados y respuestas JSON para errores.