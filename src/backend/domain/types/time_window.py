from typing import TypedDict
import ee

class TimeWindow(TypedDict):
    start: ee.Date
    end: ee.Date
    label: str
