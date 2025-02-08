import requests
import argparse
import json
from datetime import datetime
import os


parser = argparse.ArgumentParser(
    description="Get GitHub events for a user."
)
parser.add_argument("username", help="GitHub username to fetch events for")
parser.add_argument("--event-type", help="Filter events by type (e.g., PushEvent, IssuesEvent)")
args = parser.parse_args()


def get_events(username: str):

    # Caching: Events are saved in a local JSON file ({username}_events.json) to avoid fetching data from the API on subsequent runs, improving performance.
    cache_file = f"{username}_events.json"

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            events = json.load(f)

    else:
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url)

        if response.status_code == 200:
            events = response.json()

            with open(cache_file, "w") as f:
                json.dump(events, f)

        elif response.status_code == 404:
            print(f"Error: User '{username}' not found.")
            return
        else:
            print(f"Failed to retrieve events. Status code: {response.status_code}")
            return

    if events:
        print(f"Recent Activity for {username}:")

        event_type_filter = args.event_type

        for event in events:
            event_type = event['type']
            repo_name = event['repo']['name']
            created_at = event['created_at']
            ref = event['payload'].get('ref',None)

            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = created_at_dt.strftime("%b %d, %Y at %H:%M:%S")

            if event_type_filter and event_type != event_type_filter:
                continue

            if event_type == "CreateEvent":
                if ref:
                    print(f"- Created a new branch '{ref}' in {repo_name} on {formatted_time}") 
                else:
                    print(f"- Created a repository '{repo_name}' on {formatted_time}") 

            elif event_type == "PushEvent":
                commits_count = len(event['payload']['commits'])
                print(f"- Pushed {commits_count} commit(s) to {repo_name} on {formatted_time}")

            elif event_type == "IssuesEvent":
                print(f"- Opened an issue in {repo_name} on {formatted_time}")

            elif event_type == "WatchEvent":
                print(f"- Starred {repo_name} on {formatted_time}")

        else:
            print(f"No recent events found for {username}.")

get_events(args.username)