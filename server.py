from vk_api.exceptions import ApiError
from vk_api.bot_longpoll import VkBotMessageEvent

from pyeasyvkbot.core.utils import FileDB
from pyeasyvkbot.release import VkBot


class Server(VkBot):
    """
    All the bot logic is the upper level of the system, inherited from the parents
    providing the necessary functionality and allowing you to focus only on writing business logic
    """

    def __init__(self, *args, **kwargs):
        self.db = FileDB(file_name='chat.txt')
        super().__init__(*args, **kwargs)

    def command_ping(self, send_id: int) -> None:
        self.send_msg(send_id, message='Понг!')

    def command_hide_keyboard(self, send_id: int):
        self.send_msg(send_id, message='Клавиатура скрыта!', keyboard=self.keyboard.hide_keyboard())

    def command_return_keyboard(self, send_id: int):
        self.send_msg(send_id, message='✌️Вернул вам клавиатуру!', keyboard=self.keyboard.get_standart_keyboard())

    def command_helpop(self, send_id: int):
        text_in_msg = self.get_command_text(self._text_in_msg, self._command_args)
        if not text_in_msg:
            self.send_msg(send_id,
                          message=f'⛔️ Ваше обращение не может быть пустым!')
            return
        self.send_msg(send_id,
                      message=f'✅ Ваше обращение принято.\nАдминистрация рассмотрит его и ответит Вам в ближайшее время')
        self.send_admin_msg(
            f"👤 Пользователь написал: {text_in_msg}\n\n📞Для ответа ему используйте такой id: {send_id}")

    def start_chat(self, send_id: int):
        data_in_file = self.db.splitter()
        for number, line in enumerate(data_in_file):
            # Если пользователь уже ищет собеседника, то мы не записываем его заново в файл
            if line[-1] == '0' and line[0] == str(send_id):
                self.send_msg(send_id, message=f'Ищем собеседника...')
                break
            if line[-1] == '0' and line[0] != str(send_id):
                data_in_file[number][-1] = str(send_id)
                list_with_data = list(map(lambda i: '/'.join(i), data_in_file))
                self.db.write("\n".join(list_with_data), 'w')
                self.send_msg(send_id, message=f'Вы успешно начали диалог!\nПриятного общения😉')
                break
        else:
            self.db.write(f'{send_id}/0')
            self.send_msg(send_id, message=f'Ищем собеседника...')

    def send_chat(self, event: VkBotMessageEvent):
        data_in_file = self.db.splitter()
        data_in_file.reverse()
        send_id = str(event.object.peer_id)
        for number, line in enumerate(data_in_file):
            if line[0] == send_id and line[-1] != '0':
                companion_id = line[-1]
                break
            if line[-1] == send_id and line[0] != '0':
                companion_id = line[0]
                break
        else:
            self.start_chat(int(send_id))
            return
        if not self.send_msg(companion_id, message=event.object.text):
            self.send_msg(int(send_id), message='❌ Вы не можете отправлять сообщения такого типа!')
