

from pydantic import BaseModel, ConfigDict


class Exchange(BaseModel):
    model_config = ConfigDict(strict=True)

    result: str
    documentation: str
    terms_of_use: str
    time_last_update_unix: int
    time_last_update_utc: str
    time_next_update_unix: int
    time_next_update_utc: str
    base_code: str
    target_code: str
    conversion_rate: float
