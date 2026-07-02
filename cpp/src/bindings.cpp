#include "data_structures.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(ds_core, module) {
    module.doc() = "Nucleo C++17 do simulador interativo de estruturas de dados.";

    py::class_<simulator::Stack>(module, "Stack")
        .def(py::init<>())
        .def("push", &simulator::Stack::push, py::arg("value"))
        .def("pop", &simulator::Stack::pop)
        .def("top", &simulator::Stack::top)
        .def("empty", &simulator::Stack::empty)
        .def("size", &simulator::Stack::size)
        .def("sum", &simulator::Stack::sum)
        .def("min_value", &simulator::Stack::min_value)
        .def("max_value", &simulator::Stack::max_value)
        .def("values", &simulator::Stack::values)
        .def("clear", &simulator::Stack::clear);

    py::class_<simulator::Queue>(module, "Queue")
        .def(py::init<>())
        .def("enqueue", &simulator::Queue::enqueue, py::arg("value"))
        .def("dequeue", &simulator::Queue::dequeue)
        .def("front", &simulator::Queue::front)
        .def("back", &simulator::Queue::back)
        .def("empty", &simulator::Queue::empty)
        .def("size", &simulator::Queue::size)
        .def("sum", &simulator::Queue::sum)
        .def("min_value", &simulator::Queue::min_value)
        .def("max_value", &simulator::Queue::max_value)
        .def("values", &simulator::Queue::values)
        .def("clear", &simulator::Queue::clear);

    py::class_<simulator::SinglyLinkedList>(module, "SinglyLinkedList")
        .def(py::init<>())
        .def("push_front", &simulator::SinglyLinkedList::push_front, py::arg("value"))
        .def("push_back", &simulator::SinglyLinkedList::push_back, py::arg("value"))
        .def("insert_at", &simulator::SinglyLinkedList::insert_at,
             py::arg("index"), py::arg("value"))
        .def("remove_at", &simulator::SinglyLinkedList::remove_at, py::arg("index"))
        .def("remove_first", &simulator::SinglyLinkedList::remove_first, py::arg("value"))
        .def("remove_all", &simulator::SinglyLinkedList::remove_all, py::arg("value"))
        .def("find", &simulator::SinglyLinkedList::find, py::arg("value"))
        .def("reverse", &simulator::SinglyLinkedList::reverse)
        .def("empty", &simulator::SinglyLinkedList::empty)
        .def("size", &simulator::SinglyLinkedList::size)
        .def("sum", &simulator::SinglyLinkedList::sum)
        .def("values", &simulator::SinglyLinkedList::values)
        .def("clear", &simulator::SinglyLinkedList::clear);

    py::class_<simulator::BinarySearchTree>(module, "BinarySearchTree")
        .def(py::init<>())
        .def("insert", &simulator::BinarySearchTree::insert, py::arg("value"))
        .def("remove", &simulator::BinarySearchTree::remove, py::arg("value"))
        .def("contains", &simulator::BinarySearchTree::contains, py::arg("value"))
        .def("empty", &simulator::BinarySearchTree::empty)
        .def("size", &simulator::BinarySearchTree::size)
        .def("sum", &simulator::BinarySearchTree::sum)
        .def("leaf_count", &simulator::BinarySearchTree::leaf_count)
        .def("height", &simulator::BinarySearchTree::height)
        .def("inorder", &simulator::BinarySearchTree::inorder)
        .def("preorder", &simulator::BinarySearchTree::preorder)
        .def("postorder", &simulator::BinarySearchTree::postorder)
        .def("level_order", &simulator::BinarySearchTree::level_order)
        .def("snapshot", &simulator::BinarySearchTree::snapshot)
        .def("clear", &simulator::BinarySearchTree::clear);
}
