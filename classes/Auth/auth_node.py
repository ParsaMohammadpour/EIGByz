from typing import Self


class AuthNode:
    def __init__(self, parent: Self, proc_uid: int, val: int, path: list[int], signed_val: bytes,
                 is_authed: bool = False):
        self.__proc_uid = proc_uid
        self.__parent = parent
        self.__children = []
        self.__val = val
        self.__path = path.copy()
        self.__depth = len(path)
        self.__decision = -1  # default value is -1, None is for the time that a node is not authenticated
        self.__is_authed = is_authed
        self.__signed_val = signed_val

    def get_signed_val(self) -> bytes:
        return self.__signed_val

    def set_signed_val(self, val: bytes | None):
        self.__signed_val = val

    def is_authed(self) -> bool:
        return self.__is_authed

    def set_is_authed(self, is_authed: bool):
        self.__is_authed = is_authed

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

    def set_decision(self, decision: int | None):
        self.__decision = decision

    def decide(self) -> int | None:
        if self.get_decision() != -1:  # we have decided for this node before
            return self.get_decision()
        if not self.is_authed():
            if not self.is_leaf():
                for child in self.get_children():
                    child.decide()
            self.set_decision(None)
        elif self.is_leaf():
            if self.get_val() is None:
                self.set_decision(0)
            else:
                self.set_decision(self.get_val())
        else:
            child_decision = [child.decide() for child in self.get_children() if
                              child.is_authed() and child.decide() is not None]
            summation = sum(child_decision)
            half_child_count = len(child_decision) // 2
            decision = 1 if summation > half_child_count else 0
            self.set_decision(decision)
        return self.get_decision()

    def __str__(self):
        correct_path = [str(p) for p in self.get_path()[1:]]
        path = ''.join(correct_path)
        if self.is_leaf():
            return f'path: {path}, val: {self.get_val()}, signed-val: {self.__signed_val[:5] if self.__signed_val is not None else None}'
        else:
            return f'path: {path}'

    def __repr__(self):
        return self.__str__()
