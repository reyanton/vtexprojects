from datetime import date, timedelta

end_prev_month = date.today().replace(day=1) - timedelta(days=1)

ini_prev_month = date.today().replace(day=1) - timedelta(days=end_prev_month.day)

# For printing results
print("First day of prev month:", start_day_of_prev_month)
print("Last day of prev month:", last_day_of_prev_month)