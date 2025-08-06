# notifications.py
from flask import Flask
from flask_apscheduler import APScheduler
from app.model.notifications_preferences import NotificationPreference
from app.model.user import User
import smtplib
from email.message import EmailMessage

# at the top of notifications.py
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash,
    g,
)
from app.model.notifications_preferences import NotificationPreference


notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "yafawebsite@gmail.com"
SMTP_PASS = "qsit qdze utlr bqwe"
# qsit qdze utlr bqwe

scheduler = APScheduler()


def send_notification(subject: str, body: str, to: str) -> None:
    """Send an email via SMTP."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def schedule_notifications(user_id: int) -> None:
    """Schedule reminders based on user-defined preferences."""
    prefs = NotificationPreference.query.filter_by(user_id=user_id).all()
    for pref in prefs:
        user_email = pref.user.email
        if not user_email:
            continue

        for time_str in pref.times.split(","):  # e.g. "08:00,12:00,18:00"
            hour, minute = map(int, time_str.split(":"))
            job_id = f"user{user_id}-{pref.reminder_type}-{time_str}".replace(":", "")
            scheduler.add_job(
                id=job_id,
                func=send_notification,
                args=[
                    f"{pref.reminder_type.title()} Reminder",
                    pref.message,
                    user_email,
                ],
                trigger="cron",
                hour=hour,
                minute=minute,
            )


def send_water_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user and user.email:
        send_notification(
            subject="Hydration Reminder",
            body=f"Hi {user.username}, remember to drink water and stay hydrated!",
            to=user.email,
        )


def send_steps_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user and user.email:
        send_notification(
            subject="Steps Reminder",
            body=f"Hi {user.username}, make sure to get enough steps in today!",
            to=user.email,
        )


def send_nutrients_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user and user.email:
        send_notification(
            subject="Nutrition Reminder",
            body=f"Hi {user.username}, don't forget to eat a balanced diet with enough nutrients!",
            to=user.email,
        )
def send_motivation_reminder(user_id: int) -> None:
    user = User.query.get(user_id)
    if user and user.email:
        motivation_quotes = [
            "Keep pushing forward, you are doing great!",
            "Every step counts — stay motivated!",
            "Believe in yourself and all that you are.",
            "Your body can stand almost anything — it’s your mind you have to convince.",
            "Consistency is key — keep going!",
        ]
        # Pick a quote based on user ID to vary messages (simple approach)
        quote = motivation_quotes[user_id % len(motivation_quotes)]
        send_notification(
            "Motivation Reminder",
            f"Hi {user.username}, here's a motivation boost for you:\n\n{quote}",
            user.email,
        )


def schedule_daily_reminders(user_id: int) -> None:
    """Schedule built-in daily health reminders."""
    scheduler.add_job(
        id=f"water-reminder-{user_id}",
        func=send_water_reminder,
        args=[user_id],
        trigger="cron",
        hour=9,  # 9 AM daily
        minute=0,
    )
    scheduler.add_job(
        id=f"steps-reminder-{user_id}",
        func=send_steps_reminder,
        args=[user_id],
        trigger="cron",
        hour=12,  # 12 PM daily
        minute=0,
    )
    scheduler.add_job(
        id=f"nutrients-reminder-{user_id}",
        func=send_nutrients_reminder,
        args=[user_id],
        trigger="cron",
        hour=18,  # 6 PM daily
        minute=0,
    )


def init_notifications(app: Flask) -> None:
    """Initialize APScheduler and schedule all reminders for every user."""
    app.config.setdefault("SCHEDULER_API_ENABLED", True)
    scheduler.init_app(app)

    # ensure we're in app context for DB queries
    with app.app_context():
        for user in User.query.all():
            schedule_notifications(user.id)
            schedule_daily_reminders(user.id)

    scheduler.start()


def main():
    """Standalone test for emailing notifications."""
    import datetime
    import time

    # Direct email test
    send_notification(
        subject="Test Notification",
        body="This is a direct test notification via email.",
        to="minh.tran@ufl.edu",
    )

    # Scheduled email test (3 seconds from now)
    run_at = datetime.datetime.now() + datetime.timedelta(seconds=3)
    scheduler.add_job(
        id="email-test",
        func=send_notification,
        args=[
            "Scheduled Test Notification",
            "This is a 3-second scheduled test email.",
            "minh.tran@ufl.edu",
        ],
        trigger="date",
        run_date=run_at,
    )

    app = Flask(__name__)
    scheduler.init_app(app)
    scheduler.start()

    # wait for the email job to fire
    time.sleep(5)


from app.routes.auth import login_required


@notifications_bp.route("/settings")
@login_required
def settings():
    current_uid = g.user.id
    prefs = []  # TODO: load user prefs once model is integrated
    return render_template("settings.html", prefs=prefs)


@notifications_bp.route("/schedule_all")
@login_required
def schedule_all():
    current_uid = g.user.id

    # Schedule user-defined prefs (if model exists) and daily reminders
    try:
        schedule_notifications(current_uid)
    except:
        pass
    schedule_daily_reminders(current_uid)

    flash("Notifications have been scheduled!", "success")
    return redirect(url_for("notifications.settings"))


if __name__ == "__main__":
    main()
