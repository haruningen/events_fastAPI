# Online event aggregator test project
Create a web page that will display a list of events (meetups, conferences, etc).

A normal user can only view and subscribe to events. If the user goes to an event, the application generate a QR with a link to this event.

Moderator or admin can manually create events and publish. An admin or moderator can make two types of reports in the admin panel: CSV on events. The second report is in PDF format and reflect information about the number of events for the period (how many of them were visited and how many times).

The application in the background (once a day) collects information about events using third-party APIs and saves it to the database.

# Demo

![](https://github.com/haruningen/events_fastAPI/blob/main/demo/admin_demo.gif)

## Tech stack
- Python 3.11
- FastApi
- SqlAlchemy 1.4
- PyTest
- Poetry

## Foreign components 
- PostgreSQL

## You need to add a datasource to the table!
### Data source for load events background task:
1. [Ticketmaster developer](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/)

Handler: data.TicketmasterDataHandler

2. [PredictHQ](https://www.predicthq.com/support/getting-started-with-api)

Handler: data.PredictHQDataHandler

## To build and run:
```bash
make build
make migrate
make start
```

# Frontend

You can find an example site [here](https://github.com/haruningen/events_test/tree/fastAPI)

## Swagger

![](https://github.com/haruningen/events_fastAPI/blob/main/demo/swagger.png)
