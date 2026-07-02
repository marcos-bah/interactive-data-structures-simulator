#include "data_structures.hpp"

#include <algorithm>
#include <queue>
#include <stdexcept>
#include <utility>

namespace simulator {

namespace {

void require_non_empty(bool condition, const char* message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

}  // namespace

void Stack::push(int value) {
    data_.push_back(value);
}

int Stack::pop() {
    require_non_empty(!data_.empty(), "A pilha esta vazia.");
    const int value = data_.back();
    data_.pop_back();
    return value;
}

int Stack::top() const {
    require_non_empty(!data_.empty(), "A pilha esta vazia.");
    return data_.back();
}

bool Stack::empty() const noexcept {
    return data_.empty();
}

std::size_t Stack::size() const noexcept {
    return data_.size();
}

int Stack::sum() const noexcept {
    int total = 0;
    for (const int value : data_) {
        total += value;
    }
    return total;
}

int Stack::min_value() const {
    require_non_empty(!data_.empty(), "A pilha esta vazia.");
    return *std::min_element(data_.begin(), data_.end());
}

int Stack::max_value() const {
    require_non_empty(!data_.empty(), "A pilha esta vazia.");
    return *std::max_element(data_.begin(), data_.end());
}

std::vector<int> Stack::values() const {
    return data_;
}

void Stack::clear() noexcept {
    data_.clear();
}

void Queue::enqueue(int value) {
    data_.push_back(value);
}

int Queue::dequeue() {
    require_non_empty(!data_.empty(), "A fila esta vazia.");
    const int value = data_.front();
    data_.pop_front();
    return value;
}

int Queue::front() const {
    require_non_empty(!data_.empty(), "A fila esta vazia.");
    return data_.front();
}

int Queue::back() const {
    require_non_empty(!data_.empty(), "A fila esta vazia.");
    return data_.back();
}

bool Queue::empty() const noexcept {
    return data_.empty();
}

std::size_t Queue::size() const noexcept {
    return data_.size();
}

int Queue::sum() const noexcept {
    int total = 0;
    for (const int value : data_) {
        total += value;
    }
    return total;
}

int Queue::min_value() const {
    require_non_empty(!data_.empty(), "A fila esta vazia.");
    return *std::min_element(data_.begin(), data_.end());
}

int Queue::max_value() const {
    require_non_empty(!data_.empty(), "A fila esta vazia.");
    return *std::max_element(data_.begin(), data_.end());
}

std::vector<int> Queue::values() const {
    return {data_.begin(), data_.end()};
}

void Queue::clear() noexcept {
    data_.clear();
}

SinglyLinkedList::~SinglyLinkedList() {
    clear();
}

void SinglyLinkedList::push_front(int value) {
    Node* node = new Node(value);
    node->next = head_;
    head_ = node;
    ++size_;
}

void SinglyLinkedList::push_back(int value) {
    Node* node = new Node(value);
    if (head_ == nullptr) {
        head_ = node;
        ++size_;
        return;
    }

    Node* current = head_;
    while (current->next != nullptr) {
        current = current->next;
    }

    current->next = node;
    ++size_;
}

void SinglyLinkedList::insert_at(std::size_t index, int value) {
    if (index > size_) {
        throw std::out_of_range("Indice de insercao fora dos limites da lista.");
    }

    if (index == 0) {
        push_front(value);
        return;
    }

    Node* previous = node_at(index - 1);
    Node* node = new Node(value);
    node->next = previous->next;
    previous->next = node;
    ++size_;
}

int SinglyLinkedList::remove_at(std::size_t index) {
    if (index >= size_) {
        throw std::out_of_range("Indice de remocao fora dos limites da lista.");
    }

    Node* removed = nullptr;
    if (index == 0) {
        removed = head_;
        head_ = head_->next;
    } else {
        Node* previous = node_at(index - 1);
        removed = previous->next;
        previous->next = removed->next;
    }

    const int value = removed->value;
    delete removed;
    --size_;
    return value;
}

bool SinglyLinkedList::remove_first(int value) {
    Node* previous = nullptr;
    Node* current = head_;

    while (current != nullptr) {
        if (current->value == value) {
            if (previous == nullptr) {
                head_ = current->next;
            } else {
                previous->next = current->next;
            }
            delete current;
            --size_;
            return true;
        }
        previous = current;
        current = current->next;
    }

    return false;
}

std::size_t SinglyLinkedList::remove_all(int value) {
    std::size_t removed_count = 0;
    while (head_ != nullptr && head_->value == value) {
        Node* removed = head_;
        head_ = head_->next;
        delete removed;
        --size_;
        ++removed_count;
    }

    Node* current = head_;
    while (current != nullptr && current->next != nullptr) {
        if (current->next->value == value) {
            Node* removed = current->next;
            current->next = removed->next;
            delete removed;
            --size_;
            ++removed_count;
        } else {
            current = current->next;
        }
    }

    return removed_count;
}

int SinglyLinkedList::find(int value) const noexcept {
    int index = 0;
    Node* current = head_;
    while (current != nullptr) {
        if (current->value == value) {
            return index;
        }
        current = current->next;
        ++index;
    }
    return -1;
}

void SinglyLinkedList::reverse() noexcept {
    Node* previous = nullptr;
    Node* current = head_;

    while (current != nullptr) {
        Node* next = current->next;
        current->next = previous;
        previous = current;
        current = next;
    }

    head_ = previous;
}

bool SinglyLinkedList::empty() const noexcept {
    return head_ == nullptr;
}

std::size_t SinglyLinkedList::size() const noexcept {
    return size_;
}

int SinglyLinkedList::sum() const noexcept {
    int total = 0;
    Node* current = head_;
    while (current != nullptr) {
        total += current->value;
        current = current->next;
    }
    return total;
}

std::vector<int> SinglyLinkedList::values() const {
    std::vector<int> output;
    output.reserve(size_);

    Node* current = head_;
    while (current != nullptr) {
        output.push_back(current->value);
        current = current->next;
    }

    return output;
}

void SinglyLinkedList::clear() noexcept {
    while (head_ != nullptr) {
        Node* removed = head_;
        head_ = head_->next;
        delete removed;
    }
    size_ = 0;
}

SinglyLinkedList::Node* SinglyLinkedList::node_at(std::size_t index) const {
    Node* current = head_;
    for (std::size_t position = 0; position < index; ++position) {
        current = current->next;
    }
    return current;
}

bool BinarySearchTree::insert(int value) {
    if (!insert_node(root_, value)) {
        return false;
    }
    ++size_;
    return true;
}

bool BinarySearchTree::remove(int value) {
    if (!remove_node(root_, value)) {
        return false;
    }
    --size_;
    return true;
}

bool BinarySearchTree::contains(int value) const noexcept {
    return contains_node(root_.get(), value);
}

bool BinarySearchTree::empty() const noexcept {
    return root_ == nullptr;
}

std::size_t BinarySearchTree::size() const noexcept {
    return size_;
}

int BinarySearchTree::sum() const noexcept {
    return sum_node(root_.get());
}

std::size_t BinarySearchTree::leaf_count() const noexcept {
    return leaf_count_node(root_.get());
}

int BinarySearchTree::height() const noexcept {
    return height_node(root_.get());
}

std::vector<int> BinarySearchTree::inorder() const {
    std::vector<int> output;
    output.reserve(size_);
    inorder_node(root_.get(), output);
    return output;
}

std::vector<int> BinarySearchTree::preorder() const {
    std::vector<int> output;
    output.reserve(size_);
    preorder_node(root_.get(), output);
    return output;
}

std::vector<int> BinarySearchTree::postorder() const {
    std::vector<int> output;
    output.reserve(size_);
    postorder_node(root_.get(), output);
    return output;
}

std::vector<int> BinarySearchTree::level_order() const {
    std::vector<int> output;
    if (root_ == nullptr) {
        return output;
    }

    std::queue<const Node*> pending;
    pending.push(root_.get());
    while (!pending.empty()) {
        const Node* current = pending.front();
        pending.pop();
        output.push_back(current->value);

        if (current->left != nullptr) {
            pending.push(current->left.get());
        }
        if (current->right != nullptr) {
            pending.push(current->right.get());
        }
    }

    return output;
}

std::vector<BinarySearchTree::SnapshotNode> BinarySearchTree::snapshot() const {
    std::vector<SnapshotNode> output;
    output.reserve(size_);
    snapshot_node(root_.get(), output);
    return output;
}

void BinarySearchTree::clear() noexcept {
    root_.reset();
    size_ = 0;
}

bool BinarySearchTree::insert_node(std::unique_ptr<Node>& node, int value) {
    if (node == nullptr) {
        node = std::make_unique<Node>(value);
        return true;
    }

    if (value == node->value) {
        return false;
    }

    if (value < node->value) {
        return insert_node(node->left, value);
    }

    return insert_node(node->right, value);
}

bool BinarySearchTree::remove_node(std::unique_ptr<Node>& node, int value) {
    if (node == nullptr) {
        return false;
    }

    if (value < node->value) {
        return remove_node(node->left, value);
    }

    if (value > node->value) {
        return remove_node(node->right, value);
    }

    if (node->left == nullptr) {
        node = std::move(node->right);
        return true;
    }

    if (node->right == nullptr) {
        node = std::move(node->left);
        return true;
    }

    Node* successor = min_node(node->right.get());
    node->value = successor->value;
    return remove_node(node->right, successor->value);
}

BinarySearchTree::Node* BinarySearchTree::min_node(Node* node) noexcept {
    while (node->left != nullptr) {
        node = node->left.get();
    }
    return node;
}

bool BinarySearchTree::contains_node(const Node* node, int value) noexcept {
    while (node != nullptr) {
        if (value == node->value) {
            return true;
        }
        node = value < node->value ? node->left.get() : node->right.get();
    }
    return false;
}

int BinarySearchTree::sum_node(const Node* node) noexcept {
    if (node == nullptr) {
        return 0;
    }
    return node->value + sum_node(node->left.get()) + sum_node(node->right.get());
}

std::size_t BinarySearchTree::leaf_count_node(const Node* node) noexcept {
    if (node == nullptr) {
        return 0;
    }
    if (node->left == nullptr && node->right == nullptr) {
        return 1;
    }
    return leaf_count_node(node->left.get()) + leaf_count_node(node->right.get());
}

int BinarySearchTree::height_node(const Node* node) noexcept {
    if (node == nullptr) {
        return 0;
    }
    return 1 + std::max(height_node(node->left.get()), height_node(node->right.get()));
}

void BinarySearchTree::inorder_node(const Node* node, std::vector<int>& output) {
    if (node == nullptr) {
        return;
    }
    inorder_node(node->left.get(), output);
    output.push_back(node->value);
    inorder_node(node->right.get(), output);
}

void BinarySearchTree::preorder_node(const Node* node, std::vector<int>& output) {
    if (node == nullptr) {
        return;
    }
    output.push_back(node->value);
    preorder_node(node->left.get(), output);
    preorder_node(node->right.get(), output);
}

void BinarySearchTree::postorder_node(const Node* node, std::vector<int>& output) {
    if (node == nullptr) {
        return;
    }
    postorder_node(node->left.get(), output);
    postorder_node(node->right.get(), output);
    output.push_back(node->value);
}

void BinarySearchTree::snapshot_node(const Node* node, std::vector<SnapshotNode>& output) {
    if (node == nullptr) {
        return;
    }

    const std::optional<int> left_value =
        node->left == nullptr ? std::nullopt : std::optional<int>{node->left->value};
    const std::optional<int> right_value =
        node->right == nullptr ? std::nullopt : std::optional<int>{node->right->value};

    output.emplace_back(node->value, left_value, right_value);
    snapshot_node(node->left.get(), output);
    snapshot_node(node->right.get(), output);
}

}  // namespace simulator
