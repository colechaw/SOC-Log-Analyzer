import json
from pathlib import Path
from datetime import datetime, timedelta


def main():

    print("SOC Log Analyzer")

    # Our test data is stored in a JSON file at this point
    log_path = Path("__file__").parent / "sample_logs.json"
    with log_path.open('r') as log_file:

        events = json.load(log_file)

        # We began by counting the number of failed
        # logins, then graduated to storing the failed
        # logins by time.  Here are the variables we used,
        # the depricated one is here for context
        failures_by_user = {} # Legacy
        failure_times_by_user = {}

        # We count and display the number of events loaded
        # to ensure that worked.  From here the threshold of
        # login failures and time between each failure is set
        print (f"Loaded {len(events)} events\n")
        failure_threshold = 5
        time_window = timedelta(minutes=10)

        for event in events:

            if event['outcome'] == 'failure':
                username = event['username']

                event_time = datetime.fromisoformat(
                    event["timestamp"].replace("Z", "+00:00")
                )

                if username not in failure_times_by_user:
                    failure_times_by_user[username] = []

                failure_times_by_user[username].append(event_time)

                # Our first code simply counted failures
                # It was kept to display the test data was in fact
                # being caught
                if username not in failures_by_user:
                    failures_by_user[username] = 0

                failures_by_user[username] += 1

    # At this point it was decided to store the alerts in a txt file
    alert_path = Path(__file__).parent / "alerts.txt"
    with alert_path.open("a") as alert_file:

        for username, times in failure_times_by_user.items():
            times.sort()

            # Looping through the list of events we remember to subtract
            # 1 to prevent an error from incorrect indexing
            for start in range(len(times)):
                end = start + failure_threshold - 1

                if end >= len(times):
                    break

                elapsed_time = times[end] - times[start]

                if elapsed_time <= time_window:
                    message = (
                        f"ALERT: {username} had at least {failure_threshold} "
                        f"failed logins within {time_window} "
                        f"starting at {times[start]}"
                    )

                    alert_file.write(message + "\n")

                    print(message)
                    break

    for username, count in failures_by_user.items():
        if count >= failure_threshold:
            print(f"{username}: {count} failed login attempts")



if __name__ == "__main__":
    main()