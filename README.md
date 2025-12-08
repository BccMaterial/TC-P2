# O Quebra-cabeça Kuromasu (Kurodoko)

Projeto acadêmico que estuda o quebra-cabeça **Kuromasu (Kurodoko)**, sua
**complexidade computacional (NP-Completo)** e implementa um **resolvedor em Python**
usando busca com poda e heurística **MRV (Minimum Remaining Values)**.

---

## 🎯 Objetivos

- Modelar formalmente o problema do Kuromasu.
- Implementar um **algoritmo de resolução** baseado em backtracking com poda.
- Utilizar uma heurística de escolha de variável (MRV) para reduzir o espaço de busca.
- Relacionar o problema com a teoria da complexidade, mostrando que o problema de
  decisão de Kuromasu é **NP-Completo**.

---

## 🧩 Regras do Kuromasu (resumo)

Dado um tabuleiro retangular:

1. Algumas células possuem **números**.
2. Devemos colorir algumas células de **preto**, deixando as demais **brancas**.
3. Regras:
   - Células numeradas são sempre **brancas**.
   - Nenhuma célula preta pode ser ortogonalmente adjacente a outra preta.
   - Todas as células brancas devem formar **um único componente conexo**.
   - Cada número indica quantas células brancas são **visíveis** a partir dele
     (incluindo a própria célula), olhando nas 4 direções até encontrar um preto
     ou a borda do tabuleiro.

O problema de decisão é: **“dado um tabuleiro, existe alguma solução que satisfaça
todas as regras?”** — esse é o problema mostrado como **NP-Completo**.

---

## kuromasu_modelo.py – Modelo e regras

Contém as funções relacionadas ao modelo do tabuleiro e às regras do jogo:
  - Constantes:
    - ESTADO_DESCONHECIDO, ESTADO_BRANCO, ESTADO_PRETO
  - Funções utilitárias:
    - dimensoes, esta_dentro, vizinhos_ortogonais
  - Visibilidade:
    - contar_visiveis(...): conta quantas casas brancas um número vê (solução completa).
    - intervalo_visiveis(...): calcula um intervalo [mín, máx] de casas visíveis para cada número, dado um estado parcial (usado para poda).
  - Conectividade:
    - todas_celulas_brancas_conectadas(...): verifica se todas as brancas estão em um único componente conexo (BFS).
  - Utilitário:
    - imprimir_tabuleiro(...): imprime o tabuleiro com números, B para preto e . para branco sem número.
## kuromasu_resolvedor.py – Algoritmo de resolução
Implementa o backtracking com poda e a heurística MRV:
  - Inicialização:
    - inicializar_estados(...): cria a matriz de estados, marcando números como brancos e demais células como desconhecidas.
  - Regras locais:
    - verificar_preto_nao_adjacente(...): proíbe dois pretos adjacentes.
    - verificar_intervalos_numeros(...): checa se, para cada número, o valor desejado está dentro do intervalo [mín, máx] possível, dado o estado parcial.
  - Heurística MRV:
    - escolher_proxima_celula(...):
      - Para cada célula desconhecida, testa temporariamente:
        - se pode ser branca sem quebrar os intervalos de visibilidade;
        - se pode ser preta sem quebrar adjacência de pretos, nem os intervalos, nem pintar um número de preto.
      - Conta quantas opções são possíveis (0, 1 ou 2).
      - Se alguma célula tiver 0 opções, o estado atual é impossível → poda imediata.
      - Caso contrário, escolhe a célula com menor número de opções (mais restrita), aplicando a heurística MRV (Minimum Remaining Values).
  - Backtracking:
    - buscar_solucao(...): explora recursivamente as possibilidades (branco/preto), usando poda por regras e pelos intervalos.
    - verificar_regras_finais(...): na solução completa, confere números exatos e conectividade das brancas.
  - Função de alto nível:
    - resolver_kuromasu(tabuleiro_numeros): recebe uma matriz de pistas e retorna a matriz de estados (branco/preto) de uma solução, ou None se não houver.

## main.py – Ponto de entrada
 - Faz a leitura do tabuleiro, podendo:
   - Ler de um arquivo .txt (tabuleiro_kuromasu.txt), ou
   - Usar um tabuleiro de exemplo definido em código (se você quiser).
 - Chama:
   - resolver_kuromasu(...)
   - imprimir_tabuleiro(...)
 - Exibe:
   - “Solução encontrada:” + tabuleiro resolvido, ou
   - “Não foi encontrada solução para este tabuleiro.”

## tabuleiro_kuromasu.txt – Arquivo de entrada
Define um tabuleiro em texto, por exemplo:

```text
. . . 4 .
. . . . .
. 6 . . .
. . . . .
. . 3 . .
```
- Cada linha do arquivo = uma linha do tabuleiro.
- Valores separados por espaço:
  - . → célula sem número
  - um inteiro (ex.: 3, 10) → célula numerada

O main.py lê esse arquivo e converte para a matriz tabuleiro_numeros.

## 🔧 Requisitos
- Python 3.8+ (recomendado 3.10+)

## ▶️ Como executar
- Clone ou baixe o repositório.
- Execute o main
```text
cd src
python main.py
```


## 🧠 Complexidade e NP-Completo

O problema de decidir se um tabuleiro arbitrário de Kuromasu admite solução é
**NP-Completo**, provado via redução polinomial a partir do problema
**One-in-Three SAT**. Em alto nível:

- O problema está em **NP** porque:
  - Dada uma marcação de casas pretas/brancas (um **certificado**),
    podemos verificar **deterministicamente em tempo polinomial** se:
    - números são brancos;
    - não há pretos adjacentes;
    - as brancas formam um componente conexo;
    - cada número enxerga exatamente o valor indicado.
  - Esses passos formam um **verificador determinístico polinomial**.  
    Pela definição padrão de NP, isso é equivalente a dizer que existe uma
    **máquina de Turing não determinística** que decide o problema em tempo
    polinomial. Logo, o problema de decisão de Kuromasu pertence à classe NP.

- O problema é **NP-difícil** porque é possível codificar instâncias de
  One-in-Three SAT em tabuleiros de Kuromasu usando *gadgets* lógicos
  (fio, variável, XOR, choice, split, etc.) que preservam satisfatibilidade.

Como consequência, espera-se que **nenhum algoritmo determinístico polinomial**
exista para o problema em geral (a menos que P = NP).  
Nosso algoritmo de backtracking com poda e heurística MRV ainda tem
complexidade **exponencial no pior caso**, mas é bem mais eficiente na prática
para tabuleiros de tamanho moderado, justamente pelas podas e pela escolha
heurística da próxima célula (MRV).


## 👥 Integrantes
- Caio Collino
- Thiago Lins
- Vinicius Vianna
- Vinicius Miyata

  
