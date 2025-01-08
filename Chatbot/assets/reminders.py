import threading
from datetime import datetime, timedelta
import logging

def set_reminder(time_str):
    try:
        reminder_time = datetime.strptime(time_str, '%H:%M')
        current_time = datetime.now()
        delta = reminder_time - current_time
        if delta.total_seconds() < 0:
            delta += timedelta(days=1)

        threading.Timer(delta.total_seconds(), reminder_alert).start()
        logging.debug(f"Reminder set for {time_str}")
    except Exception as e:
        logging.error(f'Error setting reminder: {e}')

def set_alarm(time_str):
    try:
        alarm_time = datetime.strptime(time_str, '%H:%M')
        current_time = datetime.now()
        delta = alarm_time - current_time
        if delta.total_seconds() < 0:
            delta += timedelta(days=1)

        threading.Timer(delta.total_seconds(), alarm_alert).start()
        logging.debug(f"Alarm set for {time_str}")
    except Exception as e:
        logging.error(f'Error setting alarm: {e}')

def reminder_alert():
    logging.info('Reminder alert!')
    print('Reminder alert!')

def alarm_alert():
    logging.info('Alarm alert!')
    print('Alarm alert!')