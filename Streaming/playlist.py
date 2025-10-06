from .arquivo_de_midia import ArquivoDeMidia
class Playlist:
    """Representa uma playlist de mídias."""
    def __init__(self, nome: str, usuario):
        self.nome = nome 
        self.usuario = usuario 
        self.itens = [] 
        self.reproducoes = 0 

    def adicionar_midia(self, midia): 
        self.itens.append(midia)

    def remover_midia(self, midia): 
        self.itens.remove(midia)

    def reproduzir(self): 
        """Reproduz todos os itens da playlist em sequência."""
        print(f"--- Reproduzindo a playlist: {self.nome} ---")
        for item in self.itens:
            item.reproduzir() 
        self.reproducoes += 1

    def __add__(self, other): 
        """Concatena duas playlists."""
        nova_playlist = Playlist(self.nome, self.usuario) 
        nova_playlist.itens = self.itens + other.itens 
        nova_playlist.reproducoes = self.reproducoes + other.reproducoes # Soma as reproduções 
        return nova_playlist

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
