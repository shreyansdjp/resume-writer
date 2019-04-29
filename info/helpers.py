from datetime import datetime

# check data if data is dirty


# check if date_started and date_ended has minimum difference of 30 days
def check_dates(date_started, date_ended):
    date_format = "%Y-%m-%d"
    if not date_ended:
        return False
    started = datetime.strptime(date_started, date_format)
    ended = datetime.strptime(date_ended, date_format)
    delta = ended - started
    if delta.days < 30:
        return True
    return False
