from collections import defaultdict


class Dialogue:
    """
    Класс для работы с диалогом. В будущем можно внедрить работу с базой данных
    """

    def __init__(self, state: str, data=None):
        self.state = state
        self.data = data

    def set_state(self, new_state: str):
        self.state = new_state

    def set_data(self, new_data):
        self.data = new_data

    def __str__(self):
        return f"state={self.state}, data={self.data}"

    def __repr__(self):
        return f"state={self.state}, data={self.data}"


class Context:
    """
    Класс для хранения данных о полоьзователях и диалогах.
    Сейчас данные хранятся в памяти, в будущем здесь
    можно имплементировать базу данных и пулл соединений
    """

    dialogue: defaultdict[int, Dialogue]

    def __init__(self):
        self.dialogue = defaultdict()

    def get_dialogue(self, user_id):
        return self.dialogue.get(user_id)

    def start_dialogue(self, user_id: int, state: str, data=None):
        self.dialogue[user_id] = Dialogue(state, data)

    def end_dialogue(self, user_id: int):
        del self.dialogue[user_id]
