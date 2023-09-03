"""
Models
"""
from pydantic import BaseModel, Field


class Event(BaseModel):
    """
    Event to listen type and code to listen to
    In Linux: include/uapi/linux/input-event-codes.h
    """

    type: str = Field(description="Event Type")
    code: str = Field(description="Event Code")


class Mapping(BaseModel):
    """
    Mappings between the linux event codes and the remote code values
    """

    event_code: str
    remote_value: int = Field(description="The Event Value")
    description: str


class MappingDefinition(BaseModel):
    """
    Remote to Linux Event Mapping
    """

    name: str
    description: str
    event: Event
    mappings: list[Mapping]
