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
    # Se ninguém está logado, mostra o menu inicial
    # Usaremos a função do arquivo menu.py para manter o main.py limpo
    exibir_menu_inicial(st.session_state.usuarios)
else:
    # Se um usuário está logado, mostra o menu principal dele
    exibir_menu_usuario(
        usuario=st.session_state.usuario_logado,
        midias=st.session_state.midias,
        playlists=st.session_state.playlists,
        usuarios_gerais=st.session_state.usuarios
    )


    '''
    # ... Implementar as outras opções: listar playlists [cite: 28], criar playlist[cite: 30], etc. ...
    # Para o relatório, crie um botão que chama os métodos da classe Analises
    if st.button("Gerar Relatório de Análises"): # [cite: 32]
        # Chamar os métodos estáticos da classe Analises
        top_5 = Analises.top_musicas_reproduzidas([m for m in st.session_state.midias if isinstance(m, Musica)], 5)
        # ... chamar outros métodos ...
        # Formatar os resultados e salvar em relatorios/relatorio.txt [cite: 88]
        st.success("Relatório gerado com sucesso!") 
    '''    