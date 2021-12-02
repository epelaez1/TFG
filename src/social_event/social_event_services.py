from datetime import datetime

from src.social_event.domain.social_event import SocialEvent
from src.social_event.domain.social_event_repository import SocialEventRepository


def create(  # noqa: WPS211 Too many arguments
    venue_id: str,
    name: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    social_event_repository: SocialEventRepository,
) -> str:
    social_event = SocialEvent(
        venue_id=venue_id,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
    )
    social_event_repository.add(social_event)
    return str(social_event.id)


def get(social_event_id: str, social_event_repository: SocialEventRepository) -> SocialEvent:
    return social_event_repository.get(social_event_id)
