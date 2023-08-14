from sqladmin import ModelView

from models import Event


class EventAdmin(ModelView, model=Event):
    column_list = [
        Event.id, Event.name, Event.source, Event.start, Event.end
    ]
