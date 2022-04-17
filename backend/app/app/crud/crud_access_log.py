from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.access_log import AccessLog
from app.schemas.access_log import AccessLogCreate, AccessLogUpdate


class CRUDAccessLog(CRUDBase[AccessLog, AccessLogCreate, AccessLogUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        event_id: int,
        skip: int = 0,
        limit: int = 100,
        given_by_id: int = None,
        received_id: int = None,
    ) -> List[AccessLog]:
        if given_by_id and received_id:
            return (
                db.query(self.model)
                .filter(
                    AccessLog.event_id == event_id,
                    AccessLog.given_by_id == given_by_id,
                    AccessLog.received_id == received_id,
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
        elif given_by_id:
            return (
                db.query(self.model)
                .filter(
                    AccessLog.event_id == event_id,
                    AccessLog.given_by_id == given_by_id,
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
        elif received_id:
            return (
                db.query(self.model)
                .filter(
                    AccessLog.event_id == event_id,
                    AccessLog.received_id == received_id,
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
        return (
            db.query(self.model)
            .filter(AccessLog.event_id == event_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


access_log = CRUDAccessLog(AccessLog)
