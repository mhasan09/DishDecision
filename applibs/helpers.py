from datetime import datetime, time


def string_to_datetime(datetime_string, format="%Y-%m-%d %H:%M:%S.%f"):
    return datetime.strptime(datetime_string, format)


def check_time_limit_validity_for_uploading_menu():
    current_time = datetime.now().time()
    # Define the time ranges for midnight (12:00 AM) and 10:00 AM
    midnight = time(0, 0)
    ten_am = time(10, 0)

    # Check if the current time is between midnight and 10:00 AM
    if midnight <= current_time < ten_am:
        return True
    return False


def check_time_limit_validity_for_voting():
    current_time = datetime.now().time()
    # Define the time ranges for midnight (12:00 AM) and 10:00 AM
    midnight = time(10, 0)
    ten_am = time(12, 0)

    # Check if the current time is between midnight and 10:00 AM
    if midnight <= current_time < ten_am:
        return True
    return False
