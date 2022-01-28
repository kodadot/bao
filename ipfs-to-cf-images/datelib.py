from datetime import datetime, timedelta


def ago(min= 15):
    """
    Return a datetime object representing the time `min` minutes ago.
    """
    return datetime.now() - timedelta(minutes=min)

def fmt_date(date):
    """
    Return a formatted string for a datetime object.
    """
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")