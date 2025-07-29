from flask import Flask
from flask_apscheduler import APScheduler
from ..model.notifications_preferences import NotificationPreference
from app.model.user import User
# from flask_socketio import current_app

scheduler = APScheduler()


def send_notification(title: str, message: str) -> None:
    # Make actual notifications later, for now just prints to console
    print(f'[Notification] {title}: {message}')


def schedule_notifications(user_id: int) -> None:
    # Schedules notifications for reminders in one user's prefs
    prefs = (NotificationPreference.query.filter_by(user_id=user_id).all())
    for pref in prefs:
        for time_str in pref.times.split(','):  # "08:00,12:00,18:00"
            hour, minute = map(int, time_str.split(':'))
            job_id = f"user{pref.user_id}-{pref.reminder_type}-{time_str}".replace(':', '')
            scheduler.add_job(
                id=job_id,
                func=send_notification,
                args=[
                    f'{pref.reminder_type} Reminder for {pref.user.username}',
                    pref.message
                ],
                trigger='cron',
                hour=hour,
                minute=minute
            )


def send_water_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user:
        send_notification(
            title="Hydration Reminder",
            message=f"Hi {user.username}, remember to drink water and stay hydrated!"
        )


def send_steps_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user:
        send_notification(
            title="Steps Reminder",
            message=f"Hi {user.username}, make sure to get enough steps in today!"
        )


def send_nutrients_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user:
        send_notification(
            title="Nutrition Reminder",
            message=f"Hi {user.username}, don't forget to eat a balanced diet with enough nutrients!"
        )


def schedule_daily_reminders(user_id: int) -> None:
    # Schedule daily reminders for water, steps, and nutrients
    scheduler.add_job(
        id=f"water-reminder-{user_id}",
        func=send_water_reminder,
        args=[user_id],
        trigger='cron',
        hour=9  # Example: 9 AM daily
    )
    scheduler.add_job(
        id=f"steps-reminder-{user_id}",
        func=send_steps_reminder,
        args=[user_id],
        trigger='cron',
        hour=12  # Example: 12 PM daily
    )
    scheduler.add_job(
        id=f"nutrients-reminder-{user_id}",
        func=send_nutrients_reminder,
        args=[user_id],
        trigger='cron',
        hour=18  # Example: 6 PM daily
    )


def init_notifications(app: Flask) -> None:
    # enable scheduler api
    app.config.setdefault('SCHEDULER_API_ENABLED', True)

    # start scheduler
    scheduler.init_app(app)
    for user in User.query.all():
        schedule_notifications(user.id)
        schedule_daily_reminders(user.id)
    scheduler.start()


def main():  # test notification usage, need to add notification scheduling testing too
    import datetime
    import time

    # direct notification test
    send_notification(title="Test Notification",
                      message="This is a direct test notification.")

    # scheduled notification test
    run_at = datetime.datetime.now() + datetime.timedelta(seconds=3)
    scheduler.add_job(
        id='standalone-test',
        func=send_notification,
        args=["Test Notification", "This is a 3-second scheduled test notification."],
        trigger='date',
        run_date=run_at
    )
    scheduler.start()

    time.sleep(5)


if __name__ == "__main__":
    main()
