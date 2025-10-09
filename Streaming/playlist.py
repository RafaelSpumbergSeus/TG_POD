from .arquivo_de_midia import ArquivoDeMidia
class Playlist:
    """Representa uma playlist de mídias."""
    def __init__(self, nome: str, usuario):
        self.nome = nome 
        self.usuario = usuario 
        self.itens = [] 
        self.reproducoes = 0 

    def adicionar_midia(self, midia):
        if midia not in self.itens:
            self.itens.append(midia)
        else:
            raise ValueError(f"A mídia '{midia.titulo}' já está na playlist '{self.nome}'.") 
        
    def remover_midia(self, midia): 
        self.itens.remove(midia)

    def reproduzir(self): 
        """Reproduz todos os itens da playlist em sequência."""
        print(f"Reproduzindo a playlist: {self.nome}")
        for item in self.itens:
            item.reproduzir() 
        self.reproducoes += 1

    def __add__(self, other): 
        if not isinstance(other, Playlist):
           return NotImplemented
       
        novo_nome = f"{self.nome} + {other.nome}"
        playlist_concatenada = Playlist(nome=novo_nome, usuario=self.usuario)
        itens_combinados = self.itens + other.itens
        playlist_concatenada.itens = list(dict.fromkeys(itens_combinados))
        playlist_concatenada.reproducoes = self.reproducoes + other.reproducoes
        
        return playlist_concatenada

    def __len__(self): 
        return len(self.itens)

    def __getitem__(self, index): 
        return self.itens[index]

    def __eq__(self, other): 
        """Compara playlists pelo nome, criador e itens."""
        return self.nome == other.nome and self.usuario == other.usuario and self.itens == other.itens

    def __str__(self):
        return f"Playlist '{self.nome}' de {self.usuario.nome} ({len(self.itens)} itens)"

    def __repr__(self):
        return f"<Playlist(nome={self.nome}, usuario={self.usuario.nome})>"
