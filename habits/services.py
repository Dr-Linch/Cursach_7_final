from collections import defaultdict
# from datetime import datetime
import requests
from django.utils import timezone
from django.conf import settings
from habits.models import Habit
from users.models import User

WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def send_telegram_message(messages):
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
    for chat_id, message in messages.items():
        params = {"chat_id": chat_id, "text": message}
        response = requests.post(url=url, data=params)
        return response.json()


def check_habits(habit, current_time, today):
    if habit.frequency in ('Daily', today):
        if habit.time.strftime('%H:%M') == current_time.strftime('%H:%M'):
            print(f'Информация привычки: {habit}')

            chat_id = habit.owner.chat_id
            message = f'Действие: {habit.action}\nМесто: {habit.place}'

            if habit.tribute:
                message += f'Награда: {habit.tribute}'
            elif habit.pleasant_link:
                message += f'Создайте приятную привычку: {habit.pleasant_link}'
            else:
                message += 'Награда или приятная привычка не выбраны'

            message += f'  Продолжительность: {habit.duration}'
            return chat_id, message
    return None


def get_group_habits_by_day_time(habits):
    habits_by_day_time = defaultdict(list)
    for habit in habits:
        habits_by_day_time[(habit.frequency, habit.time)].append(habit)
    return habits_by_day_time


def get_combined_message(united_habits, current_time, today):
    combined_message = ''
    chat_ids = []
    for habit in united_habits:
        chat_id, message = check_habits(habit, current_time, today)
        if chat_id and message:
            chat_ids.append(chat_id)
            combined_message += message + '\n'
    return chat_ids, combined_message


def get_habit_scheduler():
    # current_time = datetime.now()
    # today = WEEK_DAYS[datetime.today().weekday()]
    current_time = timezone.now()
    today = WEEK_DAYS[timezone.now().weekday()]

    habits = Habit.objects.filter(is_pleasant=False, frequency__in=['Daily', today])
    habits_by_day_time = get_group_habits_by_day_time(habits)

    message = {}
    for (time, frequency), grouped_habits in habits_by_day_time.items():
        try:
            chat_ids, combined_message = get_combined_message(grouped_habits, current_time, today)
        except TypeError:
            print('Нет подходящих привычек!')
            break
        if chat_ids and combined_message:
            for chat_id in chat_ids:
                message[chat_id] = combined_message
    mes = send_telegram_message(message)
    return mes


def tg_bot_get_updates_check():
    get_updates_url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/getUpdates"
    response = requests.get(get_updates_url)

    if response.status_code == 200:
        for telegram_users in response.json()['result']:
            telegram_user_chat_id = telegram_users['message']['from']['id']
            telegram_user_name = telegram_users['message']['from']['username']

            try:
                user = User.objects.get(tg_user_name=telegram_user_name)
                if user.chat_id is None:
                    user.chat_id = telegram_user_chat_id
                    user.save()
            except User.DoesNotExist:
                print('Пользователь не найден')
