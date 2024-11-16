import matplotlib.pyplot as plt

import random
import os

from classes.Auth.auth_process import AuthProcess


def save_plot(path):
    generate_file(path)
    plt.savefig(path)


def generate_file(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


class AuthEIGByzSim:
    def __init__(self, proc_count: int, byz_proc_count: int, initial_vals: list[int] = None, byz_prob: int = 50):
        self.__proc_count = proc_count
        self.__byz_proc_count = byz_proc_count
        self.__set_byz_proc_uid_list()
        self.__byz_prob = byz_prob
        self.__set_initial_vals(initial_vals)
        self.__generate_process_list()
        self.__set_public_keys()
        self.__set_processes_all_pub_keys()

    def __set_processes_all_pub_keys(self):
        for p in self.get_processes():
            p.set_public_keys(self.get_public_keys())

    def get_public_keys(self):
        return self.__public_keys.copy()

    def __set_public_keys(self):
        self.__public_keys = [p.get_pub_key() for p in self.get_processes()]

    def get_processes(self):
        return self.__processes

    def __generate_process_list(self):
        self.__processes = [self.__generate_proc_with_uid(uid) for uid in range(1, self.__proc_count + 1)]

    def __generate_proc_with_uid(self, uid):
        is_byz = uid in self.__byz_proc_uid_list
        return AuthProcess(proc_uid=uid, proc_count=self.__proc_count, proc_val=self.__initial_vals[uid - 1],
                           is_byz=is_byz, lie_prob=self.__byz_prob)

    def __set_byz_proc_uid_list(self):
        self.__byz_proc_uid_list = random.sample(list(range(1, self.__proc_count + 1)), self.__byz_proc_count)

    def __set_initial_vals(self, initial_vals: list[int] = None):
        if initial_vals is None:
            initial_vals = random.choices([0, 1], k=self.__proc_count)
        self.__initial_vals = initial_vals.copy()

    def get_byz_proc(self):
        return self.__byz_proc_uid_list.copy()

    def get_proc_initial_vals(self):
        return self.__initial_vals.copy()

    def __send_all_messages(self):
        for p in self.__processes:
            # generating messages for each process specifically because byzantine process be able
            # to send different messages for different processes
            msgs = self.__generate_all_messages()
            p.receive_msgs(msgs)

    def __generate_all_messages(self):
        msgs = [p.generate_msg() for p in self.get_processes()]
        return msgs

    def __add_tree_level(self):
        for p in self.__processes:
            p.add_tree_level()

    def __apply_messages(self):
        for p in self.__processes:
            p.apply_msgs()

    def __save_step_plot(self, base_path: str, step: int, node_size: int, fig_size: tuple[int, int],
                         show_step_plots: bool):
        for p in self.__processes:
            path = base_path + f'step-{step}/proc-{p.get_proc_uid()}.png'
            p.plot_tree(fig_size=fig_size, node_size=node_size, path=path, show_step_plots=show_step_plots)

    def __plot_final_decision(self, base_path: str, node_size: int, fig_size: tuple[int, int]):
        for p in self.__processes:
            path = base_path + f'final-decision/proc-{p.get_proc_uid()}.png'
            p.plot_tree(fig_size=fig_size, node_size=node_size, path=path)

    def __decide(self):
        for p in self.__processes:
            p.decide()

    def get_final_decision(self) -> list[int]:
        return [p.get_decision() for p in self.__processes]

    def apply_algo(self, save_step_plot: bool = True, show_step_plots: bool = False, save_decision_plot: bool = True,
                   base_path: str = 'results-auth/', fig_size: tuple[int, int] = (15, 5), node_size: int = None,
                   step_number: int = None):
        if step_number is None:
            step_number = self.__byz_proc_count + 1
        if node_size is None:
            node_size = 1000 + self.__proc_count * 100
        if base_path is not None:
            base_path += f'proc-{self.__proc_count}-byz-{self.__byz_proc_count}-r-{step_number}/'
        for i in range(1, step_number + 1):
            self.__send_all_messages()
            self.__add_tree_level()
            self.__apply_messages()
            if save_step_plot:
                self.__save_step_plot(base_path, i, node_size, fig_size, show_step_plots=show_step_plots)
        self.__decide()
        if save_decision_plot:
            self.__plot_final_decision(base_path, node_size, fig_size)
        return self.get_final_decision()

    def check_agreement(self) -> bool:
        decision_set = set()
        for p in self.__processes:
            if not p.is_byz():
                decision_set.add(p.get_decision())
        return len(decision_set) == 1

    def check_validity(self) -> bool:
        initial_values_set = set()
        for p in self.__processes:
            if not p.is_byz():
                initial_values_set.add(p.get_proc_val())
        if len(initial_values_set) > 1:
            return True
        decision_set = set()
        for p in self.__processes:
            if not p.is_byz():
                decision_set.add(p.get_decision())
        return decision_set == initial_values_set

    def check_termination(self) -> bool:
        for p in self.__processes:
            if not p.is_byz() and p.get_decision() is None:
                return False
        return True

    def check_requirements(self) -> str:
        validity = self.check_validity()
        termination = self.check_termination()
        agreement = self.check_agreement()
        if validity and termination and agreement:
            return '-'
        res = []
        if not validity:
            res.append('validity')
        if not termination:
            res.append('termination')
        if not agreement:
            res.append('agreement')
        return '-'.join(res)
