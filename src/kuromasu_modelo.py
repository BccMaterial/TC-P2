"""
Funções de modelo e verificação de regras do quebra-cabeça Kuromasu.

Regras principais:
- Células numeradas são sempre brancas.
- Nenhuma célula preta pode ser adjacente (cima/baixo/esquerda/direita) a outra preta.
- Cada número indica quantas células brancas são "visíveis" na mesma linha/coluna,
  incluindo a própria, parando ao encontrar uma célula preta ou a borda.
- Todas as células brancas devem formar um único componente conexo (4-direções).
"""

ESTADO_DESCONHECIDO = -1
ESTADO_BRANCO = 0
ESTADO_PRETO = 1


def dimensoes(tabuleiro):
    quantidade_linhas = len(tabuleiro)
    quantidade_colunas = len(tabuleiro[0]) if quantidade_linhas > 0 else 0
    return quantidade_linhas, quantidade_colunas


def esta_dentro(tabuleiro, linha, coluna):
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro)
    return 0 <= linha < quantidade_linhas and 0 <= coluna < quantidade_colunas


def vizinhos_ortogonais(tabuleiro, linha, coluna):
    deslocamentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dl, dc in deslocamentos:
        nova_linha = linha + dl
        nova_coluna = coluna + dc
        if esta_dentro(tabuleiro, nova_linha, nova_coluna):
            yield nova_linha, nova_coluna


def contar_visiveis(tabuleiro_numeros, tabuleiro_estados, linha, coluna):
    """
    Conta quantas células brancas são visíveis a partir de (linha, coluna),
    incluindo ela mesma, em todas as 4 direções.
    Supõe que a célula (linha, coluna) é branca.
    """
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)

    total = 1  # conta a própria célula

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dl, dc in direcoes:
        l = linha + dl
        c = coluna + dc
        while 0 <= l < quantidade_linhas and 0 <= c < quantidade_colunas:
            if tabuleiro_estados[l][c] == ESTADO_PRETO:
                break
            # branca (e, em solução final, numerada também é branca)
            total += 1
            l += dl
            c += dc

    return total


def intervalo_visiveis(tabuleiro_numeros, tabuleiro_estados, linha, coluna):
    """
    Calcula (minimo, maximo) de células brancas visíveis para um número
    na posição (linha, coluna), dado um estado parcial do tabuleiro.

    - mínimo: assume que células DESCONHECIDAS podem ser pretas e bloqueiam
      a visão, então só conta as brancas garantidas até o primeiro desconhecido/preto.
    - máximo: assume que todas DESCONHECIDAS visíveis podem ser brancas.
    """
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)

    minimo = 1  # a própria célula (número) é branca
    maximo = 1

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dl, dc in direcoes:
        # mínimo
        l = linha + dl
        c = coluna + dc
        while 0 <= l < quantidade_linhas and 0 <= c < quantidade_colunas:
            estado = tabuleiro_estados[l][c]
            if estado == ESTADO_PRETO:
                break
            elif estado == ESTADO_BRANCO:
                minimo += 1
                l += dl
                c += dc
            else:  # DESCONHECIDO, não é garantido branco nem podemos ver além
                break

        # máximo
        l = linha + dl
        c = coluna + dc
        while 0 <= l < quantidade_linhas and 0 <= c < quantidade_colunas:
            estado = tabuleiro_estados[l][c]
            if estado == ESTADO_PRETO:
                break
            # branca ou desconhecida contam para o máximo
            maximo += 1
            l += dl
            c += dc

    return minimo, maximo


def ha_celulas_desconhecidas(tabuleiro_estados):
    for linha in tabuleiro_estados:
        for estado in linha:
            if estado == ESTADO_DESCONHECIDO:
                return True
    return False


def todas_celulas_brancas_conectadas(tabuleiro_estados):
    """
    Verifica se todas as células brancas formam um único componente conexo.
    (células numeradas são consideradas brancas pelo estado).
    """
    from collections import deque

    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)

    # Encontra uma célula branca qualquer para iniciar a busca
    linha_inicial = None
    coluna_inicial = None
    total_brancas = 0

    for i in range(quantidade_linhas):
        for j in range(quantidade_colunas):
            if tabuleiro_estados[i][j] == ESTADO_BRANCO:
                total_brancas += 1
                if linha_inicial is None:
                    linha_inicial, coluna_inicial = i, j

    if total_brancas == 0:
        # não deveria acontecer em Kuromasu válido, mas por segurança
        return False

    # BFS/DFS para contar brancas alcançáveis
    visitado = [[False] * quantidade_colunas for _ in range(quantidade_linhas)]
    fila = deque()
    fila.append((linha_inicial, coluna_inicial))
    visitado[linha_inicial][coluna_inicial] = True
    alcançadas = 0

    while fila:
        linha, coluna = fila.popleft()
        alcançadas += 1

        for nova_linha, nova_coluna in vizinhos_ortogonais(tabuleiro_estados, linha, coluna):
            if not visitado[nova_linha][nova_coluna] and tabuleiro_estados[nova_linha][nova_coluna] == ESTADO_BRANCO:
                visitado[nova_linha][nova_coluna] = True
                fila.append((nova_linha, nova_coluna))

    return alcançadas == total_brancas


def imprimir_tabuleiro(tabuleiro_numeros, tabuleiro_estados):
    """
    Imprime o tabuleiro de forma amigável:
    - números onde houver número
    - 'B' para preto
    - '.' para branco sem número
    """
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)

    for i in range(quantidade_linhas):
        linha_texto = []
        for j in range(quantidade_colunas):
            numero = tabuleiro_numeros[i][j]
            estado = tabuleiro_estados[i][j]

            if numero is not None:
                linha_texto.append(str(numero))
            else:
                if estado == ESTADO_PRETO:
                    linha_texto.append("B")
                elif estado == ESTADO_BRANCO:
                    linha_texto.append(".")
                else:
                    linha_texto.append("?")
        print(" ".join(linha_texto))
