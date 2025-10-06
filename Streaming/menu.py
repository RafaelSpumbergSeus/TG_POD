import streamlit as st
from datetime import datetime
import os 

from .usuario import Usuario 
from .analises import Analises

def exibir_menu_inicial(usuarios):
    """
    Exibe o menu para login, criação de usuário e listagem de usuários.
    """
    st.header("Bem-vindo ao Streming de Música Genérico!")

    #Primeira opcao 
    st.subheader("Entrar como usuário")
    nomes_usuaiors = [u.nome for u in usuarios]
    usuario_selecionado = st.selectbox("Selecione seu usuário:", nomes_usuaiors)

    if st.button("Entrar"):
        usuario_encontrado = next((u for u in usuarios if u.nome == usuario_selecionado), None)
        if usuario_encontrado:
            st.session_state['usuario_logado'] = usuario_encontrado
            st.rerun()

    with st.expander("Criar novo usuário"):
        novo_nome = st.text_input("Digite o nome do novo usuário:")
        if st.button("Criar"):
            if any(u.nome == novo_nome for u in usuarios):
                st.error(f"Usuário '{novo_nome}' já existe. Escolha outro nome.")
            elif not novo_nome:
                st.warning("O nome do usuário não pode ser vazio.")
            else:
                novo_usuario = Usuario(novo_nome)
                usuarios.append(novo_usuario)
                st.success(f"Usuário '{novo_nome}' criado com sucesso!")

    with st.expander("Listar usuários"):
        for u in usuarios:
            st.write(f"- {u.nome} ({len(u.playlists)} playlists)")

def exibir_menu_usuario(usuario, midias, playlists, usuarios_gerais):
    """
    Exibe o menu para o usuário logado.
    """
    st.sidebar.header(f"Olá, {usuario.nome}!")

    if st.sidebar.button("Sair"):
        st.session_state['usuario_logado'] = None
        st.rerun()

    st.title("Bibilioteca de Músicas e Podcasts")

    # Listar as mídias disponíveis
    st.subheader("Músicas Disponíveis")
    for midia in midias:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{midia.titulo}** - {midia.artista}")
        with col2:
            if st.button("▶️ Ouvir", key=f"play_{midia.titulo}"):
                usuario.ouvir_midia(midia)
                st.toast(f"Reproduzindo {midia.titulo}!")

     # Gerenciar Playlists
    st.subheader("Suas Playlists")
    for p in usuario.playlists:
        with st.expander(f"{p.nome} ({len(p.itens)} itens)"):
            for item in p.itens:
                st.write(f"- {item.titulo}")
            if st.button(f"Reproduzir Playlist '{p.nome}'", key=f"play_playlist_{p.nome}"):
                # A reprodução no backend já incrementa os contadores
                p.reproduzir()
                st.success(f"Playlist '{p.nome}' reproduzida!")

    # Ações do Usuário
    with st.sidebar.expander("Ações"):
        st.subheader("Criar Nova Playlist")
        nome_nova_playlist = st.text_input("Nome da nova playlist:")
        if st.button("Criar Playlist"):
            try:
                usuario.criar_playlist(nome_nova_playlist)
                st.success(f"Playlist '{nome_nova_playlist}' criada!")
                st.rerun()
            except ValueError as e:
                st.error(str(e)) #

    # Relatórios
    if st.sidebar.button("Gerar Relatório de Análises"):
        # Garante que o diretório de relatórios exista
        if not os.path.exists('relatorios'):
            os.makedirs('relatorios')

        lista_de_musicas = [m for m in midias if hasattr(m, 'genero')]
        
        top_5_musicas = Analises.top_musicas_reproduzidas(lista_de_musicas, 5)
        playlist_pop = Analises.playlist_mais_popular(playlists)
        user_ativo = Analises.usuario_mais_ativo(usuarios_gerais)
        medias = Analises.media_avaliacoes(lista_de_musicas)
        total_plays = Analises.total_reproducoes(usuarios_gerais)

        # Formata o conteúdo do relatório
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        relatorio_conteudo = f"""# Relatório de Análises do MusicStream
Gerado em: {timestamp}

## Músicas Mais Populares (Top 5)
"""
        if top_5_musicas:
            for i, m in enumerate(top_5_musicas):
                relatorio_conteudo += f"{i+1}. {m.titulo} - {m.artista} ({m.reproducoes} reproduções)\n"
        else:
            relatorio_conteudo += "Nenhuma música foi reproduzida ainda.\n"

        relatorio_conteudo += f"""

## Playlist Mais Popular
- {playlist_pop.nome if playlist_pop else 'N/A'} ({playlist_pop.reproducoes if playlist_pop else 0} reproduções)

## Usuário Mais Ativo
- {user_ativo.nome if user_ativo else 'N/A'} ({len(user_ativo.historico) if user_ativo else 0} mídias ouvidas)

## Total de Reproduções no Sistema
- {total_plays}

## Média de Avaliações por Música
"""
        if medias:
            for titulo, media in medias.items():
                relatorio_conteudo += f"- {titulo}: {media:.2f}\n"
        else:
            relatorio_conteudo += "Nenhuma música para avaliar.\n"

        # Salva o relatório em um arquivo
        with open("relatorios/relatorio.txt", "w", encoding="utf-8") as f:
            f.write(relatorio_conteudo)
        
        st.success("Relatório salvo em 'relatorios/relatorio.txt'!")
        st.balloons()     