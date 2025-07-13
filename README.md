# IntelliGuard - Sistema de Gestión de Pertenencias Estudiantiles

## Descripción General

IntelliGuard es un sistema integral de gestión de pertenencias estudiantiles que utiliza tecnologías de inteligencia artificial para el reconocimiento facial de estudiantes y la detección automática de objetos. El sistema está diseñado para instituciones educativas que requieren un control eficiente y automatizado de las pertenencias que ingresan y salen de sus instalaciones.

## Arquitectura del Sistema

El proyecto está organizado en múltiples módulos independientes, cada uno con su propio backend y frontend:

### Módulos del Sistema

1. **Login Administrador** - Autenticación para administradores del sistema
2. **Login Personal** - Autenticación para personal operativo
3. **Gestión de Personal** - Administración de usuarios del sistema
4. **Identificar Ingresante** - Reconocimiento facial de estudiantes
5. **Registro de Pertenencias** - Registro de objetos con detección automática
6. **Salida de Pertenencias** - Control de salida de objetos
7. **Historial de Pertenencias** - Consulta de registros históricos
8. **Reportes** - Generación de reportes y estadísticas

## Tecnologías Utilizadas

### Backend
- **Flask** - Framework web para Python
- **SQLite** - Base de datos relacional
- **OpenCV** - Procesamiento de imágenes y visión por computadora
- **YOLOv8** - Detección de objetos con inteligencia artificial
- **JWT** - Autenticación basada en tokens
- **Flask-CORS** - Manejo de solicitudes cross-origin

### Frontend
- **HTML5** - Estructura de páginas web
- **CSS3** - Estilos y diseño responsivo
- **JavaScript** - Lógica del lado del cliente
- **Bootstrap 5** - Framework CSS para diseño responsivo
- **Alpine.js** - Framework JavaScript ligero

### Inteligencia Artificial
- **Reconocimiento Facial** - Basado en FisherFace con OpenCV
- **Detección de Objetos** - Modelo YOLOv8 personalizado
- **Comparación de Imágenes** - Algoritmos de similitud visual

## Estructura de Base de Datos

### Tablas Principales

#### Usuarios
```sql
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    hash_contraseña TEXT NOT NULL,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
);
```

#### Estudiantes
```sql
CREATE TABLE estudiantes (
    idEstudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    codigoEstudiante TEXT NOT NULL,
    nombresEstudiante TEXT NOT NULL,
    carreraEstudiante TEXT NOT NULL,
    planEstudiante TEXT NOT NULL
);
```

#### Pertenencias
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

#### Registros de Pertenencia
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

## Funcionalidades Principales

### 1. Reconocimiento Facial
- **Captura de Rostros**: Sistema automático de captura de imágenes faciales
- **Entrenamiento de Modelos**: Generación de modelos de reconocimiento personalizados
- **Identificación en Tiempo Real**: Reconocimiento instantáneo de estudiantes registrados

### 2. Detección de Objetos
- **Modelo YOLOv8**: Detección automática de tipos de objetos
- **Clasificación Inteligente**: Identificación de categorías de pertenencias
- **Extracción de Imágenes**: Recorte automático de objetos detectados

### 3. Gestión de Pertenencias
- **Registro de Entrada**: Asociación de objetos con estudiantes
- **Control de Salida**: Verificación de pertenencias al salir
- **Estados de Objetos**: Seguimiento del estado actual de cada pertenencia
- **Historial Completo**: Registro de todas las actividades

### 4. Sistema de Autenticación
- **Roles de Usuario**: Administradores y personal operativo
- **JWT Tokens**: Autenticación segura y persistente
- **Control de Acceso**: Restricciones basadas en roles

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### Instalación del Backend

1. **Clonar el repositorio**:
```bash
git clone [URL_DEL_REPOSITORIO]
cd IntelliGuard-main
```

2. **Instalar dependencias**:
```bash
cd "Intelliguard - [MODULO]/Backend"
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
```bash
# Crear archivo .env si es necesario
JWT_SECRET_KEY=tu_clave_secreta_aqui
```

4. **Ejecutar la aplicación**:
```bash
python app.py
```

### Configuración del Frontend

1. **Navegar al directorio del frontend**:
```bash
cd "Intelliguard - [MODULO]/Frontend"
```

2. **Configurar la URL del backend**:
Editar `utils/config.js`:
```javascript
const API_URL = 'http://localhost:5000';
```

3. **Abrir en el navegador**:
```bash
# Abrir index.html en el navegador
```

## Uso del Sistema

### Flujo de Registro de Pertenencias

1. **Identificación del Estudiante**:
   - El sistema captura una imagen del rostro del estudiante
   - Se realiza reconocimiento facial contra la base de datos
   - Se confirma la identidad del estudiante

2. **Detección del Objeto**:
   - Se captura una imagen del objeto a registrar
   - El modelo YOLOv8 identifica el tipo de objeto
   - Se extrae y procesa la imagen del objeto

3. **Registro de Pertenencia**:
   - Se asocia el objeto con el estudiante identificado
   - Se establece el estado inicial (entrada)
   - Se registra la fecha y hora del evento

### Flujo de Salida de Pertenencias

1. **Verificación de Identidad**:
   - Reconocimiento facial del estudiante
   - Consulta de pertenencias registradas

2. **Confirmación de Salida**:
   - Verificación de que el objeto pertenece al estudiante
   - Actualización del estado a "salida"
   - Registro del evento en el historial

## Modelos de Inteligencia Artificial

### Reconocimiento Facial
- **Algoritmo**: FisherFace (OpenCV)
- **Precisión**: Configurable (umbral de similitud)
- **Entrenamiento**: Automático con imágenes capturadas
- **Formato de Imágenes**: 150x150 píxeles en escala de grises

### Detección de Objetos
- **Modelo**: YOLOv8 personalizado
- **Confianza**: 80% (configurable)
- **Entrenamiento**: Dataset personalizado de objetos
- **Categorías**: Definidas según necesidades institucionales

## API REST

### Endpoints Principales

#### Autenticación
- `POST /auth/login` - Inicio de sesión
- `POST /auth/logout` - Cierre de sesión

#### Estudiantes
- `GET /estudiantes/identificar` - Identificación por reconocimiento facial
- `POST /estudiantes/registrar` - Registro de nuevo estudiante
- `GET /estudiantes/{id}` - Consulta de estudiante específico

#### Pertenencias
- `POST /pertenencia/nueva-pertenencia` - Registro de nueva pertenencia
- `POST /pertenencia/registrar-ingreso-pertenencia` - Registro de ingreso
- `POST /pertenencia/registrar-salida-pertenencia` - Registro de salida
- `GET /pertenencia/historial` - Consulta de historial

#### Objetos
- `POST /objetos/identificar` - Identificación de objetos
- `GET /objetos/tipos` - Lista de tipos de objetos

## Seguridad

### Autenticación y Autorización
- **JWT Tokens**: Autenticación stateless
- **Roles de Usuario**: Control de acceso granular
- **Decoradores de Roles**: Protección de endpoints

### Validación de Datos
- **Sanitización**: Limpieza de datos de entrada
- **Validación**: Verificación de tipos y formatos
- **Manejo de Errores**: Respuestas de error estructuradas

## Mantenimiento

### Base de Datos
- **Backups Regulares**: Respaldo automático de datos
- **Optimización**: Índices para consultas frecuentes
- **Integridad**: Restricciones de clave foránea

### Modelos de IA
- **Reentrenamiento**: Actualización periódica de modelos
- **Validación**: Pruebas de precisión y rendimiento
- **Versionado**: Control de versiones de modelos

## Troubleshooting

### Problemas Comunes

1. **Error de Reconocimiento Facial**:
   - Verificar iluminación adecuada
   - Asegurar que el rostro esté completamente visible
   - Comprobar que el estudiante esté registrado

2. **Error de Detección de Objetos**:
   - Verificar que el objeto esté bien iluminado
   - Asegurar que el objeto esté completamente visible
   - Comprobar que el tipo de objeto esté en el modelo

3. **Errores de Conexión**:
   - Verificar que el backend esté ejecutándose
   - Comprobar la configuración de CORS
   - Validar la URL del API en config.js

## Contribución

### Guías de Desarrollo
- Seguir las convenciones de nomenclatura establecidas
- Documentar nuevas funcionalidades
- Realizar pruebas antes de commits
- Mantener la compatibilidad con módulos existentes

### Estructura de Commits
```
feat: nueva funcionalidad
fix: corrección de errores
docs: actualización de documentación
refactor: refactorización de código
test: adición de pruebas
```

## Licencia

Este proyecto está bajo la licencia [ESPECIFICAR_LICENCIA]. Todos los derechos reservados.

## Contacto

Para soporte técnico o consultas sobre el sistema:
- Email: [EMAIL_CONTACTO]
- Documentación: [URL_DOCUMENTACION]
- Repositorio: [URL_REPOSITORIO]

---

**IntelliGuard** - Sistema Inteligente de Gestión de Pertenencias Estudiantiles 
