from celery import shared_task
from habits.services import get_habit_scheduler, tg_bot_get_updates_check, get_combined_message


@shared_task
def check_habit_time():
    """
    Проверяет время выполнения привычек и отправляет уведомления пользователям через Telegram.
    """
    # Проверка обновлений от Telegram бота и обновление данных пользователей
    tg_bot_get_updates_check()
    get_habit_scheduler()
