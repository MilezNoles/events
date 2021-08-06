def get_mail_subject(nick, event):
    return f"{nick}, на ваше событие: {event}, поступила заявка или отклик"


def get_mail_context(event_title, nick, type):
    return f'На ваше событие: {event_title}, оставил {type} юзер с ником: {nick}'
