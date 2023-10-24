from datetime import datetime


def string_to_datetime(datetime_string, format="%Y-%m-%d %H:%M:%S.%f"):
    return datetime.strptime(datetime_string, format)