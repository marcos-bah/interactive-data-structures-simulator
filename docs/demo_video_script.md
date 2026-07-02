# Roteiro de demonstracao em ate 3 minutos

## Preparacao

1. Abra a aplicacao no navegador pelo Codespaces.
2. Deixe a pagina inicial em `Pilha e Fila`.
3. Use valores pequenos para que as mudancas visuais sejam claras.

## Roteiro sugerido

### 0:00 a 0:20 - Abertura

Apresente o titulo do projeto, a disciplina PCO001 e a arquitetura: Streamlit no front-end, C++17 como nucleo das estruturas e Pybind11 como camada de integracao.

### 0:20 a 1:00 - Pilha

1. Selecione `Pilha`.
2. Execute `push(10)`, `push(20)` e `push(30)`.
3. Destaque que a estrutura cresce verticalmente e que push e pop ocorrem no topo.
4. Execute `pop` e mostre o valor removido, o tamanho, a soma, o menor e o maior valor.

### 1:00 a 1:35 - Fila

1. Selecione `Fila`.
2. Execute `enqueue(5)`, `enqueue(15)` e `enqueue(25)`.
3. Mostre que a insercao ocorre no fim e a remocao no inicio.
4. Execute `dequeue` e relacione a operacao com a politica FIFO.

### 1:35 a 2:10 - Lista simplesmente encadeada

1. Abra `Lista Encadeada`.
2. Insira 4 no inicio, 8 no fim e 6 no indice 1.
3. Mostre o `head`, as setas `next` e o ponteiro final para `nullptr`.
4. Execute uma busca por 6 e depois inverta a lista.

### 2:10 a 2:50 - Arvore binaria de busca

1. Abra `Arvore Binaria de Busca`.
2. Insira 8, 4, 12, 2, 6, 10 e 14.
3. Mostre a representacao grafica e os percursos em ordem, pre-ordem e pos-ordem.
4. Remova o no 8 para demonstrar a remocao de um no com dois filhos.

### 2:50 a 3:00 - Encerramento

Mostre o historico de operacoes e destaque que a aplicacao executa as operacoes e os calculos no modulo C++.
