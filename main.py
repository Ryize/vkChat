import os

API_KEY = os.getenv('API_KEY')
GROUP_ID = int(os.getenv('GROUP_ID'))

if __name__ == '__main__':
    from server import Server

    server = Server(api_token=API_KEY, group_id=GROUP_ID, debug=True)

    server.admins = [513239285]

    COMMANDS = {
        '/help': {
            'command': server.command_help,
            'comment': 'Получить список всех команд',
        },
        '/dialog': {
            'command': server.start_chat,
            'comment': 'Начать диалог с рандомным пользователем',
        },
        '/ping': {
            'command': server.command_ping,
            'comment': 'Проверить работоспособность бота',
        },
        '/helpop *args': {
            'command': server.command_helpop,
            'comment': 'Задать вопрос Администрации',
        },
        '☠️Скрыть клавиатуру *nshow': {
            'command': server.command_hide_keyboard,
            'comment': 'Получить своё расписание',
        },
        '📌️Вернуть клавиатуру *nshow': {
            'command': server.command_return_keyboard,
            'comment': 'Получить своё расписание',
        },
        '✍️Начать диалог *nshow': {
            'command': server.start_chat,
            'comment': 'Начать диалог с рандомным пользователем',
        },
        'Начать *nshow': {
            'command': server.command_help,
            'comment': 'Получить список всех команд',
        },
        '🔎Помощь *nshow': {
            'command': server.command_help,
            'comment': 'Получить список всех команд',
        },
    }
    while True:
        server.start(COMMANDS)
