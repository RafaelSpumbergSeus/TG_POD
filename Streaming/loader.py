import logging
from .usuario import Usuario
from .musica import Musica
from .podcast import Podcast

# Configura o sistema de log para registrar erros em um arquivo.
# 'filemode='w'' faz com que o arquivo de log seja limpo toda vez que o programa roda.
logging.basicConfig(filename='logs/erros.log', 
                    level=logging.ERROR,
                    format='%(asctime)s - ERRO: %(message)s',
                    filemode='w') 

def carregar_dados(caminho_do_arquivo):
    """
    Lê o arquivo .md, cria os objetos e registra os erros de forma simples.
    """
    
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        logging.error(f"O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return None

    usuarios_criados = {}
    midias_criadas = {}
    playlists_criadas = []
    
    info_usuarios = []
    info_musicas = []
    info_podcasts = []
    info_playlists = []
    
    secao_atual = ''
    item_atual = None

    # 2. SEPARAR AS INFORMAÇÕES POR CATEGORIA
    for linha in linhas:
        linha = linha.strip()

        # Ignorar linhas vazias ou separadores ---
        if not linha or linha.startswith('---'):
            continue

        # Detecta mudança de seção
        if linha.startswith('#'):
            secao_atual = linha.replace('#', '').strip()
            continue

        # Novo item
        if linha.startswith('-'):
            item_atual = {}
            conteudo = linha.replace('-', '', 1).strip()

            if ':' in conteudo:
                chave, valor = conteudo.split(':', 1)
                item_atual[chave.strip()] = valor.strip()
            else:
                logging.error(f"Linha inválida sem ':': {linha}")
                continue
            
            if secao_atual == 'Usuários':
                info_usuarios.append(item_atual)
            elif secao_atual == 'Músicas':
                info_musicas.append(item_atual)
            elif secao_atual == 'Podcasts':
                info_podcasts.append(item_atual)
            elif secao_atual == 'Playlists':
                info_playlists.append(item_atual)
        
        # Linha de atributo extra do último item
        elif ':' in linha and item_atual is not None:
            chave, valor = linha.split(':', 1)
            item_atual[chave.strip()] = valor.strip()
        else:
            logging.error(f"Linha fora do padrão ignorada: {linha}")

    # 3. CRIAR OS OBJETOS A PARTIR DAS INFORMAÇÕES SEPARADAS

    # Criar Usuários
    for info in info_usuarios:
        nome = info['nome']
        if nome not in usuarios_criados:
            usuarios_criados[nome] = Usuario(nome=nome)
        else:
            logging.error(f"Usuário duplicado encontrado e ignorado: '{nome}'.")

    # Criar Músicas
    for info in info_musicas:
        try:
            titulo = info['titulo']
            duracao = int(info['duracao'])
            musica = Musica(titulo=titulo, artista=info['artista'], genero=info['genero'], duracao=duracao)
            midias_criadas[titulo] = musica
        except Exception as e:
            logging.error(f"Falha ao carregar música '{info.get('titulo', 'N/A')}'. Detalhe: {e}")

    # Criar Podcasts
    for info in info_podcasts:
        try:
            titulo = info['titulo']
            duracao = int(info['duracao'])
            episodio = int(info['episodio'])
            podcast = Podcast(
                titulo=titulo,
                artista=info['temporada'],  # aqui tu usou temporada como artista, confere?
                duracao=duracao, 
                host=info['host'], 
                temporada=info['temporada'], 
                episodio=episodio
            )
            midias_criadas[titulo] = podcast
        except Exception as e:
            logging.error(f"Falha ao carregar podcast '{info.get('titulo', 'N/A')}'. Detalhe: {e}")

    # Criar Playlists
    for info in info_playlists:
        nome_usuario = info['usuario']
        nome_playlist = info['nome']
        
        usuario = usuarios_criados.get(nome_usuario)
        if not usuario:
            logging.error(f"Usuário '{nome_usuario}' da playlist '{nome_playlist}' não existe. Playlist ignorada.")
            continue

        try:
            playlist = usuario.criar_playlist(nome_playlist)
            playlists_criadas.append(playlist)
            
            nomes_das_midias = info['itens'].strip('[]').split(',')
            
            for nome_midia in nomes_das_midias:
                nome_midia = nome_midia.strip()
                midia = midias_criadas.get(nome_midia)
                if midia:
                    playlist.adicionar_midia(midia)
                else:
                    logging.error(f"Mídia '{nome_midia}' da playlist '{nome_playlist}' não existe e foi ignorada.")
                    
        except Exception as e:
            logging.error(f"Falha ao criar a playlist '{nome_playlist}'. Detalhe: {e}")

    return {
        "usuarios": list(usuarios_criados.values()),
        "midias": list(midias_criadas.values()),
        "playlists": playlists_criadas
    }
