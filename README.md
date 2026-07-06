# Simulador Interativo de Estruturas de Dados

Aplicacao web educacional para a disciplina **PCO001 - Algoritmos e Estruturas de Dados**. O projeto apresenta simulacoes visuais de pilha, fila, lista simplesmente encadeada e arvore binaria de busca.

O front-end foi desenvolvido em Python com Streamlit. A logica, o armazenamento dos dados e os calculos das estruturas foram implementados em C++17. A integracao entre as duas camadas ocorre por bindings Pybind11.

## Funcionalidades

| Estrutura | Operacoes | Visualizacao |
|---|---|---|
| Pilha | push, pop, topo, tamanho, somatorio, menor, maior, limpar | Crescimento vertical e indicacao do topo |
| Fila | enqueue, dequeue, inicio, fim, tamanho, somatorio, menor, maior, limpar | Organizacao horizontal, com inicio e fim destacados |
| Lista simplesmente encadeada | inserir no inicio, fim ou indice, remover, buscar, remover todas as ocorrencias, inverter, somar, limpar | Nos conectados por setas, `head` e `nullptr` |
| Arvore binaria de busca | inserir, remover, buscar, percursos, altura, folhas, somatorio, limpeza | Diagrama da arvore e percursos em ordem, pre-ordem, pos-ordem e por nivel |

## Arquitetura

```text
+----------------------------+
|  Interface Streamlit       |
|  app.py                    |
+-------------+--------------+
              |
              | chamadas Python
              v
+----------------------------+
|  Bindings Pybind11         |
|  cpp/src/bindings.cpp      |
+-------------+--------------+
              |
              | chamadas C++
              v
+----------------------------+
|  Estruturas C++17          |
|  Pilha, fila, lista e BST  |
+----------------------------+
```

A interface nao reimplementa as estruturas em Python. Cada insercao, remocao, busca, percurso e calculo de medida e executado pelo modulo compilado `ds_core` em C++.

## Estrutura de diretorios

```text
interactive-data-structures-simulator/
├── app.py                         # Interface Streamlit
├── CMakeLists.txt                 # Compilacao do modulo C++
├── requirements.txt               # Dependencias Python
├── cpp/
│   ├── include/data_structures.hpp
│   └── src/
│       ├── data_structures.cpp     # Implementacoes C++17
│       └── bindings.cpp            # Bindings Pybind11
├── tests/test_core.py              # Testes automatizados
├── scripts/
│   ├── build.sh                    # Compila o modulo C++
│   └── run.sh                      # Compila se necessario e inicia Streamlit                
└── .devcontainer/                  # Configuracao para GitHub Codespaces
```

## Execucao manual em Linux ou macOS

### 1. Criar e ativar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Compilar o modulo C++

```bash
bash scripts/build.sh
```

### 4. Iniciar a aplicacao

```bash
streamlit run app.py
```

A aplicacao sera disponibilizada, por padrao, em `http://localhost:8501`.

## Testes automatizados

Apos compilar o modulo C++, execute:

```bash
pytest -q
```

Os testes abrangem comportamento LIFO da pilha, FIFO da fila, insercao e remocao em lista encadeada, percursos e remocao na arvore binaria de busca.

## Requisitos tecnicos

- Python 3.10 ou superior
- Compilador C++ com suporte a C++17, como GCC ou Clang
- CMake 3.20 ou superior
- Dependencias Python em `requirements.txt`


