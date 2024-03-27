from celery import shared_task

from habits.services import get_habit_scheduler, tg_bot_get_updates_check


@shared_task(name="check_habit_time")
def check_habit_time():
    """
    Проверяет время выполнения привычек и отправляет уведомления пользователям через Telegram.
    """
    # Проверка обновлений от Telegram бота и обновление данных пользователей
    tg_bot_get_updates_check()
    get_habit_scheduler()
