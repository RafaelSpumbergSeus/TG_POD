from abc import ABC, abstractmethod

class ArquivoDeMidia(ABC):
    def __init__(self, titulo: str, artista: str, duracao: int):
        # validação de tamanho 

        if duracao < 0:
            raise ValueError("A duração não pode ser negativa.")
        
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao
        self.reproducoes = 0

    @abstractmethod
    def reproduzir(self):
        #Simula a reprodução do arquivo de mídia
        print(f"Reproduzindo {self.titulo} de {self.artista} ({self.duracao}s)")
        self.reproducoes += 1

    def __eq__(self, other): 
        # Compara dois arquivos de mídia
        if not isinstance(other, ArquivoDeMidia):
            return NotImplemented
        return self.titulo == other.titulo and self.artista == other.artista
    
    def __hash__(self):
        return hash((self.titulo, self.artista))
    
    def __str__(self):
        return f"{self.titulo} por {self.artista}"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(titulo={self.titulo}, artista={self.artista})>"