from datetime import date, timedelta


class Day:
    def __init__(self, date, work_hours, country_holidays):
        self.date = date
        self.is_weekday = date.weekday() < 5
        self.is_holiday = date in country_holidays
        self.is_workday = self.is_weekday and not self.is_holiday
        self.hours = work_hours[date.weekday()] if self.is_workday else 0
        self.is_pto = False


def maximize_pto(days, total_pto_hours, holidays):
    remaining_pto = total_pto_hours
    pto_days = []

    sorted_days = sorted(
        [day for day in days if day.is_workday],
        key=lambda d: (
            d.date - timedelta(days=1) in holidays
            or d.date + timedelta(days=1) in holidays,  # Next to a holiday
            d.date.weekday() == 4,  # Fridays (for long weekends)
            d.hours,  # Lower-hour workdays first
        ),
        reverse=True,  # Higher priority first
    )

    for i, day in enumerate(sorted_days):
        if remaining_pto <= 0:
            break

        if not day.is_pto and remaining_pto >= day.hours:
            if i + 1 < len(days) and i - 1 >= 0:
                next_day = days[i + 1]
                prev_day = days[i - 1]

                if not prev_day.is_workday or not next_day.is_workday:
                    day.is_pto = True
                    pto_days.append(day.date)
                    remaining_pto -= day.hours

    return pto_days


def create_days(year, holidays, work_hours):
    start_dt = date(year, 1, 1)
    end_dt = date(year + 1, 1, 1)

    days = []
    for i in range((end_dt - start_dt).days):
        dt = start_dt + timedelta(days=i)
        days.append(Day(dt, work_hours, holidays))

    return days
