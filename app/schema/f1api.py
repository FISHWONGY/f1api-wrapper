from app.schema.base import F1BaseModel


class Drivers(F1BaseModel):
    pos: str | None = None
    driver: str | None = None
    nationality: str | None = None
    car: str | None = None
    pts: float | None = None


class Teams(F1BaseModel):
    pos: str | None = None
    team: str | None = None
    pts: str | None = None
