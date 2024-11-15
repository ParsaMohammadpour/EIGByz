import random

from classes.message import Message
from classes.eig_tree import EIGByzTree


class Process:
    def __init__(self, proc_uid: int, proc_count: int, proc_val: int, is_byz: bool = False, lie_prob: int = 50):
        self.__proc_uid = proc_uid
        self.__proc_count = proc_count
        self.__proc_val = proc_val
        self.__byz = is_byz
        self.__tree = EIGByzTree(self.__proc_uid, self.__proc_count, self.__proc_val)
        self.__received_messages = []
        self.__decision = None
        self.__lie_prob = lie_prob

    def get_proc_uid(self) -> int:
        return self.__proc_uid

    def get_proc_count(self) -> int:
        return self.__proc_count

    def get_proc_val(self) -> int:
        return self.__proc_val

    def get_decision(self) -> int:
        return self.__decision

    def is_byz(self) -> bool:
        return self.__byz

    def receive_msg(self, msg: Message):
        self.__received_messages.append(msg)

    def receive_msgs(self, msgs: list[Message]):
        for msg in msgs:
            self.receive_msg(msg)

    def apply_msgs(self):
        for msg in self.__received_messages:
            self.__tree.apply_msg(msg)

    def generate_msg(self):
        msg = self.__tree.get_message()
        random.seed()
        if self.__byz:
            for msg_content in msg.get_content():
                if random.randint(1, 100) <= self.__lie_prob:
                    val = msg_content.get_val()
                    msg_content.set_val(1 - val)  # 1 - val change zero to one and one to zero
        return msg

    def plot_tree(self, fig_size: tuple[int, int] = (75, 10), path: str = None, node_size: int = 1200,
                  show_step_plots: bool = True):
        self.__tree.plot_tree(fig_size=fig_size, path=path, node_size=node_size, show_step_plots=show_step_plots)

    def add_tree_level(self):
        tree_height = self.__tree.get_tree_height()
        if tree_height != self.get_proc_count():
            self.__tree.add_level()
        else:
            raise Exception(f'tree-has been completed with height: {tree_height}')

    def log_tree(self):
        return self.__tree.log()

    def decide(self) -> int:
        self.__decision = self.__tree.decide()
        return self.__decision
