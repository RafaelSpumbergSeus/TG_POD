class Playlist:
    """Representa uma playlist de mídias."""
    def __init__(self, nome: str, usuario):
        self.nome = nome # [cite: 51]
        self.usuario = usuario # [cite: 52]
        self.itens = [] # [cite: 53]
        self.reproducoes = 0 # [cite: 54]

    def adicionar_midia(self, midia): # [cite: 56]
        self.itens.append(midia)

    def remover_midia(self, midia): # [cite: 57]
        self.itens.remove(midia)

    def reproduzir(self): # [cite: 58]
        """Reproduz todos os itens da playlist em sequência."""
        print(f"--- Reproduzindo a playlist: {self.nome} ---")
        for item in self.itens:
            item.reproduzir() # Isso já incrementa a reprodução da mídia individual
        self.reproducoes += 1

    def __add__(self, other): # [cite: 59]
        """Concatena duas playlists."""
        nova_playlist = Playlist(self.nome, self.usuario) # Mantém nome e usuário da primeira [cite: 60]
        nova_playlist.itens = self.itens + other.itens # Concatena os itens [cite: 60]
        nova_playlist.reproducoes = self.reproducoes + other.reproducoes # Soma as reproduções [cite: 60]
        return nova_playlist

    def __len__(self): # [cite: 61]
        return len(self.itens)

    def __getitem__(self, index): # [cite: 62]
        return self.itens[index]

    def __eq__(self, other): # [cite: 63]
        """Compara playlists pelo nome, criador e itens."""
        return self.nome == other.nome and self.usuario == other.usuario and self.itens == other.itens

    def __str__(self):
        return f"Playlist '{self.nome}' de {self.usuario.nome} ({len(self.itens)} itens)"

    def __repr__(self):
        return f"<Playlist(nome={self.nome}, usuario={self.usuario.nome})>"
