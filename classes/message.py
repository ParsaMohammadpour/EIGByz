class MessageContent:
    def __init__(self, path_list: list[int], val: int):
        self.__path_list = path_list.copy()
        self.__val = val

    def get_path_list(self) -> list[int]:
        return self.__path_list.copy()

    def get_val(self) -> int:
        return self.__val

    def get_content(self) -> tuple[list[int], int]:
        return self.__path_list.copy(), self.__val

    def set_val(self, val: int):
        self.__val = val

    def __str__(self):
        path = ''.join(str(p) for p in self.__path_list)
        return f'path: {path}, val: {self.__val}'

    def __repr__(self):
        return self.__str__()


class Message:
    def __init__(self, content_list: list[MessageContent], sender: int):
        self.__contents = content_list.copy()
        self.__sender = sender

    def get_content(self) -> list[MessageContent]:
        return self.__contents.copy()

    def get_sender(self) -> int:
        return self.__sender

    def __str__(self):
        contents_str = [str(content) for content in self.__contents]
        return f'sender: {self.get_sender()}\n' + '\n'.join(contents_str)

    def __repr__(self):
        return self.__str__()
