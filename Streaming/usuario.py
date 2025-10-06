from .playlist import Playlist 

class Usuario:
    #Usuário
    qntd_instancias = 0 

    def __init__(self, nome: str):
        self.nome = nome 
        self.playlists = [] 
        self.historico = [] 
        Usuario.qntd_instancias += 1

    def ouvir_midia(self, midia): 
        """Adiciona uma mídia ao histórico do usuário e a reproduz."""
        midia.reproduzir()
        self.historico.append(midia)
    
    def criar_playlist(self, nome_playlist: str): 
        #Verifica se já existe uma playlist com o mesmo nome para este usuário 
        for p in self.playlists:
            if p.nome == nome_playlist:
                # Se encontrar, levanta um erro com uma mensagem clara.
                raise ValueError(f"O usuário '{self.nome}' já possui uma playlist chamada '{nome_playlist}'.")
               
        nova_playlist = Playlist(nome=nome_playlist, usuario=self)
        
        self.playlists.append(nova_playlist)
        
        return nova_playlist

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"<Usuario(nome={self.nome})>"
