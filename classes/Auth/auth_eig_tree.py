import matplotlib.pyplot as plt
import networkx as nx
import os

from classes.Auth.auth_message import AuthMessage, AuthMessageContent
from classes.Auth.auth_node import AuthNode
from external.plot_tree import hierarchy_pos


def save_plot(path):
    generate_file(path)
    plt.savefig(path)


def generate_file(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


class AuthEIGByzTree:
    def __init__(self, proc_uid: int, proc_count: int, proc_val: int):
        self.__proc_uid = proc_uid
        self.__proc_count = proc_count
        self.__root = AuthNode(parent=None, proc_uid=-1, val=proc_val, path=[], is_authed=True, signed_val=None)
        self.__decision = None

    def get_proc_uid(self) -> int:
        return self.__proc_uid

    def get_proc_count(self) -> int:
        return self.__proc_count

    def get_decision(self) -> int:
        return self.__decision

    def get_root(self) -> AuthNode:
        return self.__root

    def add_level(self):
        if self.get_root().is_leaf():
            for i in range(1, self.get_proc_count() + 1):
                child = AuthNode(parent=self.get_root(), proc_uid=i, val=None, path=[-1, i], is_authed=False,
                                 signed_val=None)
                self.get_root().add_child(child)
        else:
            for child in self.get_root().get_children():
                self.__add_level_non_root(node=child)

    def __add_level_non_root(self, node: AuthNode):
        if node.is_leaf():
            for i in range(1, self.get_proc_count() + 1):
                if i not in node.get_path():
                    new_path = node.get_path() + [i]
                    child = AuthNode(parent=node, proc_uid=i, val=None, path=new_path, is_authed=False, signed_val=None)
                    node.add_child(child)
        else:
            for child in node.get_children():
                self.__add_level_non_root(node=child)

    def log(self) -> str:
        res = ''
        res += f'root: {self.__root.get_proc_uid()}'
        if self.__root.is_leaf():
            return res + f' val: {self.__root.get_val()}'
        queue = [c for c in self.__root.get_children()]
        last_depth = 1
        while len(queue) > 0:
            node = queue.pop(0)
            if node.get_depth() != last_depth:
                last_depth += 1
                res += '\n'
            res += node.__str__() + ' ** '
            if not node.is_leaf():
                queue = queue + node.get_children()
        return res

    def __str__(self):
        return self.log()

    def __repr__(self):
        return self.__str__()

    def convert_to_networkx_graph(self) -> nx.Graph:
        graph = nx.Graph()
        graph.add_node('-1')
        queue = [self.__root]
        while len(queue) > 0:
            node = queue.pop(0)
            path = ''.join(str(p) for p in node.get_path()[1:])
            if not node.is_root():
                parent = path[:-1] if len(path) > 1 else '-1'
                graph.add_edge(parent, path)
            if not node.is_leaf():
                queue = queue + node.get_children()
        return graph

    def get_decision_colors(self) -> list[str]:
        res = []
        queue = [self.get_root()]
        while len(queue) > 0:
            node = queue.pop(0)
            match node.get_decision():
                case 1:
                    color = 'lawngreen'
                case 0:
                    color = 'crimson'
                case -1:
                    if node.is_authed():
                        color = 'deepskyblue'
                    else:
                        color = 'yellow'
                case None:
                    color = 'yellow'
                case _:
                    color = 'lightgray'
            res.append(color)
            if not node.is_leaf():
                queue = queue + node.get_children()
        return res

    def plot_tree(self, fig_size: tuple[int, int] = (75, 10), path: str = None, node_size: int = 1200,
                  show_step_plots: bool = True):
        graph = self.convert_to_networkx_graph()
        plt.figure(figsize=fig_size)
        if self.__root.is_leaf():
            pos = nx.spring_layout(graph)
        else:
            pos = hierarchy_pos(graph, '-1')
        node_size_list = [node_size] * graph.number_of_nodes()
        colors = self.get_decision_colors()
        plt.title(f'process {self.get_proc_uid()} tree plot')
        nx.draw(graph, pos=pos, with_labels=True, node_size=node_size_list, node_color=colors)
        if path is not None:
            save_plot(path)
        if not show_step_plots:
            plt.close()

    def get_tree_height(self) -> int:
        height = 0
        node = self.__root
        while not node.is_leaf():
            node = node.get_children()[0]
            height += 1
        return height

    def get_message(self) -> AuthMessage:
        if self.get_root().is_leaf():
            msg_content = AuthMessageContent(self.get_root().get_path(), self.get_root().get_val(),
                                             bytes(self.get_root().get_val()))
            return AuthMessage([msg_content], sender=self.get_proc_uid())
        else:
            msg_contents = self.__get_messages(self.get_root())
            return AuthMessage(msg_contents, sender=self.get_proc_uid())

    def __get_messages(self, node: AuthNode) -> list[AuthMessageContent]:
        if node.is_leaf():
            return [AuthMessageContent(node.get_path(), node.get_val(), node.get_signed_val())]
        else:
            msg_contents = []
            for child in node.get_children():
                msg_contents += self.__get_messages(child)
            return msg_contents

    def apply_msg(self, msg: AuthMessage):
        for msg_content in msg.get_content():
            if len(msg_content.get_path_list()) == 0:
                self.__apply_msg_content(self.__root, [msg.get_sender()], msg_content.get_val(),
                                         msg_content.get_signed_val())
            else:
                path_from_root = msg_content.get_path_list()[1:] + [msg.get_sender()]
                self.__apply_msg_content(self.get_root(), path_from_root, msg_content.get_val(),
                                         msg_content.get_signed_val())

    def __apply_msg_content(self, node: AuthNode, path: list[int], val: int, signed_val: bytes):
        if len(path) == 0 or path is None:
            node.set_val(val)
            node.set_signed_val(signed_val)
            node.set_is_authed(True)
        else:
            next_id = path[0]
            for child in node.get_children():
                if child.get_proc_uid() == next_id:
                    self.__apply_msg_content(child, path[1:], val, signed_val)
                    break

    def decide(self):
        self.__decision = self.get_root().decide()
        return self.__decision
