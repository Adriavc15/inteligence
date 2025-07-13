# Guía de Instalación y Configuración - IntelliGuard

## Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 o superior
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Almacenamiento**: 10 GB de espacio libre
- **Cámara Web**: Para reconocimiento facial y detección de objetos
- **Navegador**: Chrome 90+, Firefox 88+, Safari 14+

### Requisitos Recomendados
- **RAM**: 16 GB
- **Almacenamiento**: SSD de 50 GB
- **GPU**: NVIDIA con CUDA para aceleración de IA (opcional)
- **Red**: Conexión estable a internet para descarga de dependencias

## Instalación Paso a Paso

### 1. Preparación del Entorno

#### Instalar Python
1. **Descargar Python** desde [python.org](https://www.python.org/downloads/)
2. **Verificar instalación**:
   ```bash
   python --version
   pip --version
   ```

#### Crear Entorno Virtual (Recomendado)
```bash
# Crear directorio del proyecto
mkdir IntelliGuard
cd IntelliGuard

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Clonación del Repositorio

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO] IntelliGuard-main
cd IntelliGuard-main
```

### 3. Instalación de Dependencias

#### Dependencias del Sistema (Ubuntu/Debian)
```bash
# Actualizar paquetes
sudo apt update

# Instalar dependencias del sistema
sudo apt install -y python3-dev python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libgl1-mesa-glx libglib2.0-0
sudo apt install -y libsm6 libxext6 libxrender-dev
sudo apt install -y libgomp1 libgthread-2.0-0
```

#### Dependencias del Sistema (Windows)
1. **Instalar Visual Studio Build Tools** (para compilación de OpenCV)
2. **Descargar OpenCV** desde [opencv.org](https://opencv.org/releases/)

#### Dependencias de Python
```bash
# Navegar al módulo principal
cd "Intelliguard - Registro de Pertenencias/Backend"

# Instalar dependencias
pip install -r requirements.txt
```

**Contenido típico de requirements.txt**:
```
Flask==2.3.3
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.3
opencv-python==4.8.1.78
ultralytics==8.0.196
numpy==1.24.3
Pillow==10.0.1
Werkzeug==2.3.7
```

### 4. Configuración de la Base de Datos

#### Inicialización Automática
La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

#### Configuración Manual (Opcional)
```bash
# Navegar al directorio del backend
cd "Intelliguard - Registro de Pertenencias/Backend"

# Ejecutar script de inicialización
python -c "
from models.usuario import BaseDatosUsuarios
from models.estudiante import BaseDatosEstudiantes
from models.pertenencia import BaseDatosPertenencia

# Crear instancias para inicializar tablas
db_usuarios = BaseDatosUsuarios('basededatos.db')
db_estudiantes = BaseDatosEstudiantes('basededatos.db')
db_pertenencias = BaseDatosPertenencia('basededatos.db')

print('Base de datos inicializada correctamente')
"
```

### 5. Configuración de Modelos de IA

#### Descarga de Modelos Pre-entrenados
```bash
# Crear directorio para modelos
mkdir -p "Intelliguard - Registro de Pertenencias/Backend/models"

# Descargar modelo YOLOv8 (si no está incluido)
# El modelo debe estar en: models/ModelObjetoFinal.pt
```

#### Configuración de OpenCV
```bash
# Verificar instalación de OpenCV
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

### 6. Configuración del Frontend

#### Configurar URL del Backend
Editar `utils/config.js` en cada módulo:
```javascript
// Cambiar según tu configuración
const API_URL = 'http://localhost:5000';
```

#### Configurar CORS (si es necesario)
En el backend, verificar configuración CORS:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
```

### 7. Configuración de Variables de Entorno

#### Crear archivo .env
```bash
# Crear archivo .env en el directorio del backend
touch "Intelliguard - Registro de Pertenencias/Backend/.env"
```

#### Contenido del archivo .env
```env
# Configuración de JWT
JWT_SECRET_KEY=tu_clave_secreta_muy_segura_aqui

# Configuración de la base de datos
DATABASE_URL=sqlite:///basededatos.db

# Configuración del servidor
FLASK_ENV=development
FLASK_DEBUG=True

# Configuración de IA
OPENCV_CASCADE_PATH=/usr/share/opencv4/haarcascades/
YOLO_MODEL_PATH=models/ModelObjetoFinal.pt
```

### 8. Configuración de Permisos

#### Permisos de Cámara (Linux)
```bash
# Agregar usuario al grupo video
sudo usermod -a -G video $USER

# Verificar permisos
ls -l /dev/video*
```

#### Permisos de Archivos
```bash
# Dar permisos de ejecución a scripts
chmod +x scripts/*.sh

# Dar permisos de escritura a directorios de datos
chmod 755 uploads/
chmod 755 models/
```

## Verificación de la Instalación

### 1. Prueba del Backend

#### Ejecutar Servidor de Desarrollo
```bash
# Navegar al módulo principal
cd "Intelliguard - Registro de Pertenencias/Backend"

# Ejecutar aplicación
python app.py
```

#### Verificar Endpoints
```bash
# Probar endpoint básico
curl http://localhost:5000/

# Respuesta esperada: "Hola mundo"
```

### 2. Prueba del Frontend

#### Abrir en Navegador
1. Navegar a `Intelliguard - Login Administrador/Frontend/`
2. Abrir `index.html` en el navegador
3. Verificar que la página carga correctamente

### 3. Prueba de Reconocimiento Facial

#### Verificar OpenCV
```python
import cv2
import numpy as np

# Probar detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print("OpenCV configurado correctamente")
```

### 4. Prueba de Detección de Objetos

#### Verificar YOLOv8
```python
from ultralytics import YOLO

# Cargar modelo (si existe)
try:
    model = YOLO('models/ModelObjetoFinal.pt')
    print("Modelo YOLOv8 cargado correctamente")
except:
    print("Modelo YOLOv8 no encontrado - se requiere entrenamiento")
```

## Configuración de Producción

### 1. Configuración del Servidor

#### Usar Gunicorn (Recomendado)
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Configuración de Nginx
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/IntelliGuard/Frontend;
    }
}
```

### 2. Configuración de Base de Datos en Producción

#### Migración a PostgreSQL (Opcional)
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb intelliguard

# Instalar dependencias Python
pip install psycopg2-binary
```

### 3. Configuración de Seguridad

#### Configurar HTTPS
```bash
# Obtener certificado SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

#### Configurar Firewall
```bash
# Configurar UFW
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Solución de Problemas

### Problemas Comunes

#### 1. Error de Importación de OpenCV
```bash
# Solución: Reinstalar OpenCV
pip uninstall opencv-python
pip install opencv-python-headless
```

#### 2. Error de Permisos de Cámara
```bash
# Verificar dispositivos de video
ls -l /dev/video*

# Agregar usuario al grupo video
sudo usermod -a -G video $USER
```

#### 3. Error de Conexión a Base de Datos
```bash
# Verificar permisos del archivo de base de datos
ls -l basededatos.db

# Recrear base de datos si es necesario
rm basededatos.db
python app.py
```

#### 4. Error de CORS
```python
# En app.py, verificar configuración CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'])  # Solo para desarrollo
```

#### 5. Error de Modelo YOLOv8
```bash
# Verificar que el modelo existe
ls -l models/ModelObjetoFinal.pt

# Si no existe, entrenar modelo o descargar
python -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.save('models/ModelObjetoFinal.pt')
"
```

### Logs y Debugging

#### Habilitar Logs Detallados
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Verificar Logs del Sistema
```bash
# Ver logs de la aplicación
tail -f intelliguard.log

# Ver logs del sistema
journalctl -u intelliguard -f
```

## Mantenimiento

### Actualizaciones Regulares

#### Actualizar Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Actualizar dependencias
pip install --upgrade -r requirements.txt
```

#### Backup de Base de Datos
```bash
# Crear script de backup
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp basededatos.db backup_${DATE}.db
echo "Backup creado: backup_${DATE}.db"
EOF

chmod +x backup.sh
```

#### Limpieza de Archivos Temporales
```bash
# Limpiar archivos temporales
find . -name "*.tmp" -delete
find . -name "*.log" -mtime +7 -delete
```

### Monitoreo

#### Script de Monitoreo
```bash
cat > monitor.sh << 'EOF'
#!/bin/bash
# Verificar si la aplicación está ejecutándose
if pgrep -f "python app.py" > /dev/null; then
    echo "Aplicación ejecutándose correctamente"
else
    echo "Aplicación no está ejecutándose"
    # Reiniciar aplicación
    cd /path/to/IntelliGuard/Backend
    nohup python app.py > app.log 2>&1 &
fi
EOF

chmod +x monitor.sh
```

## Contacto y Soporte

### Información de Contacto
- **Email**: soporte@intelliguard.com
- **Documentación**: [URL_DOCUMENTACION]
- **Repositorio**: [URL_REPOSITORIO]

### Recursos Adicionales
- **Wiki del Proyecto**: [URL_WIKI]
- **FAQ**: [URL_FAQ]
- **Comunidad**: [URL_COMUNIDAD]

---

**Guía de Instalación IntelliGuard** - Versión 1.0 