# GitHub Activity CLI

A simple command-line interface (CLI) to fetch and display recent GitHub activity for a specified user. This project allows you to view events such as commits, issue creation, and pushed events.

## Features

- Fetches recent GitHub activity for a specified user.
- Allows filtering events by type (e.g., PushEvent, IssuesEvent, WatchEvent).
- Caches the data locally in a JSON file to improve performance on subsequent runs.
- Displays events with timestamps for easy reading.

## Requirements

- Python 3.12+
- requests library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/codefromlani/Roadmap.sh-Projects.git
cd beginner
cd github-user-activity
```

2. Install dependencies:
```bash
pip install requests
```

## Usage

Run the program from the command line, providing a GitHub username and an optional event filter.

- Syntax

    python github_activity.py <username> [--event-type <event_type>]

- Example:
    Fetch all recent activity for a user:

        python github_activity.py kamranahmedse

    Fetch only PushEvent activity for a user:

        python github_activity.py kamranahmedse --event-type PushEvent

- Output:
The program will display recent events in the terminal. For example:

- Pushed 3 commit(s) to kamranahmedse/repository on Jan 01, 2025 at 10:00:00
- Opened an issue in kamranahmedse/repository on Jan 01, 2025 at 11:00:00
- Starred kamranahmedse/repository on Jan 01, 2025 at 12:00:00

## Caching:

The program stores the fetched data in a local JSON file (<username>_events.json). This prevents unnecessary API calls on subsequent runs, improving performance.

## Error Handling:

If the user is not found, the program will print an error message.
If the GitHub API request fails, an appropriate error message will be shown.