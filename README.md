# 🎵 Reproductor de Música Online

Una aplicación web interactiva para buscar y escuchar música online de forma gratuita, construida con Streamlit.

## 🌟 Características

- 🔍 **Búsqueda de música**: Busca cualquier canción o artista
- 🎧 **Reproducción en línea**: Escucha música directamente desde la aplicación
- 📊 **Información detallada**: Ve la duración, vistas y canal de cada canción
- 🖼️ **Miniaturas**: Visualiza las portadas de las canciones
- 🆓 **Completamente gratis**: Usa recursos gratuitos (YouTube)
- 🚀 **Interfaz moderna**: Diseño limpio y fácil de usar

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
   streamlit run app.py
   ```

2. **Abre tu navegador** en `http://localhost:8501` (se abrirá automáticamente)

3. **Busca y reproduce música**:
   - Escribe el nombre de una canción o artista en la barra lateral
   - Ajusta el número de resultados si lo deseas
   - Haz clic en "Buscar"
   - Selecciona una canción de los resultados
   - Haz clic en "▶️ Reproducir" para escucharla

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

### Error al buscar o reproducir
- Verifica tu conexión a Internet
- Algunos videos pueden tener restricciones regionales
- Actualiza `yt-dlp` con: `pip install --upgrade yt-dlp`

### La aplicación no se inicia
- Asegúrate de tener todas las dependencias instaladas
- Verifica que estés usando Python 3.8 o superior
- Reactiva el entorno virtual si lo estás usando

### Audio no se reproduce
- Algunos navegadores pueden bloquear la reproducción automática
- Intenta con otro navegador (Chrome o Edge recomendados)
- Verifica que el volumen no esté silenciado

## 📝 Personalización

Puedes personalizar la aplicación editando `app.py`:
- Cambiar el número máximo de resultados
- Modificar el diseño y colores
- Agregar más funcionalidades (listas de reproducción, favoritos, etc.)

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
