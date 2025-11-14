import streamlit as st
import yt_dlp
from io import BytesIO
import requests
import json
import time
import pickle
import os
import base64

# Configuración de la página
st.set_page_config(
    page_title="Reproductor de Música Online",
    page_icon="🎵",
    layout="wide"
)

# Archivo para guardar las listas de reproducción
PLAYLISTS_FILE = "playlists_data.pkl"

def load_playlists():
    """Carga las listas de reproducción guardadas"""
    if os.path.exists(PLAYLISTS_FILE):
        try:
            with open(PLAYLISTS_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    return {}

def save_playlists(playlists_dict):
    """Guarda las listas de reproducción"""
    try:
        with open(PLAYLISTS_FILE, 'wb') as f:
            pickle.dump(playlists_dict, f)
        return True
    except:
        return False

# Inicializar session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'current_audio_url' not in st.session_state:
    st.session_state.current_audio_url = None
if 'current_title' not in st.session_state:
    st.session_state.current_title = None
if 'playlist' not in st.session_state:
    st.session_state.playlist = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'autoplay' not in st.session_state:
    st.session_state.autoplay = True
if 'song_duration' not in st.session_state:
    st.session_state.song_duration = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'saved_playlists' not in st.session_state:
    st.session_state.saved_playlists = load_playlists()
if 'current_playlist_name' not in st.session_state:
    st.session_state.current_playlist_name = "Lista Temporal"

def search_music(query, max_results=10):
    """Busca música en YouTube usando yt-dlp"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch' + str(max_results),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            
            if 'entries' in results:
                videos = []
                for entry in results['entries']:
                    if entry:
                        video_info = {
                            'title': entry.get('title', 'Sin título'),
                            'url': entry.get('url', ''),
                            'id': entry.get('id', ''),
                            'duration': entry.get('duration', 0),
                            'thumbnail': entry.get('thumbnail', ''),
                            'uploader': entry.get('uploader', 'Desconocido'),
                            'view_count': entry.get('view_count', 0)
                        }
                        videos.append(video_info)
                return videos
    except Exception as e:
        st.error(f"Error al buscar música: {str(e)}")
        return []

def get_audio_url(video_id):
    """Obtiene la URL de audio directa del video - Compatible con todas las plataformas"""
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',  # Priorizar m4a para mejor compatibilidad
            'quiet': True,
            'no_warnings': True,
            'prefer_ffmpeg': False,
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            
            # Buscar el mejor formato de audio compatible con móviles
            if 'formats' in info:
                # Priorizar formatos m4a y webm que son universalmente compatibles
                audio_formats = [
                    f for f in info['formats'] 
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none'
                ]
                
                if audio_formats:
                    # Ordenar: primero m4a, luego por calidad de audio
                    audio_formats.sort(
                        key=lambda x: (
                            1 if x.get('ext') == 'm4a' else 0,
                            x.get('abr', 0)
                        ), 
                        reverse=True
                    )
                    return audio_formats[0]['url']
            
            # Si no hay formato solo de audio, usar el URL directo
            return info.get('url', '')
    except Exception as e:
        st.error(f"Error al obtener audio: {str(e)}")
        return None

def format_duration(seconds):
    """Formatea la duración en minutos:segundos"""
    if seconds:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
    return "N/A"

def format_views(views):
    """Formatea el número de vistas"""
    if views:
        if views >= 1_000_000:
            return f"{views/1_000_000:.1f}M vistas"
        elif views >= 1_000:
            return f"{views/1_000:.1f}K vistas"
        else:
            return f"{views} vistas"
    return "N/A"

def play_next():
    """Reproduce la siguiente canción en la lista"""
    if st.session_state.playlist and len(st.session_state.playlist) > 0:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.playlist)
        current_song = st.session_state.playlist[st.session_state.current_index]
        audio_url = get_audio_url(current_song['id'])
        if audio_url:
            st.session_state.current_audio_url = audio_url
            st.session_state.current_title = current_song['title']
            st.session_state.song_duration = current_song.get('duration', 0)

def play_previous():
    """Reproduce la canción anterior en la lista"""
    if st.session_state.playlist and len(st.session_state.playlist) > 0:
        st.session_state.current_index = (st.session_state.current_index - 1) % len(st.session_state.playlist)
        current_song = st.session_state.playlist[st.session_state.current_index]
        audio_url = get_audio_url(current_song['id'])
        if audio_url:
            st.session_state.current_audio_url = audio_url
            st.session_state.current_title = current_song['title']
            st.session_state.song_duration = current_song.get('duration', 0)

def add_to_playlist(song):
    """Agrega una canción a la lista de reproducción"""
    if song not in st.session_state.playlist:
        st.session_state.playlist.append(song)
        # Auto-guardar si es una lista guardada
        if st.session_state.current_playlist_name != "Lista Temporal":
            st.session_state.saved_playlists[st.session_state.current_playlist_name] = st.session_state.playlist
            save_playlists(st.session_state.saved_playlists)
        return True
    return False

def create_audio_player_with_autoplay(audio_url, autoplay_enabled=True):
    """Crea un reproductor de audio compatible con iOS Safari"""
    # Usar el reproductor nativo de Streamlit que es compatible con iOS
    # En lugar del componente HTML personalizado
    pass  # Esta función ya no se usa, se reemplaza por st.audio directo

def download_mp3(video_id, title):
    """Descarga el audio en mp3 y lo retorna como bytes"""
    try:
        backend_url = "https://music-ds9z.onrender.com/download"
        params = {"video_id": video_id}
        response = requests.get(backend_url, params=params)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error del backend: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error al descargar mp3 desde backend: {str(e)}")
        return None

# Título de la aplicación
st.title("🎵 Buscador y Reproductor de Música")

# Indicador de reproducción activa
if st.session_state.current_audio_url:
    st.success(f"🔊 **Reproduciendo:** {st.session_state.current_title[:60]}... | Lista: {st.session_state.current_playlist_name}")

# Selector rápido de listas en la parte superior
if st.session_state.saved_playlists:
    col_quick1, col_quick2 = st.columns([3, 1])
    with col_quick1:
        playlist_options = ["Lista Temporal"] + list(st.session_state.saved_playlists.keys())
        quick_select = st.selectbox(
            "🎼 Acceso Rápido a Listas:",
            playlist_options,
            index=playlist_options.index(st.session_state.current_playlist_name) if st.session_state.current_playlist_name in playlist_options else 0,
            key="quick_playlist_selector"
        )
        
        if quick_select != st.session_state.current_playlist_name:
            st.session_state.current_playlist_name = quick_select
            if quick_select != "Lista Temporal":
                st.session_state.playlist = st.session_state.saved_playlists.get(quick_select, []).copy()
            st.session_state.current_index = 0
            st.rerun()
    
    with col_quick2:
        if st.session_state.current_playlist_name != "Lista Temporal" and st.session_state.playlist:
            if st.button("▶️ Reproducir Primera", use_container_width=True):
                st.session_state.current_index = 0
                song = st.session_state.playlist[0]
                audio_url = get_audio_url(song['id'])
                if audio_url:
                    st.session_state.current_audio_url = audio_url
                    st.session_state.current_title = song['title']
                    st.session_state.song_duration = song.get('duration', 0)
                    st.session_state.start_time = None
                    st.rerun()

st.markdown("---")

# Sidebar para búsqueda
with st.sidebar:
    st.header("🔍 Buscar Música")
    search_query = st.text_input("Ingresa el nombre de la canción o artista:", "")
    num_results = st.slider("Número de resultados:", 5, 50, 50)
    
    if st.button("Buscar", type="primary", use_container_width=True):
        if search_query:
            with st.spinner("Buscando música..."):
                st.session_state.search_results = search_music(search_query, num_results)
            if st.session_state.search_results:
                st.success(f"✅ {len(st.session_state.search_results)} resultados encontrados")
                # NO hacer rerun para no interrumpir la reproducción
            else:
                st.warning("No se encontraron resultados")
        else:
            st.warning("Por favor ingresa un término de búsqueda")
    
    # Botón para limpiar resultados de búsqueda
    if st.session_state.search_results:
        if st.button("🗑️ Limpiar Búsqueda", use_container_width=True):
            st.session_state.search_results = []
            st.rerun()
    
    st.markdown("---")
    
    # Gestión de listas de reproducción
    st.header("📚 Mis Listas de Reproducción")
    
    # Crear nueva lista
    with st.expander("➕ Crear Nueva Lista"):
        new_playlist_name = st.text_input("Nombre de la lista:", key="new_playlist_input")
        if st.button("Crear Lista", use_container_width=True):
            if new_playlist_name and new_playlist_name not in st.session_state.saved_playlists:
                st.session_state.saved_playlists[new_playlist_name] = []
                save_playlists(st.session_state.saved_playlists)
                st.success(f"✅ Lista '{new_playlist_name}' creada")
                st.rerun()
            elif new_playlist_name in st.session_state.saved_playlists:
                st.error("Ya existe una lista con ese nombre")
            else:
                st.warning("Ingresa un nombre para la lista")
    
    # Seleccionar lista activa
    playlist_names = ["Lista Temporal"] + list(st.session_state.saved_playlists.keys())
    selected_playlist = st.selectbox(
        "Lista Activa:",
        playlist_names,
        index=playlist_names.index(st.session_state.current_playlist_name) if st.session_state.current_playlist_name in playlist_names else 0,
        key="playlist_selector"
    )
    
    # Cambiar de lista
    if selected_playlist != st.session_state.current_playlist_name:
        st.session_state.current_playlist_name = selected_playlist
        if selected_playlist == "Lista Temporal":
            # Mantener la lista temporal actual
            pass
        else:
            # Cargar la lista guardada
            st.session_state.playlist = st.session_state.saved_playlists.get(selected_playlist, [])
            st.session_state.current_index = 0
            st.session_state.current_audio_url = None
            st.session_state.current_title = None
            st.session_state.start_time = None
        st.rerun()
    
    # Guardar lista actual
    if st.session_state.current_playlist_name != "Lista Temporal":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar", use_container_width=True):
                st.session_state.saved_playlists[st.session_state.current_playlist_name] = st.session_state.playlist
                save_playlists(st.session_state.saved_playlists)
                st.success("✅ Guardada")
        with col2:
            if st.button("🗑️ Borrar Lista", use_container_width=True):
                if st.session_state.current_playlist_name in st.session_state.saved_playlists:
                    del st.session_state.saved_playlists[st.session_state.current_playlist_name]
                    save_playlists(st.session_state.saved_playlists)
                    st.session_state.current_playlist_name = "Lista Temporal"
                    st.session_state.playlist = []
                    st.success("✅ Lista eliminada")
                    st.rerun()
    
    st.markdown("---")
    
    # Controles de reproducción
    st.header("🎮 Controles")
    st.session_state.autoplay = st.checkbox("🔁 Reproducción continua", value=st.session_state.autoplay)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏮️ Anterior", use_container_width=True, disabled=len(st.session_state.playlist) == 0):
            st.session_state.start_time = None
            play_previous()
            st.rerun()
    with col2:
        if st.button("⏭️ Siguiente", use_container_width=True, disabled=len(st.session_state.playlist) == 0):
            st.session_state.start_time = None
            play_next()
            st.rerun()
    
    if st.button("🗑️ Limpiar lista", use_container_width=True, disabled=len(st.session_state.playlist) == 0):
        st.session_state.playlist = []
        st.session_state.current_index = 0
        st.session_state.current_audio_url = None
        st.session_state.current_title = None
        # Si es una lista guardada, también limpiarla allí
        if st.session_state.current_playlist_name != "Lista Temporal":
            st.session_state.saved_playlists[st.session_state.current_playlist_name] = []
            save_playlists(st.session_state.saved_playlists)
        st.rerun()
    
    # Mostrar lista de reproducción
    if st.session_state.playlist:
        st.markdown("---")
        st.header(f"📜 {st.session_state.current_playlist_name} ({len(st.session_state.playlist)})")
        for idx, song in enumerate(st.session_state.playlist):
            icon = "🔊" if idx == st.session_state.current_index else "🎵"
            st.caption(f"{icon} {idx + 1}. {song['title'][:40]}...")
    
    st.markdown("---")
    st.markdown("""
    ### 📌 Instrucciones
    1. **Crear Lista**: Usa "➕ Crear Nueva Lista"
    2. **Seleccionar**: Elige la lista activa
    3. **Agregar Canciones**: Busca y agrega sin parar
    4. **Guardar**: Automático al agregar
    5. **Reproducir**: Disfruta tu música 🎶
    
    ### ℹ️ Información
    - ✅ Busca mientras reproduce
    - ✅ Agrega canciones sin pausar
    - ✅ Listas guardadas permanentemente
    - ✅ Fuente: YouTube (gratis)
    """)

# Área principal - Reproductor actual
if st.session_state.current_audio_url and st.session_state.current_title:
    # Iniciar temporizador si no existe
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    
    # Calcular tiempo transcurrido
    elapsed_time = time.time() - st.session_state.start_time
    
    # Si está activado el autoplay y hay más canciones en la lista
    if st.session_state.autoplay and len(st.session_state.playlist) > 1:
        # Si la canción ha terminado (con 5 segundos de margen)
        if st.session_state.song_duration > 0 and elapsed_time >= (st.session_state.song_duration + 5):
            # Avanzar a la siguiente canción
            st.session_state.start_time = None
            play_next()
            st.rerun()
    
    st.header("🎧 Reproduciendo Ahora")
    
    # Mostrar nombre de la lista actual
    col_info1, col_info2, col_info3 = st.columns([2, 2, 1])
    with col_info1:
        st.subheader(st.session_state.current_title)
    with col_info2:
        st.caption(f"📁 Lista: **{st.session_state.current_playlist_name}**")
    with col_info3:
        if st.session_state.playlist:
            st.info(f"🎵 {st.session_state.current_index + 1}/{len(st.session_state.playlist)}")
    
    # Usar reproductor nativo de Streamlit (compatible con iOS, Android y Windows)
    st.audio(st.session_state.current_audio_url, format='audio/mp4', start_time=0)
    
    # Información de compatibilidad multiplataforma
    st.caption("✅ **Compatible con**: 💻 Windows | 🍎 iOS/macOS | 🤖 Android | 🌐 Todos los navegadores")
    
    # Información sobre autoplay y controles
    if st.session_state.autoplay and len(st.session_state.playlist) > 1:
        if st.session_state.song_duration > 0:
            time_remaining = max(0, st.session_state.song_duration - elapsed_time)
            st.success(f"🔁 **Reproducción automática activa** - Siguiente canción en: {format_duration(int(time_remaining))}")
        else:
            st.info("🔁 **Reproducción continua activada**: Usa los botones ⏭️ **Siguiente** para cambiar de canción")
        
        # Mostrar duración total
        if st.session_state.song_duration > 0:
            st.caption(f"⏱️ Duración total: {format_duration(st.session_state.song_duration)}")
    
    # Controles rápidos principales
    st.markdown("### 🎮 Controles de Reproducción")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⏮️ Anterior", key="main_prev", disabled=len(st.session_state.playlist) <= 1, use_container_width=True):
            st.session_state.start_time = None
            play_previous()
            st.rerun()
    with col2:
        if st.button("⏭️ Siguiente", key="main_next", disabled=len(st.session_state.playlist) <= 1, use_container_width=True):
            st.session_state.start_time = None
            play_next()
            st.rerun()
    with col3:
        if st.button("🔄 Recargar Audio", key="reload", use_container_width=True):
            st.session_state.start_time = time.time()
            st.rerun()
    with col4:
        if st.button("⏹️ Detener", key="stop", use_container_width=True):
            st.session_state.current_audio_url = None
            st.session_state.current_title = None
            st.session_state.start_time = None
            st.rerun()
    
        # Botón de descarga de la canción actual en mp3
        if st.session_state.current_audio_url and st.session_state.current_title:
            st.markdown("---")
            st.subheader("Descargar esta canción en MP3")
            if st.button("⬇️ Descargar MP3", key="download_mp3_btn"):
                with st.spinner("Solicitando mp3 al servidor..."):
                    mp3_bytes = download_mp3(
                        st.session_state.playlist[st.session_state.current_index]['id'],
                        st.session_state.current_title.replace(' ', '_')[:40]
                    )
                    if mp3_bytes:
                        st.download_button(
                            label="Descargar archivo MP3",
                            data=mp3_bytes,
                            file_name=f"{st.session_state.current_title[:40]}.mp3",
                            mime="audio/mpeg"
                        )
    
    # Mostrar cola de reproducción actual
    if st.session_state.playlist and len(st.session_state.playlist) > 0:
        with st.expander(f"📜 Cola Actual - {st.session_state.current_playlist_name} ({len(st.session_state.playlist)} canciones)", expanded=False):
            for idx, song in enumerate(st.session_state.playlist):
                is_current = idx == st.session_state.current_index
                
                col_a, col_b, col_c = st.columns([0.5, 3, 1])
                with col_a:
                    icon = "🔊" if is_current else f"{idx + 1}."
                    st.markdown(f"**{icon}**")
                with col_b:
                    st.markdown(f"{'**' if is_current else ''}{song['title']}{'**' if is_current else ''}")
                    st.caption(f"⏱️ {format_duration(song.get('duration', 0))}")
                with col_c:
                    if not is_current:
                        if st.button("▶️", key=f"play_from_queue_{idx}", use_container_width=True):
                            st.session_state.current_index = idx
                            st.session_state.start_time = None
                            audio_url = get_audio_url(song['id'])
                            if audio_url:
                                st.session_state.current_audio_url = audio_url
                                st.session_state.current_title = song['title']
                                st.session_state.song_duration = song.get('duration', 0)
                                st.rerun()
                    else:
                        st.markdown("**▶️**")
    
    # Auto-refresh para actualizar el contador y cambiar de canción
    if st.session_state.autoplay and st.session_state.song_duration > 0:
        time.sleep(2)  # Esperar 2 segundos antes de refrescar
        st.rerun()
    
    st.markdown("---")

# Mostrar todas las listas guardadas con opción de reproducir canciones individuales
if st.session_state.saved_playlists:
    st.header(f"📚 Mis Listas de Reproducción ({len(st.session_state.saved_playlists)})")
    
    # Crear tabs para cada lista
    tab_names = list(st.session_state.saved_playlists.keys())
    if tab_names:
        tabs = st.tabs(tab_names)
        
        for tab_idx, (tab, playlist_name) in enumerate(zip(tabs, tab_names)):
            with tab:
                songs = st.session_state.saved_playlists[playlist_name]
                
                # Encabezado de la lista
                col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
                with col_header1:
                    st.markdown(f"### 🎵 {playlist_name}")
                    st.caption(f"📊 {len(songs)} canciones")
                with col_header2:
                    if st.button("▶️ Reproducir Todo", key=f"play_all_{playlist_name}", use_container_width=True):
                        st.session_state.current_playlist_name = playlist_name
                        st.session_state.playlist = songs.copy()
                        st.session_state.current_index = 0
                        if songs:
                            audio_url = get_audio_url(songs[0]['id'])
                            if audio_url:
                                st.session_state.current_audio_url = audio_url
                                st.session_state.current_title = songs[0]['title']
                                st.session_state.song_duration = songs[0].get('duration', 0)
                                st.session_state.start_time = None
                                st.rerun()
                with col_header3:
                    if st.button("📥 Cargar Lista", key=f"load_list_{playlist_name}", use_container_width=True):
                        st.session_state.current_playlist_name = playlist_name
                        st.session_state.playlist = songs.copy()
                        st.session_state.current_index = 0
                        st.success("Lista cargada")
                        st.rerun()
                
                st.markdown("---")
                
                # Mostrar canciones de la lista
                if songs:
                    for idx, song in enumerate(songs):
                        is_playing = (
                            st.session_state.current_playlist_name == playlist_name and 
                            st.session_state.current_index == idx and
                            st.session_state.current_audio_url is not None
                        )
                        
                        # Crear contenedor para cada canción
                        with st.container():
                            col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1, 1])
                            
                            with col1:
                                icon = "🔊" if is_playing else "🎵"
                                st.markdown(f"### {icon}")
                            
                            with col2:
                                st.markdown(f"**{idx + 1}. {song['title']}**")
                                st.caption(f"👤 {song.get('uploader', 'Desconocido')}")
                            
                            with col3:
                                st.caption(f"⏱️ {format_duration(song.get('duration', 0))}")
                                st.caption(f"👁️ {format_views(song.get('view_count', 0))}")
                            
                            with col4:
                                if st.button("▶️ Reproducir", key=f"play_song_{playlist_name}_{idx}", use_container_width=True):
                                    st.session_state.current_playlist_name = playlist_name
                                    st.session_state.playlist = songs.copy()
                                    st.session_state.current_index = idx
                                    with st.spinner("Cargando..."):
                                        audio_url = get_audio_url(song['id'])
                                        if audio_url:
                                            st.session_state.current_audio_url = audio_url
                                            st.session_state.current_title = song['title']
                                            st.session_state.song_duration = song.get('duration', 0)
                                            st.session_state.start_time = None
                                            st.rerun()
                            
                            with col5:
                                if st.button("🗑️", key=f"remove_song_{playlist_name}_{idx}", use_container_width=True, help="Eliminar de la lista"):
                                    st.session_state.saved_playlists[playlist_name].pop(idx)
                                    save_playlists(st.session_state.saved_playlists)
                                    # Actualizar la lista actual si es la que se está usando
                                    if st.session_state.current_playlist_name == playlist_name:
                                        st.session_state.playlist = st.session_state.saved_playlists[playlist_name].copy()
                                    st.rerun()
                            
                            st.markdown("---")
                else:
                    st.info("📭 Esta lista está vacía. Agrega canciones desde los resultados de búsqueda.")
    
    st.markdown("---")


# Mostrar resultados de búsqueda
if st.session_state.search_results:
    st.header("📋 Resultados de Búsqueda")
    
    # Nota sobre reproducción continua
    if st.session_state.current_audio_url:
        st.info("🎵 **La música sigue sonando** - Puedes agregar canciones a la lista sin interrumpir la reproducción actual")
    
    st.caption(f"📊 {len(st.session_state.search_results)} resultados encontrados")
    
    # Crear columnas para mostrar resultados en grid
    cols_per_row = 2
    results = st.session_state.search_results
    
    for i in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(results):
                result = results[i + j]
                
                with cols[j]:
                    with st.container():
                        # Mostrar miniatura si está disponible
                        if result.get('thumbnail'):
                            st.image(result['thumbnail'], use_container_width=True)
                        
                        # Información del video
                        st.markdown(f"**{result['title']}**")
                        st.caption(f"👤 {result['uploader']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"⏱️ {format_duration(result['duration'])}")
                        with col2:
                            st.caption(f"👁️ {format_views(result['view_count'])}")
                        
                        # Botones para reproducir y agregar a lista
                        col_play, col_add = st.columns(2)
                        with col_play:
                            if st.button(f"▶️ Reproducir", key=f"play_{result['id']}", use_container_width=True):
                                # Agregar a la lista si no está
                                add_to_playlist(result)
                                # Encontrar el índice de esta canción
                                st.session_state.current_index = next(
                                    (i for i, song in enumerate(st.session_state.playlist) if song['id'] == result['id']), 
                                    0
                                )
                                with st.spinner("Cargando audio..."):
                                    audio_url = get_audio_url(result['id'])
                                    if audio_url:
                                        st.session_state.current_audio_url = audio_url
                                        st.session_state.current_title = result['title']
                                        st.session_state.song_duration = result.get('duration', 0)
                                        st.session_state.start_time = None
                                        st.rerun()
                        
                        with col_add:
                            if st.button(f"➕ Agregar", key=f"add_{result['id']}", use_container_width=True):
                                if add_to_playlist(result):
                                    st.success("✅ Agregada a la lista")
                                    # NO hacer rerun para no interrumpir la reproducción
                                else:
                                    st.info("⚠️ Ya está en la lista")
                        
                        st.markdown("---")
else:
    # Mensaje cuando no hay resultados de búsqueda
    if st.session_state.current_audio_url:
        # Si hay música sonando, mostrar mensaje diferente
        st.info("🎵 **Música reproduciéndose** - Usa la barra lateral para buscar y agregar más canciones a la lista")
    else:
        # Mensaje de bienvenida inicial
        st.info("👈 Usa la barra lateral para buscar tu música favorita")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎤 Artistas")
        st.markdown("Busca por tu artista favorito")
        st.caption("🎸 Rock, Pop, Reggaeton...")
    with col2:
        st.markdown("### 🎼 Canciones")
        st.markdown("Encuentra canciones específicas")
        st.caption("🎵 Nuevos lanzamientos y clásicos")
    with col3:
        st.markdown("### 📜 Listas")
        st.markdown("Crea listas personalizadas")
        st.caption("💾 Guardadas permanentemente")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>Desarrollado con ❤️ usando Streamlit | Fuente: YouTube (gratis)</p>
    </div>
    """,
    unsafe_allow_html=True
)
