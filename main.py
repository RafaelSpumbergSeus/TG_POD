import streamlit as st
from Streaming.loader import carregar_dados
from Streaming.menu import exibir_menu_inicial, exibir_menu_usuario 

if 'dados_carregados' not in st.session_state:
    dados = carregar_dados('config/dados1.md')
    
    if dados:
        st.session_state.usuarios = dados['usuarios']
        st.session_state.midias = dados['midias'] 
        st.session_state.playlists = dados['playlists']
        st.session_state.usuario_logado = None 
        st.session_state.dados_carregados = True
    else:
        # Se os dados não carregarem, mostra um erro e para
        st.error("Falha crítica ao carregar os dados. Verifique o arquivo 'logs/erros.log'.")
        st.stop()

# ---  INTERFACE  ---

st.title("Streaming de Música Genérico")

# Decide qual menu mostrar baseado no estado de login
if st.session_state.get('usuario_logado') is None:
    exibir_menu_inicial(st.session_state.usuarios)
else:
    exibir_menu_usuario(
        usuario=st.session_state.usuario_logado,
        midias=st.session_state.midias,
        playlists=st.session_state.playlists,
        usuarios_gerais=st.session_state.usuarios
    )
