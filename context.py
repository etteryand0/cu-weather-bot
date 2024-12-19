from collections import defaultdict


class Context:
    """
    Класс для хранения данных о полоьзователях и диалогах.
    Сейчас данные хранятся в памяти, в будущем здесь
    можно имплементировать базу данных и пулл соединений
    """

    def __init__(self):
        self.dialogue = defaultdict()

    def get_dialogue(self, user_id):
        return self.dialogue.get(user_id)

    def set_dialogue(self, user_id, value):
        self.dialogue[user_id] = value
