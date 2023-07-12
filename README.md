# Online event aggregator test project
Create a web page that will display a list of events (meetups, conferences, etc).

A normal user can only view and subscribe to events. If the user goes to an event, the application generate a QR with a link to this event.

Moderator or admin can manually create events and publish. An admin or moderator can make two types of reports in the admin panel: CSV on events. The second report is in PDF format and reflect information about the number of events for the period (how many of them were visited and how many times).

The application in the background (once a day) collects information about events using third-party APIs and saves it to the database.

## Tech stack
- python 3.11
- fastApi
- SqlAlchemy 1.4.31

## Foreign components 
- postgres

## To build and run:
```bash
make build
make migrate
make start
```