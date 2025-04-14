from datetime import datetime

def calculate_uptime_downtime(start: datetime, end: datetime, polls: list):
    """
    Calculate uptime and downtime between start and end times using poll data.
    Returns uptime and downtime in minutes.
    """
    print(start)
    uptime = downtime = 0
    last_status = "inactive"  # assuming offline until the first poll
    last_time = start

    for poll in polls:
        if poll.timestamp_utc < start or poll.timestamp_utc > end:
            continue  # skip polls outside the interval

        delta = (poll.timestamp_utc - last_time).total_seconds() / 60
        if last_status == "active": ## add to uptime if active
            uptime += delta
        else:
            downtime += delta

        last_status = poll.status
        last_time = poll.timestamp_utc

    final_delta = (end - last_time).total_seconds() / 60 ## last interval remains
    if last_status == "active":
        uptime += final_delta
    else:
        downtime += final_delta

    return uptime, downtime
