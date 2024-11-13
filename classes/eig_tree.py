class EIGTree:
    def __init__(self, process_num, val: int):
        self.__process_num = process_num
        self.__set_root(val=val)

    def get_process_num(self) -> int:
        return self.__process_num

    def __set_root(self, val: int):
        self.__root = Node(proc_id=self.__process_num, parent=None, depth=0, val=val, children=None)

    def get_messages(self):
        return self.__root.get_leaves_values()


class Node:
    def __init__(self, proc_id: int, parent, depth: int, children: list, val: int):
        self.__parent__ = parent
        self.__proc_id = proc_id
        self.__depth = depth
        self.__children = children
        self.__val = val

    def get_proc_id(self) -> int:
        return self.__proc_id

    def get_parent(self):
        return self.__parent__

    def get_depth(self) -> int:
        return self.__depth

    def is_leaf(self) -> bool:
        return self.__children is None

    def get_children(self) -> list:
        return self.__children

    def get_val(self) -> int:
        return self.__val

    def set_children(self, parents: list[int], proc_num: int):
        if self.__children is not None:
            for child in self.__children:
                child.set_children(parents=parents + [child], proc_num=proc_num)
        else:
            self.__children = [Node(proc_id=i, parent=self, depth=self.__depth + 1, children=None, value=None) for i in
                               range(proc_num) if i not in parents]

    def get_leaves_values(self, path:list[int]=[]) -> list[list[int], int]:
        if self.is_leaf():
            final_path = path + [self.__proc_id]
            return [final_path, self.__val]
        else:
            res = []
            new_path = path + [self.__proc_id]
            for child in self.__children:
                res = res + child.get_leaves_values(path=new_path.copy())
            return res