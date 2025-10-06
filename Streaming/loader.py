import logging
from .usuario import Usuario
from .musica import Musica
from .podcast import Podcast


logging.basicConfig(filename='logs/erros.log', 
                    level=logging.ERROR,
                    format='%(asctime)s - ERRO: %(message)s',
                    filemode='w') 

def carregar_dados(caminho_do_arquivo):
    """
    Lê o arquivo .md, cria os objetos e registra os erros de forma simples e robusta.
    """
    
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        logging.error(f"O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return None

    info_usuarios = []
    info_musicas = []
    info_podcasts = []
    info_playlists = []
    
    secao_atual = None
    item_atual = None

    for linha in linhas:
        linha_limpa = linha.strip()

        if not linha_limpa or linha_limpa.startswith('---'):
            continue

        if linha_limpa.startswith('#'):
            secao_atual = linha_limpa.replace('#', '').strip()
            item_atual = None 
            continue

        if linha.startswith('-'):
            item_atual = {}
            conteudo = linha_limpa.replace('-', '', 1).strip()
            
            if ':' in conteudo:
                chave, valor = conteudo.split(':', 1)
                item_atual[chave.strip()] = valor.strip()
                
                if secao_atual == 'Usuários': info_usuarios.append(item_atual)
                elif secao_atual == 'Músicas': info_musicas.append(item_atual)
                elif secao_atual == 'Podcasts': info_podcasts.append(item_atual)
                elif secao_atual == 'Playlists': info_playlists.append(item_atual)
            else:
                logging.error(f"Linha de item principal mal formatada (falta ':'): {linha_limpa}")
                item_atual = None

        elif item_atual is not None and ':' in linha_limpa:
            chave, valor = linha_limpa.split(':', 1)
            item_atual[chave.strip()] = valor.strip()


    usuarios_criados = {}
    for info in info_usuarios:
        nome = info.get('nome')
        if nome and nome not in usuarios_criados:
            usuarios_criados[nome] = Usuario(nome=nome)
        elif nome in usuarios_criados:
            logging.error(f"Usuário duplicado encontrado e ignorado: '{nome}'.")

    midias_criadas = {}
    for info in info_musicas:
        try:
            titulo = info['titulo']
            duracao = int(info['duracao'])
            musica = Musica(titulo=titulo, artista=info['artista'], genero=info['genero'], duracao=duracao)
            midias_criadas[titulo] = musica
        except (KeyError, ValueError) as e:
            logging.error(f"Falha ao carregar música '{info.get('titulo', 'N/A')}'. Detalhe: {e}")

    for info in info_podcasts:
        try:
            titulo = info['titulo']
            duracao = int(info['duracao'])
            episodio = int(info['episodio'])
        
            podcast = Podcast(titulo=titulo, artista=info['temporada'], duracao=duracao, 
                              host=info['host'], temporada=info['temporada'], episodio=episodio)
            midias_criadas[titulo] = podcast
        except (KeyError, ValueError) as e:
            logging.error(f"Falha ao carregar podcast '{info.get('titulo', 'N/A')}'. Detalhe: {e}")

    playlists_criadas = []
    for info in info_playlists:
        try:
            nome_usuario = info['usuario']
            nome_playlist = info['nome']
            
            usuario = usuarios_criados.get(nome_usuario)
            if not usuario:
                raise ValueError(f"Usuário '{nome_usuario}' não encontrado")

            playlist = usuario.criar_playlist(nome_playlist)
            playlists_criadas.append(playlist)
            
            nomes_das_midias = info['itens'].strip('[]').split(',')
            for nome_midia in nomes_das_midias:
                nome_midia = nome_midia.strip()
                midia = midias_criadas.get(nome_midia)
                if midia:
                    playlist.adicionar_midia(midia)
                else:
                    logging.warning(f"Mídia '{nome_midia}' na playlist '{nome_playlist}' não existe e foi ignorada.")
                    
        except Exception as e:
            logging.error(f"Falha ao criar a playlist '{info.get('nome', 'N/A')}'. Detalhe: {e}")

    return {
        "usuarios": list(usuarios_criados.values()),
        "midias": list(midias_criadas.values()),
        "playlists": playlists_criadas
    }