# Documentación Técnica - IntelliGuard

## Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Base de       │
│   (HTML/JS/CSS) │◄──►│   (Flask)       │◄──►│   Datos (SQLite)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   IA Models     │
                       │  (OpenCV/YOLO)  │
                       └─────────────────┘
```

### Patrón de Diseño

El sistema utiliza un patrón **MVC (Model-View-Controller)** modificado:

- **Model**: Clases de base de datos en `models/`
- **View**: Archivos HTML y CSS en `Frontend/`
- **Controller**: Rutas Flask en `routes/` y servicios en `services/`

## Análisis de Módulos

### 1. Módulo de Autenticación

#### Backend (`Login Administrador/Backend/`)

**Archivo Principal**: `app.py`
```python
# Configuración de Flask con JWT
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323'
jwt = JWTManager(app)
```

**Modelo de Usuario**: `models/usuario.py`
- Clase `Usuario`: Representa un usuario del sistema
- Clase `BaseDatosUsuarios`: Manejo de operaciones CRUD
- Autenticación basada en roles (Administrador = rol_id = 2)

**Rutas de Autenticación**: `routes/auth_routes.py`
- `POST /auth/login`: Autenticación de usuarios
- `POST /auth/logout`: Cierre de sesión
- Protección con decoradores de roles

#### Frontend (`Login Administrador/Frontend/`)

**Gestión de Sesiones**: `utils/sessionManager.js`
```javascript
// Verificación de token JWT
function validTokenSession() {
    const token = getCookie('jwt');
    if (!token) {
        window.location.href = 'index.html';
    }
}
```

**Configuración**: `utils/config.js`
```javascript
const API_URL = 'http://localhost:5000';
```

### 2. Módulo de Reconocimiento Facial

#### Implementación (`Identificar Ingresante/Backend/utils/reconocimiento_facial.py`)

**Clase Principal**: `ReconocimientoFacial`

**Métodos Principales**:

1. **`reconocimiento_facial(imagen_archivo)`**:
   ```python
   def reconocimiento_facial(imagen_archivo):
       modelo_reconocimiento = cv2.face.FisherFaceRecognizer_create()
       modelo_reconocimiento.read('models/modeloEstudiantes.xml')
       # Procesamiento de imagen y detección de rostros
   ```

2. **`capturar_rostro(video_path, estudiante_path, codigoEstudiante)`**:
   - Captura automática de frames de video
   - Detección de rostros con Haar Cascade
   - Guardado de imágenes procesadas

3. **`entrenar_modelo()`**:
   - Lectura de imágenes de entrenamiento
   - Entrenamiento del modelo FisherFace
   - Guardado del modelo entrenado

**Parámetros de Configuración**:
- **Escala de Imagen**: 150x150 píxeles
- **Umbral de Similitud**: 500 (configurable)
- **Clasificador**: `haarcascade_frontalface_default.xml`

### 3. Módulo de Detección de Objetos

#### Implementación (`Registro de Pertenencias/Backend/utils/deteccion_objetos.py`)

**Clase Principal**: `DeteccionObjetos`

**Método Principal**: `identificarObjeto(imagen)`
```python
def identificarObjeto(imagen):
    modelo = YOLO('models/ModelObjetoFinal.pt')
    resultados = modelo(imagen, imgsz=640, conf=0.80)
    # Extracción de bounding box y etiqueta
```

**Configuración YOLOv8**:
- **Tamaño de Imagen**: 640x640 píxeles
- **Confianza Mínima**: 80%
- **Modelo**: `ModelObjetoFinal.pt` (entrenado personalmente)

### 4. Módulo de Gestión de Pertenencias

#### Modelo de Datos (`Registro de Pertenencias/Backend/models/`)

**Clase Pertenencia**:
```python
class Pertenencia:
    def __init__(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, 
                 id_estudiante, id_ultimo_estado, fecha_ultima_actividad, 
                 estado_text, objeto_text):
```

**Clase BaseDatosPertenencia**:

**Métodos Principales**:

1. **`registrar_pertenencia()`**:
   ```python
   def registrar_pertenencia(self, tipo_objeto, imagen_pertenencia, 
                           id_estudiante, id_ultimo_estado, fecha_ultima_actividad):
       # Inserción en base de datos con manejo de errores
   ```

2. **`consultar_pertenencias_codigos()`**:
   - Consulta múltiples pertenencias por códigos
   - Ordenamiento personalizado según lista de entrada
   - Join con tabla de estados

3. **`cambiar_estado_pertenencias()`**:
   - Actualización de estado y fecha de actividad
   - Transacciones seguras con rollback

#### Flujo de Proceso

**Registro de Nueva Pertenencia**:
1. Identificación del estudiante (reconocimiento facial)
2. Captura y detección del objeto (YOLOv8)
3. Registro en base de datos
4. Asociación estudiante-objeto

**Control de Salida**:
1. Verificación de identidad del estudiante
2. Consulta de pertenencias registradas
3. Actualización de estado a "salida"
4. Registro en historial

### 5. Módulo de Reportes

#### Funcionalidades

**Tipos de Reportes**:
- Historial de pertenencias por estudiante
- Estadísticas de entrada/salida
- Reportes por período de tiempo
- Análisis de tipos de objetos

**Implementación**:
- Consultas SQL complejas con JOINs
- Agregación de datos por múltiples criterios
- Exportación de datos en diferentes formatos

## Base de Datos

### Esquema Completo

#### Tabla: `usuarios`
```sql
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    hash_contraseña TEXT NOT NULL,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
);
```

#### Tabla: `rol_usuario`
```sql
CREATE TABLE rol_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol TEXT NOT NULL
);
```

#### Tabla: `estudiantes`
```sql
CREATE TABLE estudiantes (
    idEstudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    codigoEstudiante TEXT NOT NULL UNIQUE,
    nombresEstudiante TEXT NOT NULL,
    carreraEstudiante TEXT NOT NULL,
    planEstudiante TEXT NOT NULL
);
```

#### Tabla: `pertenencias`
```sql
CREATE TABLE pertenencias (
    codigoPertenencia INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoObjeto INTEGER,
    imagenPertenencia TEXT,
    idEstudiante INTEGER,
    idUltimoEstado INTEGER,
    FechaUltimaActividad INTEGER,
    FOREIGN KEY (idUltimoEstado) REFERENCES estado_pertenencias(id),
    FOREIGN KEY (idEstudiante) REFERENCES estudiantes(idEstudiante)
);
```

#### Tabla: `estado_pertenencias`
```sql
CREATE TABLE estado_pertenencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL
);
```

#### Tabla: `registros_pertenencia`
```sql
CREATE TABLE registros_pertenencia (
    idRegistro INTEGER PRIMARY KEY AUTOINCREMENT,
    codigoPertenencia INTEGER,
    idEstado INTEGER,
    fechaHoraRegistro INTEGER,
    FOREIGN KEY (codigoPertenencia) REFERENCES pertenencias(codigoPertenencia),
    FOREIGN KEY (idEstado) REFERENCES estado_pertenencias(id)
);
```

### Índices Recomendados

```sql
-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_usuarios_usuario ON usuarios(usuario);
CREATE INDEX idx_estudiantes_codigo ON estudiantes(codigoEstudiante);
CREATE INDEX idx_pertenencias_estudiante ON pertenencias(idEstudiante);
CREATE INDEX idx_pertenencias_estado ON pertenencias(idUltimoEstado);
CREATE INDEX idx_registros_pertenencia ON registros_pertenencia(codigoPertenencia);
CREATE INDEX idx_registros_fecha ON registros_pertenencia(fechaHoraRegistro);
```

## API REST - Especificación Completa

### Autenticación

#### POST /auth/login
**Descripción**: Autenticación de usuario
**Body**:
```json
{
    "usuario": "string",
    "contraseña": "string"
}
```
**Response**:
```json
{
    "success": true,
    "token": "jwt_token_here",
    "usuario": {
        "id": 1,
        "usuario": "admin",
        "rol": "Administrador"
    }
}
```

#### POST /auth/logout
**Descripción**: Cierre de sesión
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
    "success": true,
    "message": "Sesión cerrada exitosamente"
}
```

### Estudiantes

#### POST /estudiantes/identificar
**Descripción**: Identificación por reconocimiento facial
**Headers**: `Authorization: Bearer <token>`
**Body**: `FormData` con imagen
**Response**:
```json
{
    "success": true,
    "estudiante": {
        "id": 1,
        "codigo": "2023001",
        "nombre": "Juan Pérez",
        "carrera": "Ingeniería",
        "plan": "2023"
    },
    "similitud": 95
}
```

#### POST /estudiantes/registrar
**Descripción**: Registro de nuevo estudiante
**Headers**: `Authorization: Bearer <token>`
**Body**:
```json
{
    "codigoEstudiante": "2023001",
    "nombresEstudiante": "Juan Pérez",
    "carreraEstudiante": "Ingeniería",
    "planEstudiante": "2023"
}
```

### Pertenencias

#### POST /pertenencia/nueva-pertenencia
**Descripción**: Registro de nueva pertenencia
**Headers**: `Authorization: Bearer <token>`
**Body**: `FormData` con imagen, idEstudiante, idObjeto
**Response**:
```json
{
    "success": true,
    "codigoPertenencia": 123,
    "message": "Pertenencia registrada exitosamente"
}
```

#### POST /pertenencia/registrar-ingreso-pertenencia
**Descripción**: Registro de ingreso de pertenencia existente
**Headers**: `Authorization: Bearer <token>`
**Body**: `FormData` con imagen, idEstudiante, codigoPertenencia

#### POST /pertenencia/registrar-salida-pertenencia
**Descripción**: Registro de salida de pertenencia
**Headers**: `Authorization: Bearer <token>`
**Body**: `FormData` con imagen, idEstudiante, codigoPertenencia

#### GET /pertenencia/historial
**Descripción**: Consulta de historial de pertenencias
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**:
- `idEstudiante` (opcional): Filtrar por estudiante
- `fechaInicio` (opcional): Fecha de inicio
- `fechaFin` (opcional): Fecha de fin

### Objetos

#### POST /objetos/identificar
**Descripción**: Identificación de objetos con YOLOv8
**Headers**: `Authorization: Bearer <token>`
**Body**: `FormData` con imagen
**Response**:
```json
{
    "success": true,
    "objeto": {
        "idObjeto": 1,
        "objeto": "Laptop",
        "imgUri": "data:image/jpeg;base64,...",
        "confianza": 0.95
    }
}
```

## Seguridad

### Autenticación JWT

**Configuración**:
```python
app.config['JWT_SECRET_KEY'] = 'clave_12323'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
```

**Decorador de Protección**:
```python
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
```

### Decoradores de Roles

**Implementación** (`utils/role_decorador.py`):
```python
def require_role(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verificación de rol del usuario
            pass
        return wrapper
    return decorator
```

**Uso**:
```python
@app.route('/admin-only')
@require_role('Administrador')
def admin_only():
    return jsonify(message="Acceso solo para administradores")
```

### Validación de Datos

**Sanitización de Entrada**:
- Limpieza de strings
- Validación de tipos de datos
- Escape de caracteres especiales

**Manejo de Errores**:
```python
@app.errorhandler(400)
def bad_request(error):
    return jsonify(error="Datos de entrada inválidos"), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(error="No autorizado"), 401

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Error interno del servidor"), 500
```

## Rendimiento y Optimización

### Base de Datos

**Optimizaciones Implementadas**:
- Índices en columnas de búsqueda frecuente
- Consultas preparadas para evitar SQL injection
- Transacciones para operaciones críticas
- Conexiones persistentes

**Consultas Optimizadas**:
```sql
-- Consulta con JOIN optimizado
SELECT p.*, e.nombresEstudiante, ep.estado
FROM pertenencias p
JOIN estudiantes e ON p.idEstudiante = e.idEstudiante
JOIN estado_pertenencias ep ON p.idUltimoEstado = ep.id
WHERE p.idEstudiante = ?
ORDER BY p.FechaUltimaActividad DESC;
```

### Procesamiento de Imágenes

**Optimizaciones**:
- Redimensionamiento automático de imágenes
- Compresión JPEG para almacenamiento
- Procesamiento en lotes para múltiples imágenes
- Cache de modelos de IA

**Configuración de OpenCV**:
```python
# Configuración optimizada para detección de rostros
clasificador_rostros = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
rostros_detectados = clasificador_rostros.detectMultiScale(
    imagen_gris, 
    scaleFactor=1.3, 
    minNeighbors=5,
    minSize=(30, 30)
)
```

### Frontend

**Optimizaciones JavaScript**:
- Lazy loading de imágenes
- Debouncing en eventos de entrada
- Cache de datos en localStorage
- Compresión de imágenes antes del envío

## Monitoreo y Logging

### Sistema de Logs

**Configuración de Logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('intelliguard.log'),
        logging.StreamHandler()
    ]
)
```

**Logs Importantes**:
- Autenticación de usuarios
- Operaciones de base de datos
- Errores de reconocimiento facial
- Errores de detección de objetos
- Operaciones de pertenencias

### Métricas de Rendimiento

**Métricas a Monitorear**:
- Tiempo de respuesta de API
- Precisión del reconocimiento facial
- Precisión de la detección de objetos
- Uso de memoria y CPU
- Errores de base de datos

## Mantenimiento y Actualizaciones

### Actualización de Modelos de IA

**Proceso de Reentrenamiento**:

1. **Recolección de Datos**:
   ```python
   # Captura de nuevas imágenes para entrenamiento
   def capturar_datos_entrenamiento():
       # Implementación de captura automática
   ```

2. **Preparación del Dataset**:
   ```python
   # Organización de datos para entrenamiento
   def preparar_dataset():
       # Limpieza y organización de imágenes
   ```

3. **Entrenamiento**:
   ```python
   # Entrenamiento del modelo
   def entrenar_modelo():
       # Proceso de entrenamiento
   ```

4. **Validación**:
   ```python
   # Pruebas de precisión
   def validar_modelo():
       # Evaluación del modelo
   ```

### Backup y Recuperación

**Estrategia de Backup**:
- Backup diario de base de datos
- Backup semanal de modelos de IA
- Backup de configuración del sistema
- Procedimientos de recuperación documentados

**Script de Backup**:
```bash
#!/bin/bash
# Backup automático de base de datos
sqlite3 basededatos.db ".backup backup_$(date +%Y%m%d_%H%M%S).db"
```

## Escalabilidad

### Arquitectura Escalable

**Consideraciones de Escalabilidad**:
- Separación de módulos independientes
- API REST stateless
- Base de datos optimizada
- Cache distribuido (futuro)

**Posibles Mejoras**:
- Migración a PostgreSQL para mayor concurrencia
- Implementación de Redis para cache
- Microservicios para módulos críticos
- Load balancing para múltiples instancias

### Rendimiento en Producción

**Configuraciones Recomendadas**:
- Servidor WSGI (Gunicorn)
- Proxy reverso (Nginx)
- Base de datos en servidor separado
- CDN para archivos estáticos

**Monitoreo de Producción**:
- APM (Application Performance Monitoring)
- Logs centralizados
- Alertas automáticas
- Dashboard de métricas

---

**Documentación Técnica IntelliGuard** - Versión 1.0 