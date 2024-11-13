class Message:
    def __init__(self, msg:list[list[int], int]):
        self.__msg = msg.copy()

    def get_msg(self) -> list[list[int], int]:
        return self.__msg

    def __repr__(self):
        print(self.__msg)