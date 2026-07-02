from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT_DIR / "build"
sys.path.insert(0, str(BUILD_DIR))

try:
    import ds_core
except ImportError as error:  # pragma: no cover
    raise RuntimeError("Compile o modulo C++ antes de executar os testes.") from error


def test_stack_lifo_and_statistics() -> None:
    stack = ds_core.Stack()
    stack.push(4)
    stack.push(-2)
    stack.push(9)

    assert stack.values() == [4, -2, 9]
    assert stack.top() == 9
    assert stack.pop() == 9
    assert stack.values() == [4, -2]
    assert stack.size() == 2
    assert stack.sum() == 2
    assert stack.min_value() == -2
    assert stack.max_value() == 4


def test_stack_empty_access_raises() -> None:
    stack = ds_core.Stack()
    with pytest.raises(RuntimeError):
        stack.pop()
    with pytest.raises(RuntimeError):
        stack.top()


def test_queue_fifo_and_statistics() -> None:
    queue = ds_core.Queue()
    for value in [7, 1, 5]:
        queue.enqueue(value)

    assert queue.values() == [7, 1, 5]
    assert queue.front() == 7
    assert queue.back() == 5
    assert queue.dequeue() == 7
    assert queue.values() == [1, 5]
    assert queue.size() == 2
    assert queue.sum() == 6
    assert queue.min_value() == 1
    assert queue.max_value() == 5


def test_linked_list_insertion_removal_and_reverse() -> None:
    linked_list = ds_core.SinglyLinkedList()
    linked_list.push_back(10)
    linked_list.push_front(5)
    linked_list.insert_at(1, 7)
    linked_list.push_back(7)

    assert linked_list.values() == [5, 7, 10, 7]
    assert linked_list.find(10) == 2
    assert linked_list.find(99) == -1
    assert linked_list.remove_first(7) is True
    assert linked_list.values() == [5, 10, 7]
    assert linked_list.remove_all(7) == 1
    assert linked_list.remove_at(0) == 5
    linked_list.reverse()
    assert linked_list.values() == [10]
    assert linked_list.sum() == 10


def test_linked_list_invalid_index_raises() -> None:
    linked_list = ds_core.SinglyLinkedList()
    with pytest.raises(IndexError):
        linked_list.insert_at(1, 4)
    with pytest.raises(IndexError):
        linked_list.remove_at(0)


def test_bst_operations_traversals_and_metrics() -> None:
    tree = ds_core.BinarySearchTree()
    for value in [8, 4, 12, 2, 6, 10, 14]:
        assert tree.insert(value) is True

    assert tree.insert(8) is False
    assert tree.contains(10) is True
    assert tree.contains(9) is False
    assert tree.inorder() == [2, 4, 6, 8, 10, 12, 14]
    assert tree.preorder() == [8, 4, 2, 6, 12, 10, 14]
    assert tree.postorder() == [2, 6, 4, 10, 14, 12, 8]
    assert tree.level_order() == [8, 4, 12, 2, 6, 10, 14]
    assert tree.size() == 7
    assert tree.sum() == 56
    assert tree.leaf_count() == 4
    assert tree.height() == 3

    assert tree.remove(8) is True
    assert tree.inorder() == [2, 4, 6, 10, 12, 14]
    assert tree.size() == 6
    assert tree.contains(8) is False
    assert tree.remove(99) is False


def test_bst_snapshot_exposes_relationships() -> None:
    tree = ds_core.BinarySearchTree()
    for value in [5, 3, 8]:
        tree.insert(value)

    snapshot = tree.snapshot()
    assert snapshot[0] == (5, 3, 8)
    assert snapshot[1] == (3, None, None)
    assert snapshot[2] == (8, None, None)
