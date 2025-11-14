# 🎵 Reproductor de Música Online

Una aplicación web interactiva para buscar y escuchar música online de forma gratuita, construida con Streamlit.

## 🌟 Características

- 🔍 **Búsqueda de música**: Busca cualquier canción o artista
- 🎧 **Reproducción en línea**: Escucha música directamente desde la aplicación
- 📜 **Listas de reproducción**: Crea y guarda múltiples listas personalizadas
- 🔁 **Reproducción continua**: Avance automático entre canciones
- 📊 **Información detallada**: Duración, vistas y canal de cada canción
- 🖼️ **Miniaturas**: Visualiza las portadas de las canciones
- 💾 **Guardado permanente**: Tus listas se guardan automáticamente
- 🆓 **Completamente gratis**: Usa recursos gratuitos de YouTube
- 🌐 **Multiplataforma**: Compatible con iOS, Android y Windows
- 🚀 **Interfaz moderna**: Diseño limpio y responsivo

## 📱 Compatibilidad

✅ **Sistemas Operativos:**
- 💻 Windows (7/8/10/11)
- 🍎 macOS (Big Sur y superiores)
- 🐧 Linux (todas las distribuciones)

✅ **Dispositivos Móviles:**
- 📱 iOS (iPhone y iPad - Safari 14+)
- 🤖 Android (Chrome, Firefox, Samsung Internet)

✅ **Navegadores Web:**
- Google Chrome / Edge (Chromium)
- Mozilla Firefox
- Safari (macOS e iOS)
- Opera
- Brave

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para la interfaz web
- **yt-dlp**: Herramienta para buscar y extraer audio de YouTube
- **Python**: Lenguaje de programación

## 📋 Requisitos

- Python 3.8 o superior
- Conexión a Internet

## 🚀 Instalación

1. **Clona o descarga este repositorio**

2. **Navega al directorio del proyecto**:
   ```powershell
   cd "c:\Users\OLMEDOJorge\Documents\Python projects\Music"
   ```

3. **Crea un entorno virtual (recomendado)**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Instala las dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```

## 🎮 Uso

1. **Ejecuta la aplicación**:
   ```powershell
   streamlit run Mymusic.py
   ```

2. **Abre tu navegador** en `http://localhost:8501` (se abrirá automáticamente)

3. **Funciones principales**:
   
   **Buscar y Reproducir:**
   - Escribe el nombre de una canción o artista en la barra lateral
   - Ajusta el número de resultados (5-50)
   - Haz clic en "Buscar"
   - Selecciona "▶️ Reproducir" para escuchar inmediatamente
   - Usa "➕ Agregar" para agregar a la lista sin interrumpir
   
   **Crear Listas de Reproducción:**
   - Expande "➕ Crear Nueva Lista" en la barra lateral
   - Escribe un nombre y haz clic en "Crear Lista"
   - Selecciona tu lista en el dropdown
   - Agrega canciones desde los resultados de búsqueda
   - Se guarda automáticamente
   
   **Gestionar Listas:**
   - Usa las pestañas para ver todas tus listas
   - Haz clic en cualquier canción para reproducirla
   - Usa "🗑️" para eliminar canciones
   - "▶️ Reproducir Todo" para iniciar desde el principio
   
   **Controles de Reproducción:**
   - ⏮️ Anterior | ⏭️ Siguiente | 🔄 Recargar | ⏹️ Detener
   - 🔁 Reproducción continua automática
   - Cola de reproducción expandible

## 📖 Cómo Funciona

La aplicación utiliza `yt-dlp` para:
1. Buscar canciones en YouTube basándose en tu consulta
2. Extraer la URL de audio directo sin descargar el archivo
3. Reproducir el audio en tiempo real a través del navegador

**Todo es gratis** porque usa recursos públicos de YouTube sin necesidad de API keys o suscripciones.

## ⚠️ Notas Importantes

- Requiere conexión a Internet para buscar y reproducir música
- La calidad del audio depende de la disponibilidad en YouTube
- Algunos videos pueden no estar disponibles debido a restricciones regionales
- El uso está sujeto a los términos de servicio de YouTube

## 🔧 Solución de Problemas

### 📱 En dispositivos móviles (iOS/Android)
- **Audio no se reproduce automáticamente**: Los navegadores móviles bloquean autoplay por seguridad
  - Solución: Haz clic en el botón ▶️ del reproductor
- **Pantalla se apaga**: El audio seguirá reproduciéndose en segundo plano
- **Usar en pantalla completa**: Agrega el sitio a tu pantalla de inicio para una experiencia tipo app

### 💻 En Windows/macOS/Linux
- **Navegador recomendado**: Chrome o Edge para mejor rendimiento
- **Audio entrecortado**: Verifica tu conexión a Internet
- **Problemas de certificado SSL**: Actualiza tu navegador a la última versión

### 🌐 Problemas generales
- **Error al buscar o reproducir**:
  - Verifica tu conexión a Internet
  - Algunos videos pueden tener restricciones regionales
  - Actualiza `yt-dlp` con: `pip install --upgrade yt-dlp`

- **La aplicación no se inicia**:
  - Asegúrate de tener todas las dependencias instaladas
  - Verifica que estés usando Python 3.8 o superior
  - Reactiva el entorno virtual si lo estás usando

- **Las listas no se guardan**:
  - Verifica permisos de escritura en el directorio
  - El archivo `playlists_data.pkl` debe poder crearse/modificarse

## 📝 Personalización

Puedes personalizar la aplicación editando `Mymusic.py`:
- Cambiar el número máximo de resultados de búsqueda
- Modificar el diseño y colores usando Streamlit themes
- Ajustar los formatos de audio preferidos para mejor compatibilidad
- Personalizar los mensajes y textos de la interfaz
- Agregar más funcionalidades (exportar listas, compartir, etc.)

## 🎯 Características Avanzadas

- **Búsqueda sin interrupción**: Busca nuevas canciones mientras la música sigue sonando
- **Múltiples listas**: Crea tantas listas como quieras, cada una con su propio nombre
- **Persistencia de datos**: Tus listas se guardan localmente en `playlists_data.pkl`
- **Formato optimizado**: Audio en formato M4A para máxima compatibilidad
- **Interfaz adaptativa**: Se adapta automáticamente a móviles y tablets
- **Control total**: Reproduce cualquier canción de cualquier lista en cualquier momento

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de:
- Reportar bugs
- Sugerir nuevas características
- Mejorar la documentación
- Enviar pull requests

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 💡 Recursos Adicionales

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [yt-dlp en GitHub](https://github.com/yt-dlp/yt-dlp)
- [Python Official](https://www.python.org/)

## 🎉 Disfruta tu música

¡Ahora estás listo para disfrutar de música gratis online! 🎶

---

**Desarrollado por Jorge Olmedo usando Streamlit y Python**
