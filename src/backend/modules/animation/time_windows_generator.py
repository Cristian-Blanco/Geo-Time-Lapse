from backend.domain.types.time_window import TimeWindow
import ee

class TimeWindowGenerator:

    @staticmethod
    def generate(start_date: str, end_date: str, interval_months: int) -> list[TimeWindow]:
        start = ee.Date(start_date)
        end = ee.Date(end_date)

        windows: list[TimeWindow] = []
        current = start
        current_end = current.advance(interval_months, "month")

        while current_end.millis().lte(end.millis()).getInfo():
            windows.append({
                "start": current,
                "end": current_end,
                "label": f"{current.format('YYYY-MM').getInfo()}_{current_end.format('YYYY-MM').getInfo()}"
            })

            current = current_end
            current_end = current.advance(interval_months, "month")

        return windows
