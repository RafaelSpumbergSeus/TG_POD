from .musica import Musica
from .playlist import Playlist
from .usuario import Usuario

class Analises:
  
    @staticmethod
    def top_musicas_reproduzidas(musicas, top_n: int): 
        # Ordena a lista de musicas pelo atributo 'reproducoes' em ordem decrescente
        # Retorna os top_n primeiros elementos
        def obter_reproducoes(musica):
            return musica.reproducoes
        
        musicas_ordenadas = sorted(musicas, key=obter_reproducoes, reverse=True)

        return musicas_ordenadas[:top_n]

    
    @staticmethod
    def playlist_mais_popular(playlists): 
       if not playlists:
           return None
       
       def obter_reproducoes_playlist(playlist):
              return playlist.reproducoes
       
       return max(playlists, key=obter_reproducoes_playlist)
    
    @staticmethod
    def usuario_mais_ativo(usuarios): 
        """Retorna o usuário que mais ouviu mídias (maior histórico)."""
        if not usuarios:
            return None

        def obter_tamanho_historico(usuario):
            return len(usuario.historico)

        return max(usuarios, key=obter_tamanho_historico)

    @staticmethod
    def media_avaliacoes(musicas): 
        """Retorna um dicionário com a média de avaliação de cada música."""
        media_por_musica = {}
        for musica in musicas:
            # Verifica se a música tem alguma avaliação para não dar erro de divisão por zero.
            if musica.avaliacoes:
                soma_das_notas = sum(musica.avaliacoes)
                quantidade_de_notas = len(musica.avaliacoes)
                media = soma_das_notas / quantidade_de_notas
                
                # Arredonda o resultado para 2 casas decimais para ficar mais bonito.
                media_por_musica[musica.titulo] = round(media, 2)
            else:
                # Se a música não tem avaliações, a média é 0.
                media_por_musica[musica.titulo] = 0.0
                
        return media_por_musica

    @staticmethod
    def total_reproducoes(usuarios): 
        """Retorna o total de reproduções feitas por todos os usuários."""
        total = 0
        for usuario in usuarios:
            # Somamos o número de músicas no histórico dele ao nosso total.
            total = total + len(usuario.historico)
            
        return total
