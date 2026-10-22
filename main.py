import json
from pathlib import Path
from datetime import datetime, timedelta


def main():
    print("SOC Log Analyzer")

    log_path = Path("__file__").parent / "sample_logs.json"
    with log_path.open('r') as log_file:

        events = json.load(log_file)

        failures_by_user = {}
        failure_times_by_user = {}

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

                if username not in failures_by_user:
                    failures_by_user[username] = 0

                failures_by_user[username] += 1

        for username, times in failure_times_by_user.items():
            #print(f"{username}: {len(times)} failed logins")
            times.sort()
            
            for start in range(len(times)):
                end = start + failure_threshold - 1
                
                if end >= len(times):
                    break
                    
                elapsed_time = times[end] - times[start]
                
                if elapsed_time <= time_window:
                    print(f"ALERT: {username} had {failure_threshold} failed logins within {time_window} starting at {times[start]}")
                    break
            
        for username, count in failures_by_user.items():
            if count >= failure_threshold:
                print(f"{username}: {count} failed login attempts")

if __name__ == "__main__":
    main()