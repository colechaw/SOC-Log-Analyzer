import json
from pathlib import Path
from datetime import datetime


def main():
    print("SOC Log Analyzer")

    log_path = Path("__file__").parent / "sample_logs.json"
    with log_path.open('r') as log_file:

        events = json.load(log_file)

        failure_count = 0
        failures_by_user = {}

        print (f"Loaded {len(events)} events\n")
        failure_threashhold = 5

        for event in events:
            event_time = datetime.fromisoformat(
                event["timestamp"].replace("Z", "+00:00")
            )

            print(event_time)
            if event['outcome'] == 'failure':
                username = event['username']

                if username not in failures_by_user:
                    failures_by_user[username] = 0

                failures_by_user[username] += 1

                #print(
                #    f"{event['timestamp']} | "
                #    f"{event['username']} | "
                #    f"{event['source_ip']} | "
                #    f"{event['outcome']} |"
                #)
        for username, count in failures_by_user.items():
            if count >= failure_threashhold:
                print(f"{username}: {count} failed login attempts")

if __name__ == "__main__":
    main()