from collections.abc import Iterable

from miniasyncio.linkedlist import CircularDoubleLL
import pytest

class TestCircularDoubleLL:
    ll: CircularDoubleLL[int] = CircularDoubleLL()

    def check_expected(self, expected: Iterable[int]):
        consumed_ll = tuple(node.val for node in self.ll)
        assert expected == consumed_ll

    def test_add_nodes(self):
        assert str(self.ll) == "LinkedList: "
        assert len(self.ll) == 0
        self.check_expected(())

        self.ll.add(2)
        self.ll.add(4)
        self.ll.add(10)

        assert str(self.ll) == "LinkedList: - [2] -- [4] -- [10] -"
        assert len(self.ll) == 3
        self.check_expected((2, 4, 10))

        self.ll.add(8)
        self.ll.add(10)
        self.ll.add("hehe")
        self.ll.add(67)

        assert str(self.ll) == "LinkedList: - [2] -- [4] -- [10] -- [8] -- [10] -- [hehe] -- [67] -"
        assert len(self.ll) == 7
        self.check_expected((2, 4, 10, 8, 10, 'hehe', 67))

    def test_rm_nodes(self):
        with pytest.raises(KeyError):
            self.ll.delete(3)

        with pytest.raises(KeyError):
            # A tuple is hashable so it could've been a key unlike a list
            self.ll.delete((2, 4))
        
        self.ll.delete([2, 4])

        self.ll.delete("hehe")

        self.check_expected((10, 8, 10, 67))
        assert len(self.ll) == 4
        assert str(self.ll) == "LinkedList: - [10] -- [8] -- [10] -- [67] -"

        self.ll.delete(10)
        self.check_expected((10, 8, 67))
        assert len(self.ll) == 3
        assert str(self.ll) == "LinkedList: - [10] -- [8] -- [67] -"
