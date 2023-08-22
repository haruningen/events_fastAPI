# Online event aggregator test project
Create a web page that will display a list of events (meetups, conferences, etc).

A normal user can only view and subscribe to events. If the user goes to an event, the application generate a QR with a link to this event.

Moderator or admin can manually create events and publish. An admin or moderator can make CSV reports on events in the admin panel.

The application in the background (every day at 1 PM) collects information about events using third-party APIs and saves it to the database.

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

## Admin (Powered by SQLAdmin)

http://0.0.0.0:8080/admin

![](https://github.com/haruningen/events_fastAPI/blob/main/demo/admin.png)

## Swagger

http://0.0.0.0:8080/docs#/

![](https://github.com/haruningen/events_fastAPI/blob/main/demo/swagger.png)
