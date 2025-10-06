TG1: Streaming de Música - Programação Orientada à Dados 

Este projeto é uma implementação de um sistema de streaming musical simplificado, desenvolvido como parte da disciplina de Programação Orientada à Dados. O objetivo é aplicar conceitos de Programação Orientada a Objetos (POO) para abstrair e modelar um sistema complexo, inspirado em plataformas como o Spotify.

O sistema permite que usuários criem contas, montem playlists, reproduzam mídias (músicas e podcasts) e acompanhem estatísticas de uso. Toda a interface é construída com a biblioteca Streamlit.

✨ Funcionalidades
Gerenciamento de Usuários:

Criar novos usuários.

Entrar com um usuário existente.

Listar todos os usuários cadastrados.

Biblioteca de Mídia:

Listar todas as músicas e podcasts disponíveis.

Simular a reprodução de mídias individuais, que contabiliza o número de execuções.

Gerenciamento de Playlists:

Criar novas playlists associadas ao usuário logado.

Listar as playlists existentes.

Reproduzir playlists completas.

Concatenar duas playlists para criar uma terceira.

Análises e Relatórios:

Gerar um relatório com estatísticas detalhadas , como as músicas mais ouvidas, a playlist mais popular e o usuário mais ativo.


Logs:

Registrar erros de carregamento e de execução (ex: música inexistente em uma playlist) em um arquivo de log dedicado.


📂 Estrutura do Projeto
O projeto segue a estrutura de pacotes Python recomendada para organização e modularidade:

Streaming/
├── __init__.py
├── analises.py
├── arquivo_de_midia.py
├── loader.py
├── menu.py
├── musica.py
├── podcast.py
├── playlist.py
└── usuario.py
config/
└── dados.md
logs/
└── erros.log
relatorios/
└── relatorio.txt
main.py
README.md


🚀 Tecnologias Utilizadas
Python 3.10+

Streamlit (para a interface de usuário)

Bibliotecas Nativas do Python (

os, datetime, logging, abc) 

🔧 Instalação e Configuração
Siga os passos abaixo para configurar o ambiente e rodar o projeto.

1. Clone o repositório:

Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
2. Crie e ative um ambiente virtual (Recomendado):

Bash

# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências:
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

streamlit
Em seguida, instale-o com o pip:

Bash

pip install -r requirements.txt
4. Arquivo de Configuração:
O sistema carrega os dados iniciais do arquivo 

config/dados.md. Certifique-se de que este arquivo esteja presente e formatado corretamente.

▶️ Como Executar
Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no terminal, a partir da pasta raiz do projeto:

Bash

streamlit run main.py
A aplicação será aberta automaticamente no seu navegador.

💡 Funcionalidade de Inovação 

Como funcionalidade extra, foi implementado um sistema de recomendação simples. Ao reproduzir uma música, o sistema pode sugerir outras mídias baseadas no histórico de outros usuários que também ouviram aquela música.

👥 Autor
Rafael Spumberg e Arthur 