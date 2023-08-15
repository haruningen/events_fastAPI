from sqladmin import ModelView
from sqlalchemy import or_
from sqlalchemy.sql.expression import Select

from models import Event


class EventAdmin(ModelView, model=Event):
    column_sortable_list = [Event.source]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_searchable_list = [Event.source]
    column_list = [
        Event.id, Event.name, Event.source
    ]
    column_details_list = [
        Event.id, Event.name, Event.source, Event.source_id, Event.start, Event.end
    ]

    # TODO fix me
    def search_query(self, stmt: Select, term: str) -> Select:
        return stmt.filter(or_(Event.source == term))

