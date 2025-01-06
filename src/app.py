from datetime import datetime

import july
import holidays
import streamlit as st

from optimize import create_days, find_consecutive_days, maximize_pto


if __name__ == "__main__":
    st.set_page_config("Max PTO", page_icon="🌴")
    st.title("🌴 Max PTO")

    cols = st.columns(2)
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 11))
    year = cols[0].selectbox("Select Year", years, index=len(years) // 2)
    pto_hours = cols[1].number_input("PTO Hours", value=80, min_value=1, max_value=52 * 40)

    with cols[0].expander("Work Schedule"):
        monday = st.number_input("Monday", value=8.0, min_value=0.0, max_value=24.0, step=1.0)
        tuesday = st.number_input("Tuesday", value=8.0, min_value=0.0, max_value=24.0, step=1.0)
        wednesday = st.number_input("Wednesday", value=8.0, min_value=0.0, max_value=24.0, step=1.0)
        thursday = st.number_input("Thursday", value=8.0, min_value=0.0, max_value=24.0, step=1.0)
        friday = st.number_input("Friday", value=8.0, min_value=0.0, max_value=24.0, step=1.0)
        saturday = st.number_input("Saturday", value=0.0, min_value=0.0, max_value=24.0, step=1.0)
        sunday = st.number_input("Sunday", value=0.0, min_value=0.0, max_value=24.0, step=1.0)
        work_hours = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    with cols[1].expander("Holiday Schedule"):
        country_holidays = holidays.country_holidays("US", years=year)
        country_holidays_edited = st.data_editor(country_holidays, num_rows="dynamic")

    days = create_days(year, country_holidays_edited, work_hours)
    optimal_pto_days = sorted(maximize_pto(days, pto_hours))

    consecutive_days_off = find_consecutive_days(days)
    pto_taken = sum([i.hours for i in days if i.is_pto])
    total_days_off = sum(len(i) for i in consecutive_days_off)
    msg = f"#### `{int(pto_taken)}` PTO hours taken for a total of `{total_days_off}` days off:\n"
    for cdo in consecutive_days_off:
        msg += f"* Take `{cdo[0]}` to `{cdo[-1]}` for `{len(cdo)}` days off.\n"

    st.markdown(msg)
    st.divider()

    data = []
    for i in days:
        if i.date in optimal_pto_days:
            value = 2
        elif i.date in country_holidays_edited:
            value = 1
        else:
            value = 0
        data.append(value)

    calendar_plot = july.calendar_plot(
        [i.date for i in days], data, weeknum_label=False, date_label=True
    )
    st.pyplot(calendar_plot[0][0].get_figure())
