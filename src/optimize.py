from datetime import date, timedelta
from operator import add, sub

class Day:
    def __init__(self, date, work_hours, country_holidays):
        self.date = date
        self.is_weekday = date.weekday() < 5
        self.is_holiday = date in country_holidays
        self.hours = work_hours[date.weekday()]
        self.is_workday = self.hours > 0 and not self.is_holiday
        self.is_pto = False


def find_gaps(days, operator=add):
    gaps = []
    for i, day in enumerate(days):
        if day.is_holiday:
            gap = []
            for j in range(1, 5):
                other_day = days[operator(i, j)]
                if other_day.is_workday:
                    gap.append(other_day)
                else:
                    break

            if len(gap) > 0:
                gaps.append(gap)

    return gaps


def maximize_pto(days, total_pto_hours):
    remaining_pto = total_pto_hours
    pto_days = []

    gaps = sorted(find_gaps(days) + find_gaps(days, operator=sub), key=len)
    for gap in gaps:
        gap_hours = sum([day.hours for day in gap])
        if gap_hours <= remaining_pto:
            for day in gap:
                day.is_pto = True
                pto_days.append(day.date)
                remaining_pto -= day.hours

    remaining_days = [day for day in days if day.is_workday and not day.is_pto]
    sorted_days = sorted(remaining_days, key=lambda d: (d.hours, d.date.weekday() == 4))

    for i, day in enumerate(sorted_days):
       if remaining_pto >= day.hours:
            if i + 1 < len(days) and i - 1 >= 0:
                next_day = days[i + 1]
                prev_day = days[i - 1]

                if not prev_day.is_workday or not next_day.is_workday:
                    day.is_pto = True
                    pto_days.append(day.date)
                    remaining_pto -= day.hours

    return pto_days


def find_consecutive_days(days):
    consecutive_days_off = []
    current_streak = []

    for day in days:
        if not day.is_workday or day.is_pto or day.is_holiday:
            current_streak.append(day.date)
        else:
            if current_streak:
                consecutive_days_off.append(current_streak)
                current_streak = []

    if current_streak:
        consecutive_days_off.append(current_streak)

    return [i for i in consecutive_days_off if len(i) > 2]


def create_days(year, holidays, work_hours):
    start_dt = date(year, 1, 1)
    end_dt = date(year + 1, 1, 1)

    days = []
    for i in range((end_dt - start_dt).days):
        dt = start_dt + timedelta(days=i)
        days.append(Day(dt, work_hours, holidays))

    return days
