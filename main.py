import streamlit as st  
from Streaming.loader import carregar_dados
from Streaming.analises import Analises

if 'dados_carregados' not in st.session_state:
    '''nome do arquivo de dados'''
    dados = carregar_dados('config/dados1.md')
    st.session_state.usuarios = dados['usuarios']
    st.session_state.mideias = dados['midias']
    st.session_state.playlists = dados['playlists']
    st.session_state.dados_usuario_logado = None
    st.session_state.dados_carregados = True

    # ------- Interface do Streamlit ------- #

    st.title("Streming de Música Genérico")

    if st.session_state.usuario_logado is None: 
        st.header("Bem-vindo!")

        menu_inicial = ["Entrar como usuário", "Criar novo usuário", "Listar usuários"] 
        escolha = st.selectbox("O que você deseja fazer?", menu_inicial)

        if escolha == "Entrar como usuário":
            nomes_usuarios = [u.nome for u in st.session_state.usuarios]
            usuario_selecionado = st.selectbox("Selecione seu usuário:", nomes_usuarios)
            if st.button("Entrar"):
               st.session_state.usuario_logado = next(u for u in st.session_state.usuarios if u.nome == usuario_selecionado)
            st.rerun() # Recarrega a página para mostrar o menu do usuário

    # ... Implementar "Criar novo usuário" e "Listar usuários" ...

# Se um usuário está logado, mostra o menu principal
else:
    usuario = st.session_state.usuario_logado
    st.header(f"Olá, {usuario.nome}!")

    if st.button("Sair"):
        st.session_state.usuario_logado = None
        st.rerun()

    st.subheader("Músicas Disponíveis") # [cite: 26]
    for midia in st.session_state.midias:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{midia.titulo} - {midia.artista}")
        with col2:
            if st.button("▶️ Ouvir", key=f"play_{midia.titulo}"):
                usuario.ouvir_midia(midia) # Chama o método do backend [cite: 70]
                st.toast(f"Reproduzindo {midia.titulo}!")

    # ... Implementar as outras opções: listar playlists [cite: 28], criar playlist[cite: 30], etc. ...
    # Para o relatório, crie um botão que chama os métodos da classe Analises
    if st.button("Gerar Relatório de Análises"): # [cite: 32]
        # Chamar os métodos estáticos da classe Analises
        top_5 = Analises.top_musicas_reproduzidas([m for m in st.session_state.midias if isinstance(m, Musica)], 5)
        # ... chamar outros métodos ...
        # Formatar os resultados e salvar em relatorios/relatorio.txt [cite: 88]
        st.success("Relatório gerado com sucesso!") 