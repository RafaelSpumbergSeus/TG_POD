from .arquivo_de_midia import ArquivoDeMidia

class Musica(ArquivoDeMidia):

    #Representa uma música, herdando de ArquivoDeMidia.

    def __init__(self, titulo: str, artista: str, duracao: int, genero: str):
        super().__init__(titulo, artista, duracao)
        self.genero = genero 
        self.avaliacoes = [] 

    def avaliar(self, nota: int): 
        #Adiciona uma nota de 0 a 5 à lista de avaliações.
        if 0 <= nota <= 5:
            self.avaliacoes.append(nota)
        else:
            raise ValueError("A nota deve estar entre 0 e 5.")

    def reproduzir(self):
        super().reproduzir()

    