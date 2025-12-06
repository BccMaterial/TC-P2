"""
Algoritmo de resolução de Kuromasu por busca com poda (backtracking).

- Garante:
  - intervalos de visibilidade compatíveis com os números
  - nenhuma dupla de células pretas adjacentes
  - ao final, conectividade de todas as células brancas
"""

from kuromasu_modelo import (
    ESTADO_DESCONHECIDO,
    ESTADO_BRANCO,
    ESTADO_PRETO,
    dimensoes,
    vizinhos_ortogonais,
    intervalo_visiveis,
    ha_celulas_desconhecidas,
    todas_celulas_brancas_conectadas,
    contar_visiveis,
)


def inicializar_estados(tabuleiro_numeros):
    """
    Cria a matriz de estados:
    - células numeradas começam como BRANCAS (fixas)
    - demais começam DESCONHECIDAS
    """
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_numeros)
    tabuleiro_estados = [[ESTADO_DESCONHECIDO] * quantidade_colunas for _ in range(quantidade_linhas)]
    posicoes_numeradas = []

    for i in range(quantidade_linhas):
        for j in range(quantidade_colunas):
            if tabuleiro_numeros[i][j] is not None:
                tabuleiro_estados[i][j] = ESTADO_BRANCO
                posicoes_numeradas.append((i, j))

    return tabuleiro_estados, posicoes_numeradas


def verificar_preto_nao_adjacente(tabuleiro_estados, linha, coluna):
    """
    Verifica se ao colocar uma célula PRETA em (linha, coluna)
    não criamos adjacência com outra célula PRETA.
    """
    for nova_linha, nova_coluna in vizinhos_ortogonais(tabuleiro_estados, linha, coluna):
        if tabuleiro_estados[nova_linha][nova_coluna] == ESTADO_PRETO:
            return False
    return True


def verificar_intervalos_numeros(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
    """
    Para cada célula numerada, verifica se o número ainda é possível
    dado o estado parcial (usando intervalo [mínimo, máximo]).
    """
    for linha, coluna in posicoes_numeradas:
        numero = tabuleiro_numeros[linha][coluna]
        minimo, maximo = intervalo_visiveis(tabuleiro_numeros, tabuleiro_estados, linha, coluna)
        if numero < minimo or numero > maximo:
            return False
    return True


def verificar_regras_finais(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
    """
    Quando todas as células estão decididas, checa:
    - cada número vê exatamente o total requerido
    - todas as brancas são conexas
    """
    # números batendo exatamente
    for linha, coluna in posicoes_numeradas:
        numero = tabuleiro_numeros[linha][coluna]
        visiveis = contar_visiveis(tabuleiro_numeros, tabuleiro_estados, linha, coluna)
        if visiveis != numero:
            return False

    # conectividade das células brancas
    if not todas_celulas_brancas_conectadas(tabuleiro_estados):
        return False

    return True


def escolher_proxima_celula(tabuleiro_numeros, tabuleiro_estados):
    """
    Estratégia simples: devolve a primeira célula DESCONHECIDA.
    """
    quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)
    for i in range(quantidade_linhas):
        for j in range(quantidade_colunas):
            if tabuleiro_estados[i][j] == ESTADO_DESCONHECIDO:
                return i, j
    return None, None  # não existe


def buscar_solucao(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
    """
    Backtracking recursivo que tenta preencher todas as células.
    Retorna True se encontrar solução (o tabuleiro_estados é modificado in-place).
    """
    if not ha_celulas_desconhecidas(tabuleiro_estados):
        # Todas as células foram definidas: checar regras finais
        return verificar_regras_finais(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas)

    linha, coluna = escolher_proxima_celula(tabuleiro_numeros, tabuleiro_estados)
    if linha is None:
        # Não deve acontecer por causa do teste acima, mas por segurança
        return False

    # Tenta colocar BRANCO e depois PRETO
    for estado_tentado in (ESTADO_BRANCO, ESTADO_PRETO):
        # Células numeradas não podem ser pretas
        if tabuleiro_numeros[linha][coluna] is not None and estado_tentado == ESTADO_PRETO:
            continue

        if estado_tentado == ESTADO_PRETO:
            if not verificar_preto_nao_adjacente(tabuleiro_estados, linha, coluna):
                continue

        tabuleiro_estados[linha][coluna] = estado_tentado

        # Poda com base nos intervalos dos números
        if verificar_intervalos_numeros(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
            if buscar_solucao(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
                return True

        # desfaz tentativa
        tabuleiro_estados[linha][coluna] = ESTADO_DESCONHECIDO

    return False


def resolver_kuromasu(tabuleiro_numeros):
    """
    Função de alto nível: recebe a matriz de números (None para sem número)
    e devolve a matriz de estados (BRANCO/PRETO) ou None se não houver solução.
    """
    tabuleiro_estados, posicoes_numeradas = inicializar_estados(tabuleiro_numeros)

    if buscar_solucao(tabuleiro_numeros, tabuleiro_estados, posicoes_numeradas):
        # devolve uma cópia para não vazar o objeto interno
        quantidade_linhas, quantidade_colunas = dimensoes(tabuleiro_estados)
        solucao = [[tabuleiro_estados[i][j] for j in range(quantidade_colunas)] for i in range(quantidade_linhas)]
        return solucao

    return None
