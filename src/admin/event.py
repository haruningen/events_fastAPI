from typing import Any, Generator, List, Optional

from sqladmin import ModelView
from sqladmin.helpers import Writer, secure_filename, stream_to_csv
from sqladmin.pagination import Pagination
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import select
from starlette.responses import StreamingResponse

from models import Event


class EventAdmin(ModelView, model=Event):
    source: Optional[str] = None

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

    def _export_csv(
            self,
            data: List[Any],
    ) -> StreamingResponse:
        def generate(writer: Writer) -> Generator[Any, None, None]:
            # Append the column titles at the beginning
            yield writer.writerow(self._export_prop_names)

            for row in data:
                if self.source:
                    if row.source == self.source:
                        vals = [
                            str(self.get_prop_value(row, name))
                            for name in self._export_prop_names
                        ]
                        yield writer.writerow(vals)
                else:
                    vals = [
                        str(self.get_prop_value(row, name))
                        for name in self._export_prop_names
                    ]
                    yield writer.writerow(vals)

        filename = secure_filename(self.get_export_name(export_type="csv"))

        return StreamingResponse(
            content=stream_to_csv(generate),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"},
        )

    async def list(
        self,
        page: int,
        page_size: int,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort: str = "asc",
    ) -> Pagination:
        page_size = min(page_size or self.page_size, max(self.page_size_options))
        stmt = self.list_query

        for relation in self._list_relations:
            stmt = stmt.options(joinedload(relation))

        if sort_by:
            sort_fields = [(sort_by, sort == "desc")]
        else:
            sort_fields = self._get_default_sort()

        for sort_field, is_desc in sort_fields:
            if is_desc:
                stmt = stmt.order_by(desc(sort_field))
            else:
                stmt = stmt.order_by(asc(sort_field))

        if search:
            self.source = search
            stmt = self.search_query(stmt=stmt, term=search)
            count = await self.count(select(func.count()).select_from(stmt))  # type: ignore
        else:
            self.source = None
            count = await self.count()

        stmt = stmt.limit(page_size).offset((page - 1) * page_size)
        rows = await self._run_query(stmt)

        pagination = Pagination(
            rows=rows,
            page=page,
            page_size=page_size,
            count=count,
        )

        return pagination
