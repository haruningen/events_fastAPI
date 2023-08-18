from sqladmin import ModelView

from models import DataSource


class DataSourceAdmin(ModelView, model=DataSource):
    can_export = False
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        DataSource.id, DataSource.name
    ]
    column_details_list = [
        DataSource.id, DataSource.name, DataSource.handler, DataSource.secret, DataSource.api_url, DataSource.config
    ]
