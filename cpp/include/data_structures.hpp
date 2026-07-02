#pragma once

#include <cstddef>
#include <deque>
#include <memory>
#include <optional>
#include <tuple>
#include <vector>

namespace simulator {

class Stack {
public:
    void push(int value);
    int pop();
    int top() const;
    [[nodiscard]] bool empty() const noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] int sum() const noexcept;
    int min_value() const;
    int max_value() const;
    [[nodiscard]] std::vector<int> values() const;
    void clear() noexcept;

private:
    std::vector<int> data_;
};

class Queue {
public:
    void enqueue(int value);
    int dequeue();
    int front() const;
    int back() const;
    [[nodiscard]] bool empty() const noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] int sum() const noexcept;
    int min_value() const;
    int max_value() const;
    [[nodiscard]] std::vector<int> values() const;
    void clear() noexcept;

private:
    std::deque<int> data_;
};

class SinglyLinkedList {
public:
    SinglyLinkedList() = default;
    ~SinglyLinkedList();

    SinglyLinkedList(const SinglyLinkedList&) = delete;
    SinglyLinkedList& operator=(const SinglyLinkedList&) = delete;
    SinglyLinkedList(SinglyLinkedList&&) = delete;
    SinglyLinkedList& operator=(SinglyLinkedList&&) = delete;

    void push_front(int value);
    void push_back(int value);
    void insert_at(std::size_t index, int value);
    int remove_at(std::size_t index);
    bool remove_first(int value);
    std::size_t remove_all(int value);
    int find(int value) const noexcept;
    void reverse() noexcept;
    [[nodiscard]] bool empty() const noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] int sum() const noexcept;
    [[nodiscard]] std::vector<int> values() const;
    void clear() noexcept;

private:
    struct Node {
        explicit Node(int node_value) : value(node_value) {}

        int value;
        Node* next{nullptr};
    };

    Node* head_{nullptr};
    std::size_t size_{0};

    Node* node_at(std::size_t index) const;
};

class BinarySearchTree {
public:
    using SnapshotNode = std::tuple<int, std::optional<int>, std::optional<int>>;

    BinarySearchTree() = default;
    ~BinarySearchTree() = default;

    BinarySearchTree(const BinarySearchTree&) = delete;
    BinarySearchTree& operator=(const BinarySearchTree&) = delete;
    BinarySearchTree(BinarySearchTree&&) = delete;
    BinarySearchTree& operator=(BinarySearchTree&&) = delete;

    bool insert(int value);
    bool remove(int value);
    [[nodiscard]] bool contains(int value) const noexcept;
    [[nodiscard]] bool empty() const noexcept;
    [[nodiscard]] std::size_t size() const noexcept;
    [[nodiscard]] int sum() const noexcept;
    [[nodiscard]] std::size_t leaf_count() const noexcept;
    [[nodiscard]] int height() const noexcept;
    [[nodiscard]] std::vector<int> inorder() const;
    [[nodiscard]] std::vector<int> preorder() const;
    [[nodiscard]] std::vector<int> postorder() const;
    [[nodiscard]] std::vector<int> level_order() const;
    [[nodiscard]] std::vector<SnapshotNode> snapshot() const;
    void clear() noexcept;

private:
    struct Node {
        explicit Node(int node_value) : value(node_value) {}

        int value;
        std::unique_ptr<Node> left{nullptr};
        std::unique_ptr<Node> right{nullptr};
    };

    std::unique_ptr<Node> root_{nullptr};
    std::size_t size_{0};

    static bool insert_node(std::unique_ptr<Node>& node, int value);
    static bool remove_node(std::unique_ptr<Node>& node, int value);
    static Node* min_node(Node* node) noexcept;
    static bool contains_node(const Node* node, int value) noexcept;
    static int sum_node(const Node* node) noexcept;
    static std::size_t leaf_count_node(const Node* node) noexcept;
    static int height_node(const Node* node) noexcept;
    static void inorder_node(const Node* node, std::vector<int>& output);
    static void preorder_node(const Node* node, std::vector<int>& output);
    static void postorder_node(const Node* node, std::vector<int>& output);
    static void snapshot_node(const Node* node, std::vector<SnapshotNode>& output);
};

}  // namespace simulator
