"""
Exemplo de uso do resolvedor de Kuromasu.
"""

from kuromasu_resolvedor import resolver_kuromasu
from kuromasu_modelo import (
    ESTADO_BRANCO,
    ESTADO_PRETO,
    imprimir_tabuleiro,
)


def ler_tabuleiro_de_arquivo(caminho_arquivo):
    """
    Lê um tabuleiro de um arquivo de texto.
    - Cada linha do arquivo é uma linha do tabuleiro.
    - Células separadas por espaço.
    - Use '.' para célula sem número.
    - Use inteiros (ex: 3, 10) para células numeradas.
    """
    tabuleiro_numeros = []
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha_texto in arquivo:
            linha_texto = linha_texto.strip()
            if not linha_texto:
                continue
            partes = linha_texto.split()
            linha_numeros = []
            for parte in partes:
                if parte == ".":
                    linha_numeros.append(None)
                else:
                    linha_numeros.append(int(parte))
            tabuleiro_numeros.append(linha_numeros)
    return tabuleiro_numeros


def criar_tabuleiro_exemplo():
    """
    Cria um pequeno tabuleiro de exemplo.
    None = sem número.
    """
    return [
        [None, 4,    None, None],
        [None, None, None, None],
        [None, None, 6,    None],
        [None, None, None, None],
    ]


def main():
    # Usa o tabuleiro definido no código
    #tabuleiro_numeros = criar_tabuleiro_exemplo()

    # Ler do arquivo
    caminho = "tabuleiro_kuromasu.txt"
    tabuleiro_numeros = ler_tabuleiro_de_arquivo(caminho)

    solucao_estados = resolver_kuromasu(tabuleiro_numeros)

    if solucao_estados is None:
        print("Não foi encontrada solução para este tabuleiro.")
    else:
        print("Solução encontrada:")
        imprimir_tabuleiro(tabuleiro_numeros, solucao_estados)


if __name__ == "__main__":
    main()
