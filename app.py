from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Callable, Iterable

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
BUILD_DIR = ROOT_DIR / "build"
if str(BUILD_DIR) not in sys.path:
    sys.path.insert(0, str(BUILD_DIR))

try:
    import ds_core
except ImportError as error:
    st.set_page_config(page_title="Simulador de Estruturas de Dados", layout="wide")
    st.error("O modulo C++ ainda nao foi compilado.")
    st.code("bash scripts/build.sh\nstreamlit run app.py", language="bash")
    st.caption(f"Detalhe tecnico: {error}")
    st.stop()


st.set_page_config(
    page_title="Simulador de Estruturas de Dados",
    page_icon="DS",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 1320px;
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
    }
    .hero {
        padding: 1.45rem 1.6rem;
        border: 1px solid #D8E2F2;
        border-radius: 18px;
        background: linear-gradient(135deg, #F8FBFF 0%, #EEF5FF 100%);
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        color: #0F2A4A;
        font-size: 2rem;
        margin: 0 0 0.3rem 0;
    }
    .hero p {
        color: #475569;
        margin: 0;
        font-size: 1rem;
    }
    .badge {
        display: inline-block;
        font-size: 0.76rem;
        font-weight: 700;
        color: #1D4ED8;
        background: #DBEAFE;
        padding: 0.22rem 0.58rem;
        border-radius: 999px;
        margin-bottom: 0.55rem;
        letter-spacing: 0.02em;
    }
    .visual-shell {
        border: 1px solid #D8E2F2;
        border-radius: 16px;
        padding: 1rem;
        background: #FFFFFF;
        min-height: 230px;
        overflow-x: auto;
    }
    .visual-title {
        color: #334155;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    .stack-visual {
        display: flex;
        min-height: 170px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.35rem;
    }
    .stack-marker {
        width: 170px;
        text-align: center;
        border-radius: 8px;
        background: #E8F0FE;
        color: #1E40AF;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.35rem 0.6rem;
    }
    .stack-column {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        align-items: center;
    }
    .stack-node, .queue-node {
        min-width: 74px;
        padding: 0.62rem 0.8rem;
        text-align: center;
        font-weight: 700;
        color: #0F172A;
        background: #EFF6FF;
        border: 1px solid #93C5FD;
        border-radius: 10px;
    }
    .recent-node {
        color: #14532D;
        background: #DCFCE7;
        border-color: #86EFAC;
    }
    .empty-node {
        color: #64748B;
        border: 1px dashed #94A3B8;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
    }
    .queue-visual {
        min-height: 170px;
        display: flex;
        gap: 0.55rem;
        align-items: center;
        justify-content: center;
        min-width: max-content;
    }
    .queue-marker {
        min-width: 112px;
        padding: 0.55rem;
        text-align: center;
        border-radius: 10px;
        background: #E8F0FE;
        color: #1E40AF;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .queue-marker span {
        display: block;
        color: #475569;
        font-size: 0.72rem;
        font-weight: 500;
        margin-top: 0.15rem;
    }
    .queue-arrow {
        color: #64748B;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .operation-log {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        background: #FBFDFF;
        padding: 0.75rem 0.95rem;
        font-size: 0.9rem;
        color: #334155;
    }
    .operation-log ul {
        margin: 0.35rem 0 0 1.1rem;
        padding: 0;
    }
    .operation-log li {
        margin-bottom: 0.25rem;
    }
    .architecture-card {
        border-left: 4px solid #2563EB;
        background: #F8FBFF;
        border-radius: 0 10px 10px 0;
        padding: 0.85rem 0.95rem;
        color: #334155;
        font-size: 0.9rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def initialize_session() -> None:
    defaults = {
        "stack": ds_core.Stack,
        "queue": ds_core.Queue,
        "linked_list": ds_core.SinglyLinkedList,
        "bst": ds_core.BinarySearchTree,
    }
    for key, constructor in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = constructor()

    if "operation_log" not in st.session_state:
        st.session_state.operation_log = []
    if "last_action" not in st.session_state:
        st.session_state.last_action = {
            "stack": "Nenhuma operacao executada.",
            "queue": "Nenhuma operacao executada.",
            "list": "Nenhuma operacao executada.",
            "bst": "Nenhuma operacao executada.",
        }


def reset_all_structures() -> None:
    st.session_state.stack = ds_core.Stack()
    st.session_state.queue = ds_core.Queue()
    st.session_state.linked_list = ds_core.SinglyLinkedList()
    st.session_state.bst = ds_core.BinarySearchTree()
    st.session_state.operation_log = []
    for structure in st.session_state.last_action:
        st.session_state.last_action[structure] = "Estrutura reiniciada."


def register_operation(structure: str, message: str) -> None:
    st.session_state.last_action[structure] = message
    st.session_state.operation_log.insert(0, f"{structure.upper()}: {message}")
    st.session_state.operation_log = st.session_state.operation_log[:12]


def execute_operation(
    structure: str,
    success_message: str,
    operation: Callable[[], object],
) -> object | None:
    try:
        result = operation()
        register_operation(structure, success_message)
        st.success(success_message)
        return result
    except (RuntimeError, IndexError, ValueError, OverflowError) as error:
        st.error(str(error))
        return None


def metrics_row(metrics: Iterable[tuple[str, str | int]]) -> None:
    metrics_list = list(metrics)
    columns = st.columns(len(metrics_list))
    for column, (label, value) in zip(columns, metrics_list):
        column.metric(label, value)


def render_operation_log() -> None:
    entries = st.session_state.operation_log
    if not entries:
        body = "<span>Nenhuma operacao registrada nesta sessao.</span>"
    else:
        items = "".join(f"<li>{html.escape(entry)}</li>" for entry in entries)
        body = f"<strong>Historico recente</strong><ul>{items}</ul>"
    st.markdown(f"<div class='operation-log'>{body}</div>", unsafe_allow_html=True)


def render_stack(values: list[int]) -> None:
    stack_nodes: list[str] = []
    for index, value in enumerate(reversed(values)):
        recent = " recent-node" if index == 0 and values else ""
        stack_nodes.append(
            f"<div class='stack-node{recent}'>{html.escape(str(value))}</div>"
        )

    body = "".join(stack_nodes) if stack_nodes else "<div class='empty-node'>Pilha vazia</div>"
    st.markdown(
        "<div class='visual-shell'>"
        "<div class='visual-title'>Representacao vertical, da base para o topo</div>"
        "<div class='stack-visual'>"
        "<div class='stack-marker'>TOPO: push / pop</div>"
        f"<div class='stack-column'>{body}</div>"
        "<div class='stack-marker'>BASE</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )


def render_queue(values: list[int]) -> None:
    elements: list[str] = [
        "<div class='queue-marker'>INICIO<span>dequeue</span></div>",
        "<div class='queue-arrow'>→</div>",
    ]
    if values:
        for index, value in enumerate(values):
            recent = " recent-node" if index == len(values) - 1 else ""
            elements.append(
                f"<div class='queue-node{recent}'>{html.escape(str(value))}</div>"
            )
            elements.append("<div class='queue-arrow'>→</div>")
    else:
        elements.append("<div class='empty-node'>Fila vazia</div>")
        elements.append("<div class='queue-arrow'>→</div>")
    elements.append("<div class='queue-marker'>FIM<span>enqueue</span></div>")

    st.markdown(
        "<div class='visual-shell'>"
        "<div class='visual-title'>Representacao horizontal, inicio a esquerda e fim a direita</div>"
        f"<div class='queue-visual'>{''.join(elements)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_linked_list(values: list[int]) -> None:
    lines = [
        "digraph LinkedList {",
        "rankdir=LR;",
        "bgcolor=\"transparent\";",
        "node [fontname=\"Arial\"];",
        "edge [color=\"#64748B\", penwidth=1.6];",
        "head [shape=plaintext, label=\"head\", fontcolor=\"#1E40AF\"] ;",
        "null [shape=plaintext, label=\"nullptr\", fontcolor=\"#64748B\"] ;",
    ]

    if not values:
        lines.append("head -> null;")
    else:
        for index, value in enumerate(values):
            lines.append(
                f"node_{index} [shape=box, style=\"rounded,filled\", "
                f"fillcolor=\"#EFF6FF\", color=\"#60A5FA\", label=\"{value}\"] ;"
            )
        lines.append("head -> node_0;")
        for index in range(len(values) - 1):
            lines.append(f"node_{index} -> node_{index + 1};")
        lines.append(f"node_{len(values) - 1} -> null;")

    lines.append("}")
    st.graphviz_chart("\n".join(lines), width="stretch")


def render_bst(snapshot: list[tuple[int, int | None, int | None]]) -> None:
    if not snapshot:
        st.info("A arvore esta vazia. Insira valores inteiros para criar os nos.")
        return

    node_ids = {value: f"node_{index}" for index, (value, _, _) in enumerate(snapshot)}
    lines = [
        "digraph BST {",
        "rankdir=TB;",
        "bgcolor=\"transparent\";",
        "node [shape=circle, style=filled, fontname=\"Arial\", fillcolor=\"#EFF6FF\", color=\"#3B82F6\", penwidth=1.5];",
        "edge [color=\"#64748B\", penwidth=1.6];",
    ]

    for value, _, _ in snapshot:
        lines.append(f"{node_ids[value]} [label=\"{value}\"];")

    for value, left, right in snapshot:
        if left is not None:
            lines.append(f"{node_ids[value]} -> {node_ids[left]};")
        if right is not None:
            lines.append(f"{node_ids[value]} -> {node_ids[right]};")

    lines.append("}")
    st.graphviz_chart("\n".join(lines), width="stretch")


def page_intro(title: str, subtitle: str, structure_key: str | None = None) -> None:
    st.markdown(
        "<div class='hero'>"
        f"<div class='badge'>PCO001 | NUCLEO C++17</div>"
        f"<h1>{html.escape(title)}</h1>"
        f"<p>{html.escape(subtitle)}</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    if structure_key is not None:
        st.caption(f"Ultima operacao: {st.session_state.last_action[structure_key]}")


def show_stack_and_queue() -> None:
    page_intro(
        "Pilha e Fila",
        "Compare duas estruturas lineares com politicas de acesso distintas.",
    )
    selected = st.radio(
        "Escolha a estrutura ativa",
        ["Pilha", "Fila"],
        horizontal=True,
        help="A pilha segue LIFO. A fila segue FIFO.",
    )

    active_key = "stack" if selected == "Pilha" else "queue"
    st.caption(f"Ultima operacao na estrutura ativa: {st.session_state.last_action[active_key]}")

    if selected == "Pilha":
        stack = st.session_state.stack
        values = list(stack.values())
        top_value = stack.top() if not stack.empty() else "vazia"
        min_value = stack.min_value() if not stack.empty() else "-"
        max_value = stack.max_value() if not stack.empty() else "-"

        left, right = st.columns([1.05, 1.95], gap="large")
        with left:
            st.subheader("Operacoes")
            with st.form("stack_push_form", clear_on_submit=True):
                value = st.number_input("Valor para push", value=0, step=1, key="stack_push_value")
                submitted = st.form_submit_button("Executar push", width="stretch")
            if submitted:
                execute_operation("stack", f"push({int(value)}) executado no topo.", lambda: stack.push(int(value)))

            first, second, third = st.columns(3)
            if first.button("Pop", width="stretch", key="stack_pop"):
                removed = execute_operation("stack", "pop executado no topo.", stack.pop)
                if removed is not None:
                    st.caption(f"Valor removido: {removed}")
            if second.button("Topo", width="stretch", key="stack_top"):
                result = execute_operation("stack", "Consulta do topo executada.", stack.top)
                if result is not None:
                    st.caption(f"Topo atual: {result}")
            if third.button("Limpar", width="stretch", key="stack_clear"):
                execute_operation("stack", "Pilha limpa.", stack.clear)

            st.markdown("#### Medidas calculadas no C++")
            metrics_row(
                [
                    ("Tamanho", stack.size()),
                    ("Somatorio", stack.sum()),
                    ("Menor", min_value),
                    ("Maior", max_value),
                ]
            )
            st.caption(f"Topo atual: {top_value}")
            with st.expander("Semantica da pilha"):
                st.write(
                    "A pilha utiliza a politica LIFO. O ultimo elemento inserido e o primeiro a ser removido. "
                    "Neste simulador, push e pop sempre ocorrem no topo."
                )

        with right:
            st.subheader("Estado atual")
            render_stack(values)

    else:
        queue = st.session_state.queue
        values = list(queue.values())
        front_value = queue.front() if not queue.empty() else "vazia"
        back_value = queue.back() if not queue.empty() else "vazia"
        min_value = queue.min_value() if not queue.empty() else "-"
        max_value = queue.max_value() if not queue.empty() else "-"

        left, right = st.columns([1.05, 1.95], gap="large")
        with left:
            st.subheader("Operacoes")
            with st.form("queue_enqueue_form", clear_on_submit=True):
                value = st.number_input("Valor para enqueue", value=0, step=1, key="queue_enqueue_value")
                submitted = st.form_submit_button("Executar enqueue", width="stretch")
            if submitted:
                execute_operation("queue", f"enqueue({int(value)}) executado no fim.", lambda: queue.enqueue(int(value)))

            first, second, third = st.columns(3)
            if first.button("Dequeue", width="stretch", key="queue_dequeue"):
                removed = execute_operation("queue", "dequeue executado no inicio.", queue.dequeue)
                if removed is not None:
                    st.caption(f"Valor removido: {removed}")
            if second.button("Extremos", width="stretch", key="queue_extremes"):
                result = execute_operation(
                    "queue", "Consulta de inicio e fim executada.", lambda: (queue.front(), queue.back())
                )
                if result is not None:
                    st.caption(f"Inicio: {result[0]} | Fim: {result[1]}")
            if third.button("Limpar", width="stretch", key="queue_clear"):
                execute_operation("queue", "Fila limpa.", queue.clear)

            st.markdown("#### Medidas calculadas no C++")
            metrics_row(
                [
                    ("Tamanho", queue.size()),
                    ("Somatorio", queue.sum()),
                    ("Menor", min_value),
                    ("Maior", max_value),
                ]
            )
            st.caption(f"Inicio atual: {front_value} | Fim atual: {back_value}")
            with st.expander("Semantica da fila"):
                st.write(
                    "A fila utiliza a politica FIFO. O primeiro elemento inserido e o primeiro a ser removido. "
                    "Neste simulador, enqueue ocorre no fim e dequeue ocorre no inicio."
                )

        with right:
            st.subheader("Estado atual")
            render_queue(values)


def show_linked_list() -> None:
    page_intro(
        "Lista Simplesmente Encadeada",
        "Cada no armazena um valor e uma referencia para o proximo no.",
        "list",
    )
    linked_list = st.session_state.linked_list

    controls, visualization = st.columns([1.05, 1.95], gap="large")
    with controls:
        insertion_tab, removal_tab, auxiliary_tab = st.tabs(["Insercao", "Remocao e busca", "Operacoes auxiliares"])

        with insertion_tab:
            with st.form("list_insert_form", clear_on_submit=True):
                mode = st.selectbox("Modo de insercao", ["Inicio", "Fim", "Indice"])
                value = st.number_input("Valor", value=0, step=1, key="list_insert_value")
                index = st.number_input(
                    "Indice", min_value=0, value=0, step=1, key="list_insert_index",
                    help="Use um indice entre 0 e o tamanho atual da lista.",
                )
                submitted = st.form_submit_button("Inserir", width="stretch")
            if submitted:
                if mode == "Inicio":
                    execute_operation(
                        "list", f"Insercao de {int(value)} no inicio.", lambda: linked_list.push_front(int(value))
                    )
                elif mode == "Fim":
                    execute_operation(
                        "list", f"Insercao de {int(value)} no fim.", lambda: linked_list.push_back(int(value))
                    )
                else:
                    execute_operation(
                        "list", f"Insercao de {int(value)} no indice {int(index)}.",
                        lambda: linked_list.insert_at(int(index), int(value)),
                    )

        with removal_tab:
            with st.form("list_remove_form", clear_on_submit=True):
                mode = st.selectbox(
                    "Modo de remocao",
                    ["Primeira ocorrencia", "Por indice", "Todas as ocorrencias"],
                )
                value = st.number_input("Valor para remocao", value=0, step=1, key="list_remove_value")
                index = st.number_input("Indice para remocao", min_value=0, value=0, step=1, key="list_remove_index")
                submitted = st.form_submit_button("Remover", width="stretch")
            if submitted:
                if mode == "Primeira ocorrencia":
                    removed = execute_operation(
                        "list", f"Busca e remocao da primeira ocorrencia de {int(value)}.",
                        lambda: linked_list.remove_first(int(value)),
                    )
                    if removed is False:
                        st.warning("O valor nao foi encontrado na lista.")
                elif mode == "Por indice":
                    removed = execute_operation(
                        "list", f"Remocao do indice {int(index)}.", lambda: linked_list.remove_at(int(index))
                    )
                    if removed is not None:
                        st.caption(f"Valor removido: {removed}")
                else:
                    count = execute_operation(
                        "list", f"Remocao de todas as ocorrencias de {int(value)}.",
                        lambda: linked_list.remove_all(int(value)),
                    )
                    if count is not None:
                        st.caption(f"Ocorrencias removidas: {count}")

            with st.form("list_search_form", clear_on_submit=True):
                value = st.number_input("Valor para busca", value=0, step=1, key="list_search_value")
                searched = st.form_submit_button("Buscar", width="stretch")
            if searched:
                position = execute_operation(
                    "list", f"Busca de {int(value)} executada.", lambda: linked_list.find(int(value))
                )
                if position is not None:
                    if position >= 0:
                        st.success(f"Valor encontrado no indice {position}.")
                    else:
                        st.info("Valor nao encontrado.")

        with auxiliary_tab:
            first, second = st.columns(2)
            if first.button("Inverter lista", width="stretch", key="list_reverse"):
                execute_operation("list", "Lista invertida.", linked_list.reverse)
            if second.button("Limpar", width="stretch", key="list_clear"):
                execute_operation("list", "Lista limpa.", linked_list.clear)
            st.caption("A soma e o tamanho abaixo sao obtidos diretamente da estrutura em C++.")

        st.markdown("#### Medidas calculadas no C++")
        metrics_row(
            [
                ("Tamanho", linked_list.size()),
                ("Somatorio", linked_list.sum()),
            ]
        )
        st.caption("Indice inicial: 0. O ultimo no aponta para nullptr.")

    with visualization:
        st.subheader("Encadeamento atual")
        render_linked_list(list(linked_list.values()))
        st.caption("As setas representam os ponteiros next. O ultimo no aponta explicitamente para nullptr.")


def show_bst() -> None:
    page_intro(
        "Arvore Binaria de Busca",
        "A ordenacao local e mantida em cada no: menores a esquerda e maiores a direita.",
        "bst",
    )
    bst = st.session_state.bst

    controls, visualization = st.columns([1.05, 1.95], gap="large")
    with controls:
        with st.form("bst_insert_form", clear_on_submit=True):
            value = st.number_input("Valor para insercao", value=0, step=1, key="bst_insert_value")
            inserted = st.form_submit_button("Inserir no", width="stretch")
        if inserted:
            result = execute_operation("bst", f"Tentativa de insercao de {int(value)}.", lambda: bst.insert(int(value)))
            if result is True:
                st.success(f"No {int(value)} inserido com sucesso.")
            elif result is False:
                st.warning("Valores duplicados nao sao inseridos na arvore.")

        first, second = st.columns(2)
        with first:
            with st.form("bst_remove_form", clear_on_submit=True):
                value = st.number_input("Valor para remocao", value=0, step=1, key="bst_remove_value")
                removed = st.form_submit_button("Remover", width="stretch")
            if removed:
                result = execute_operation("bst", f"Tentativa de remocao de {int(value)}.", lambda: bst.remove(int(value)))
                if result is True:
                    st.success(f"No {int(value)} removido com sucesso.")
                elif result is False:
                    st.warning("O valor informado nao esta na arvore.")
        with second:
            with st.form("bst_search_form", clear_on_submit=True):
                value = st.number_input("Valor para busca", value=0, step=1, key="bst_search_value")
                searched = st.form_submit_button("Buscar", width="stretch")
            if searched:
                found = execute_operation("bst", f"Busca de {int(value)} executada.", lambda: bst.contains(int(value)))
                if found is True:
                    st.success("No encontrado na arvore.")
                elif found is False:
                    st.info("No nao encontrado na arvore.")

        if st.button("Limpar arvore", width="stretch", key="bst_clear"):
            execute_operation("bst", "Arvore limpa.", bst.clear)

        st.markdown("#### Medidas calculadas no C++")
        metrics_row(
            [
                ("Nos", bst.size()),
                ("Soma", bst.sum()),
                ("Folhas", bst.leaf_count()),
                ("Altura", bst.height()),
            ]
        )
        st.caption("Altura: numero de nos no caminho mais longo. Arvore vazia tem altura 0.")

    with visualization:
        st.subheader("Estrutura atual")
        render_bst(list(bst.snapshot()))

    st.subheader("Percursos classicos")
    traversal_tab, preorder_tab, postorder_tab, level_tab = st.tabs(
        ["Em ordem", "Pre-ordem", "Pos-ordem", "Por nivel"]
    )
    with traversal_tab:
        st.code(" -> ".join(map(str, bst.inorder())) or "Arvore vazia", language=None)
        st.caption("Em uma arvore binaria de busca, o percurso em ordem apresenta os valores em ordem crescente.")
    with preorder_tab:
        st.code(" -> ".join(map(str, bst.preorder())) or "Arvore vazia", language=None)
    with postorder_tab:
        st.code(" -> ".join(map(str, bst.postorder())) or "Arvore vazia", language=None)
    with level_tab:
        st.code(" -> ".join(map(str, bst.level_order())) or "Arvore vazia", language=None)


def main() -> None:
    initialize_session()

    with st.sidebar:
        st.title("Navegacao")
        page = st.radio(
            "Estrutura a visualizar",
            ["Pilha e Fila", "Lista Encadeada", "Arvore Binaria de Busca"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown(
            "<div class='architecture-card'><strong>Arquitetura</strong><br>"
            "Interface em Streamlit, operacoes e estado em C++17, integrados por Pybind11."
            "</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Reiniciar todas as estruturas", width="stretch"):
            reset_all_structures()
            st.success("Todas as estruturas foram reiniciadas.")
        st.divider()
        st.caption("Disciplina PCO001 - Algoritmos e Estruturas de Dados")

    if page == "Pilha e Fila":
        show_stack_and_queue()
    elif page == "Lista Encadeada":
        show_linked_list()
    else:
        show_bst()

    st.divider()
    render_operation_log()
    st.caption("Projeto educacional. Toda mutacao de estrutura e todo calculo de medidas sao executados pelo modulo C++.")


if __name__ == "__main__":
    main()
