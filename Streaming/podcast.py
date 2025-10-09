from .arquivo_de_midia import ArquivoDeMidia

class Podcast(ArquivoDeMidia):
    #Podcast, herdando de ArquivoDeMidia
    def __init__(self, titulo: str, artista: str, duracao: int, host: str, temporada: str, episodio: int):
        # No caso do podcast, "artista" pode ser o nome do programa/produtora
        super().__init__(titulo, artista, duracao)
        self.host = host 
        self.temporada = temporada 
        self.episodio = episodio 
    
    # Implementação dos métodos abstratos
    def reproduzir(self):
        print(f"Reproduzindo Podcast: {self.titulo} (Ep. {self.episodio}) - Host: {self.host}")
        self.reproducoes += 1

