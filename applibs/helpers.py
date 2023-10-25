from datetime import datetime, time, date, timedelta


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
    morning = time(10, 0)
    noon = time(12, 0)

    if morning <= current_time < noon:
        return True
    return False


def get_three_consecutive_days():
    today = date.today()

    # Calculate the date for three days ago
    three_days_ago = today - timedelta(days=3)

    # Create a list of the last three consecutive days
    consecutive_days = [three_days_ago + timedelta(days=i) for i in range(3)]
    return consecutive_days
