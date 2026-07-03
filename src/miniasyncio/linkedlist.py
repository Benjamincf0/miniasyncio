from collections import defaultdict
from collections.abc import Generator
from typing import override


class ListNode[NodeType]:
    def __init__(self, val: NodeType):
        self.val: NodeType = val
        self.next: ListNode[NodeType] = self
        self.prev: ListNode[NodeType] = self

    @override
    def __str__(self):
        return f"[{self.val}]"


class CircularDoubleLL[NodeType]:
    def __init__(self):
        self._head: ListNode[NodeType]|None = None
        self._count: int = 0
        self._node_table: dict[NodeType,list[ListNode[NodeType]]] = defaultdict(list)

    def add(self, val: ListNode[NodeType]|NodeType):
        if isinstance(val, ListNode):
            newNode: ListNode[NodeType] = val
        else:
            newNode = ListNode(val)

        if self._head is None:
            self._head = newNode
            newNode.next = newNode
            newNode.prev = newNode
        else:
            newNode.next = self._head
            newNode.prev = self._head.prev
            newNode.prev.next = newNode
            newNode.next.prev = newNode
            self._head = newNode.next
        self._count += 1
        self._node_table[newNode.val].append(newNode)

    def _delete(self, val: ListNode[NodeType]|NodeType):
        node: ListNode[NodeType] 
        if isinstance(val, ListNode):
            node = val
        else:
            if val not in self._node_table or len(self._node_table[val]) == 0:
                raise KeyError
            node = self._node_table[val].pop()

        node.prev.next = node.next
        node.next.prev = node.prev
        if self._head is not None and self._head == node:
            self._head = self._head.next
        self._count -= 1
        if self._count == 0:
            self._head = None
        # no more refs to node? => garbage collected

    def delete(self, val: list[ListNode[NodeType]|NodeType]|ListNode[NodeType]|NodeType):
        if isinstance(val, list):
            errors = []
            for item in val:
                try:
                    self._delete(item)
                except Exception as e:
                    errors.append(e)

            for e in errors:
                raise e
        else:
            self._delete(val)

    def __iter__(self):
        if self._head is None:
            return None

        current_node: ListNode[NodeType] = self._head
        yield current_node

        while current_node.next != self._head:
            current_node = current_node.next
            yield current_node

    def iter_forever(self) -> Generator[NodeType, None, None]:
        if self._head is None:
            return None

        current_node: ListNode[NodeType] = self._head
        while self._count > 0:
            yield current_node.val
            current_node = current_node.next

    def __len__(self):
        return self._count

    @override
    def __str__(self):
        out = "LinkedList: "
        for node in self:
            out += f'- {str(node)} -'
        return out

