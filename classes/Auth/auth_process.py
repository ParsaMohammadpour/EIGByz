import random
from cryptidy import asymmetric_encryption

from classes.Auth.auth_eig_tree import AuthEIGByzTree
from classes.Auth.auth_message import AuthMessage
from classes.message import Message


class AuthProcess:
    def __init__(self, proc_uid: int, proc_count: int, proc_val: int, is_byz: bool = False, lie_prob: int = 50):
        self.__proc_uid = proc_uid
        self.__proc_count = proc_count
        self.__proc_val = proc_val
        self.__byz = is_byz
        self.__tree = AuthEIGByzTree(self.__proc_uid, self.__proc_count, self.__proc_val)
        self.__received_messages = []
        self.__decision = None
        self.__lie_prob = lie_prob
        self.__public_keys = None
        self.__pub_key, self.__pri_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key
        # here we change public key and private key in order to make simply convert rsa encryption
        # to digital signature

    def set_public_keys(self, keys: list[str]):
        if len(keys) != self.get_proc_count():
            raise ValueError(
                f'public keys len {len(keys)} is not as same size an process counts {self.get_proc_count()}')
        if keys[self.get_proc_uid() - 1] != self.get_pub_key():
            raise ValueError(f'process {self.get_proc_uid()} has different public key with pub keys list')
        self.__public_keys = keys.copy()

    def get_public_keys(self) -> list[str]:
        return self.__public_keys.copy()

    def get_pub_key(self) -> str:
        return self.__pub_key

    def get_proc_uid(self) -> int:
        return self.__proc_uid

    def get_proc_count(self) -> int:
        return self.__proc_count

    def get_proc_val(self) -> int:
        return self.__proc_val

    def get_decision(self) -> int:
        return self.__decision

    def get_tree(self) -> AuthEIGByzTree:
        return self.__tree

    def get_lie_prob(self) -> int:
        return self.__lie_prob

    def is_byz(self) -> bool:
        return self.__byz

    def receive_msg(self, msg: Message):
        self.__received_messages.append(msg)

    def receive_msgs(self, msgs: list[Message]):
        for msg in msgs:
            self.receive_msg(msg)

    def apply_msgs(self):
        for msg in self.__received_messages:
            filtered_msg = self.__filter_msgs_by_correct_signature(msg)
            self.get_tree().apply_msg(filtered_msg)

    def __filter_msgs_by_correct_signature(self, msg: AuthMessage) -> AuthMessage:
        msg_contents_to_remove = []
        for msg_content in msg.get_content():
            if msg_content.get_val() is None:
                msg_contents_to_remove.append(msg_content)
                continue
            original_val = msg_content.get_signed_val()
            path = msg_content.get_path_list()
            path.append(msg.get_sender())
            if -1 in path:
                path.remove(-1)
            path.reverse()
            has_exception = False
            for p in path:
                try:
                    key = self.get_public_keys()[p - 1]
                    _, original_val = asymmetric_encryption.decrypt_message(original_val, key)
                except Exception as e:
                    has_exception = True
                    print(
                        f'proc: {self.get_proc_uid()} failed to receive from proc: {msg.get_sender()} for path: {msg_content.get_path_list()} for p: {p}, content: {msg_content.get_signed_val()[:4] if msg_content.get_signed_val() is not None else str()}, exception: {e}')
                    msg_contents_to_remove.append(msg_content)
                    break
            if has_exception or original_val != msg_content.get_val():
                msg_contents_to_remove.append(msg_content)
        final_msg_contents = [mc for mc in msg.get_content() if mc not in msg_contents_to_remove]
        return AuthMessage(final_msg_contents, sender=msg.get_sender())

    def generate_msg(self):
        msg = self.get_tree().get_message()
        random.seed()
        if self.is_byz():
            for msg_content in msg.get_content():
                if random.randint(1, 100) <= self.get_lie_prob():
                    val = msg_content.get_val()
                    val = random.randint(0, 1) if val is None else 1 - val
                    msg_content.set_val(val)  # 1 - val change zero to one and one to zero
        for msg_content in msg.get_content():
            if self.get_tree().get_root().is_leaf():
                value_to_sign = msg_content.get_val()
            else:
                value_to_sign = msg_content.get_signed_val()
            signed = asymmetric_encryption.encrypt_message(value_to_sign, self.__pri_key)
            msg_content.set_signed_val(signed)
        return msg

    def plot_tree(self, fig_size: tuple[int, int] = (75, 10), path: str = None, node_size: int = 1200,
                  show_step_plots: bool = True):
        self.__tree.plot_tree(fig_size=fig_size, path=path, node_size=node_size, show_step_plots=show_step_plots)

    def add_tree_level(self):
        tree_height = self.get_tree().get_tree_height()
        if tree_height != self.get_proc_count():
            self.get_tree().add_level()
        else:
            raise Exception(f'tree-has been completed with height: {tree_height}')

    def log_tree(self):
        return self.get_tree().log()

    def decide(self) -> int:
        self.__decision = self.get_tree().decide()
        return self.__decision
