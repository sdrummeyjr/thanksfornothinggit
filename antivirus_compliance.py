from datetime import datetime
# import pandas as pd


current_dt = datetime.now()
if current_dt.month == 1:
    previous_month = current_dt.replace(month=12)
else:
    previous_month = current_dt.replace(month=current_dt.month - 1)

# reporting_month = datetime.now()

print(previous_month.month)
