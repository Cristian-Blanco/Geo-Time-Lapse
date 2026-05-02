
```GeoTimeLapse```

Plugin for QGIS to generate multitemporal animations
Plugin de QGIS para generación de animaciones multitemporales

## DESCRIPTION / DESCRIPCIÓN

English:
GeoTimeLapse is a QGIS plugin that allows users to generate timelapse animations from satellite imagery, integrating data acquisition, processing, and video export into a single automated workflow.

Español:
GeoTimeLapse es un plugin para QGIS que permite generar animaciones tipo timelapse a partir de imágenes satelitales, integrando descarga, procesamiento y exportación de video en un solo flujo automatizado.

## FEATURES / CARACTERÍSTICAS

English:
- Integration with Google Earth Engine  
- Area of Interest (AOI) selection  
- Time range configuration  
- Multispectral support (RGB, infrared, radar)  
- Cloud filtering  
- Normalization  
- Frame duration control  
- Templates with scale, north arrow and CRS  
- Direct video export  

Español:
- Integración con Google Earth Engine  
- Selección de área de interés (AOI)  
- Configuración de rangos temporales  
- Soporte multiespectral (RGB, infrarrojo, radar)  
- Filtro de nubosidad  
- Normalización  
- Control de duración de fotogramas  
- Plantillas con escala, norte y sistema de referencia (CRS)  
- Exportación directa a video  

## REQUIREMENTS / REQUISITOS

English:
- QGIS 3.x (LTR recommended)  
- Python (included with QGIS)  

Español:
- QGIS 3.x (recomendado LTR)  
- Python (incluido con QGIS)  

## DEPENDENCIES / DEPENDENCIAS

English:
Install in the QGIS Python environment:

pip install pillow moviepy earthengine-api 

IMPORTANT:
On Windows, use OSGeo4W Shell.

On Linux, use the terminal.

==================
Español:
Instalar en el entorno de Python de QGIS:

pip install pillow moviepy earthengine-api 

IMPORTANTE:
En Windows usar OSGeo4W Shell.

En Linux usar la terminal.

```INSTALLATION / INSTALACIÓN```

## 1. DOWNLOAD / DESCARGA

English:
- Go to the GitHub repository  
- Click "Code → Download ZIP"  
- Extract the folder  

Español:
- Ir al repositorio en GitHub  
- Clic en "Code → Download ZIP"  
- Extraer la carpeta  

## 2. COPY PLUGIN / COPIAR PLUGIN

WINDOWS:

C:\Users\YOUR_USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins

LINUX:

/home/your_user/.local/share/QGIS/QGIS3/profiles/default/python/plugins

English:
Place the folder:
GeoTimeLapse

IMPORTANT:
Avoid nested folders (GeoTimeLapse inside GeoTimeLapse)

Español:
Colocar la carpeta:
GeoTimeLapse

IMPORTANTE:
Evitar doble carpeta (GeoTimeLapse dentro de GeoTimeLapse)

## 3. INSTALL DEPENDENCIES / INSTALAR DEPENDENCIAS

WINDOWS:

English:
Open OSGeo4W Shell and run:

python -m pip install pillow
python -m pip install moviepy
python -m pip install imageio
python -m pip install imageio-ffmpeg
python -m imageio_ffmpeg.download
python -m pip install earthengine-api



Español:
Abrir OSGeo4W Shell y ejecutar:

python -m pip install pillow
python -m pip install moviepy
python -m pip install imageio
python -m pip install imageio-ffmpeg
python -m imageio_ffmpeg.download
python -m pip install earthengine-api

========================
LINUX:

English:
Open terminal and run:

pip install pillow moviepy earthengine-api imageio imageio-ffmpeg

Español:
Abrir terminal y ejecutar:

pip install pillow moviepy earthengine-api imageio imageio-ffmpeg

## 4. GOOGLE EARTH ENGINE AUTHENTICATION / AUTENTICACIÓN GEE

English:
Run:

earthengine authenticate

Follow instructions in browser.

Español:
Ejecutar:

earthengine authenticate

Seguir instrucciones en el navegador.

## 5. ACTIVATE PLUGIN / ACTIVAR PLUGIN

English:
In QGIS:
Plugins → Manage and Install Plugins → Installed

Search:
GeoTimeLapse

Enable the plugin.

Español:
En QGIS:
Plugins → Manage and Install Plugins → Installed

Buscar:
GeoTimeLapse

Activar el plugin.

```USAGE / USO```

English:
1. Open plugin
2. Select Area of Interest (AOI)
3. Define time range
4. Choose imagery type
5. Generate timelapse
6. Export video

Español:
1. Abrir el plugin
2. Seleccionar área de interés
3. Definir rango temporal
4. Elegir tipo de imagen
5. Generar timelapse
6. Exportar video

```COMMON ISSUES / PROBLEMAS COMUNES```

English:
Plugin not visible:
- Check folder location
- Avoid nested folders

Error "No module named":
- Install dependencies

Earth Engine error:
- Run earthengine authenticate

Video not generated:
- Check moviepy and imageio-ffmpeg

Español:
El plugin no aparece:
- Verificar ubicación
- Evitar carpetas duplicadas

Error "No module named":
- Instalar dependencias

Error con Earth Engine:
- Ejecutar earthengine authenticate

No se genera el video:
- Verificar moviepy e imageio-ffmpeg

```TECHNOLOGIES / TECNOLOGÍAS```

- Python
- PyQt
- QGIS API
- Google Earth Engine
- MoviePy

```AUTHORS / AUTORES```

Cristian Javier Martinez Blanco  
Ingeniero de Sistemas  

Ana Fernanda Herrera  
Ingeniera Geóloga  

Proyecto desarrollado como trabajo de grado.
Especialización en Sistemas de Información Geográfica (en curso)  



```AI DISCLOSURE / DECLARACIÓN DE USO DE IA```

EN:
This project includes content supported by artificial intelligence tools (ChatGPT, OpenAI),
used exclusively for documentation writing, structuring, and language translation.
All technical development and validation were performed by the authors.

ES:
Este proyecto incluye contenido apoyado por herramientas de inteligencia artificial (ChatGPT, OpenAI),
utilizadas exclusivamente para la redacción, estructuración y traducción de la documentación. 
Todo el desarrollo técnico y validación fue realizado por los autores.

