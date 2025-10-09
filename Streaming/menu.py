import streamlit as st
from datetime import datetime
import os 
import sys

from .usuario import Usuario 
from .analises import Analises
from .playlist import Playlist

def exibir_menu_inicial(usuarios):
    """
    Exibe o menu para login, criação de usuário e listagem de usuários.
    """
    st.header("Bem-vindo!")

    st.subheader("Opções")
    col1, col2, _ = st.columns([1, 1, 4]) 
    
    
    if col1.button("Entrar", use_container_width=True):
        usuario_selecionado = st.session_state.get('usuario_selecionado_nome')
        usuario_encontrado = next((u for u in usuarios if u.nome == usuario_selecionado), None)
        if usuario_encontrado:
            st.session_state['usuario_logado'] = usuario_encontrado
            st.rerun()

    # Botão para fechar o app
    if col2.button("Fechar App", type="primary", use_container_width=True):
        st.success("Aplicação encerrada. Você já pode fechar esta aba.")
        sys.exit() 
    st.divider()
    
    st.subheader("Login")
    nomes_usuarios = [u.nome for u in usuarios]
    
    st.selectbox("Selecione seu usuário:", nomes_usuarios, key='usuario_selecionado_nome')


    with st.expander("Criar novo usuário"):
        novo_nome = st.text_input("Digite o nome do novo usuário:", key="novo_usuario_input")
        if st.button("Criar"):
            if any(u.nome == novo_nome for u in usuarios):
                st.error(f"Erro: Usuário com o nome '{novo_nome}' já existe.")
            elif not novo_nome:
                st.warning("O nome de usuário não pode estar em branco.")
            else:
                novo_usuario = Usuario(nome=novo_nome)
                usuarios.append(novo_usuario)
                st.success(f"Usuário '{novo_nome}' criado com sucesso!")
                st.rerun()

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

    st.sidebar.divider()
    if st.sidebar.button("Ver/Ocultar Top 5 Músicas"):
        st.session_state.mostrar_top_musicas = not st.session_state.get('mostrar_top_musicas', False)
    st.sidebar.divider()

    st.title("Bibilioteca de Músicas e Podcasts")

    if st.session_state.get('mostrar_top_musicas', False):
        with st.container(border=True): 
            st.subheader("🏆 Top 5 Músicas Mais Reproduzidas")
            
            lista_de_musicas = [m for m in midias if hasattr(m, 'genero')]
            top_5 = Analises.top_musicas_reproduzidas(lista_de_musicas, 5) 

            if top_5:
                cols = st.columns(len(top_5))
                for i, musica in enumerate(top_5):
                    with cols[i]:
                        st.metric(label=f"#{i+1}. {musica.titulo}", value=f"{musica.reproducoes} plays", delta=musica.artista)
            else:
                st.info("Nenhuma música foi reproduzida para montar um ranking.")

    # Listar as mídias disponíveis
    st.subheader("Músicas e Podcasts")
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

    with st.sidebar.expander("Gerenciar Playlists"):
        st.subheader("Criar Nova Playlist")
        nome_nova_playlist = st.text_input("Nome da nova playlist:", key="nova_playlist_input")
        
        if st.button("Criar Playlist"):
            if not nome_nova_playlist:
                st.warning("O nome da playlist não pode estar em branco.")
            else:
                try:
                    nova_playlist_obj = usuario.criar_playlist(nome_nova_playlist)
                    st.session_state["playlists"].append(nova_playlist_obj)  
                    st.success(f"Playlist '{nome_nova_playlist}' criada!")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        st.divider()

        st.subheader("Adicionar Mídia à Playlist")
        if usuario.playlists:
            nomes_das_playlists_do_usuario = [p.nome for p in usuario.playlists]
            
            playlist_selecionada_nome = st.selectbox(
                "Escolha a playlist:",
                nomes_das_playlists_do_usuario,
                key="select_playlist_to_add_to" 
            )

            midia_selecionada_titulo = st.selectbox(
                "Escolha a música ou podcast:",
                [m.titulo for m in midias],
                key="select_media_to_add"
            )

            if st.button("Adicionar"):
                playlist_obj = next((p for p in usuario.playlists if p.nome == playlist_selecionada_nome), None)
                midia_obj = next((m for m in midias if m.titulo == midia_selecionada_titulo), None)
                
                if playlist_obj and midia_obj:
                    try:
                        playlist_obj.adicionar_midia(midia_obj)
                        st.success(f"'{midia_obj.titulo}' adicionado(a) à playlist '{playlist_obj.nome}'!")
                    except ValueError as e:
                        st.warning(str(e))
                
                st.rerun()
                
        else:
            st.info("Você precisa criar uma playlist antes de poder adicionar mídias.")
    
    #Mostra a opção apenas se o usuário tiver 2 ou mais playlists
        if len(usuario.playlists) >= 2:
            nomes_das_playlists = [p.nome for p in usuario.playlists]
            
            #Seleciona a primeira playlist
            p1_nome = st.selectbox(
                "Escolha a primeira playlist:",
                nomes_das_playlists,
                key="concat_p1"
            )

            #Seleciona a segunda playlist
            p2_nome = st.selectbox(
                "Escolha a segunda playlist:",
                nomes_das_playlists,
                index=1 if len(nomes_das_playlists) > 1 else 0, #Evita que as duas sejam iguais no início
                key="concat_p2"
            )

            if st.button("Concatenar"):
                if p1_nome == p2_nome:
                    st.warning("Por favor, selecione duas playlists diferentes.")
                else:
                    #Encontra os objetos das playlists selecionadas
                    p1_obj = next((p for p in usuario.playlists if p.nome == p1_nome), None)
                    p2_obj = next((p for p in usuario.playlists if p.nome == p2_nome), None)

                    if p1_obj and p2_obj:
                        playlist_resultante = p1_obj + p2_obj
                        
                        # Adiciona a nova playlist à lista do usuário e à lista global
                        usuario.playlists.append(playlist_resultante)
                        playlists.append(playlist_resultante)

                        st.success(f"Playlist '{playlist_resultante.nome}' criada com sucesso!")
                        st.rerun()
        else:
            st.info("Você precisa de pelo menos duas playlists para concatenar.")

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