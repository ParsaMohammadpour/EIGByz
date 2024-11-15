from typing import Self


class Node:
    def __init__(self, parent: Self, proc_uid: int, val: int, path: list[int]):
        self.__proc_uid = proc_uid
        self.__parent = parent
        self.__children = []
        self.__val = val
        self.__path = path.copy()
        self.__depth = len(path)
        self.__decision = None

    def get_proc_uid(self) -> int:
        return self.__proc_uid

    def get_parent(self) -> Self:
        return self.__parent

    def get_children(self) -> list[Self]:
        return self.__children

    def get_val(self) -> int:
        return self.__val

    def set_val(self, val: int):
        self.__val = val

    def get_path(self) -> list[int]:
        return self.__path.copy()

    def get_depth(self) -> int:
        return self.__depth

    def is_leaf(self) -> bool:
        return len(self.__children) == 0

    def is_root(self) -> bool:
        return self.__parent is None

    def add_child(self, child: Self):
        self.__children.append(child)

    def get_decision(self) -> int:
        return self.__decision

    def decide(self) -> int:
        if self.is_leaf():
            self.__decision = self.get_val()
        else:
            summation = sum(child.decide() for child in self.__children)
            half_child_count = len(self.__children) // 2
            self.__decision = 1 if summation > half_child_count else 0
        return self.__decision

    def __str__(self):
        correct_path = [str(p) for p in self.get_path()[1:]]
        path = ''.join(correct_path)
        if self.is_leaf():
            return f'path: {path}, val: {self.get_val()}'
        else:
            return f'path: {path}'

    def __repr__(self):
        return self.__str__()