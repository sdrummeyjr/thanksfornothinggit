from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

# todo build in logs
# https://stackoverflow.com/questions/3383865/how-to-log-error-to-file-and-not-fail-on-exception

"""
https://www.microsoft.com/en-us/wdsi/definitions/antimalware-definition-release-notes

id=comboVersionList
id="dropDownOption_0" through _19

p tag id=releaseDate_0 through _19
"""

url = "https://www.microsoft.com/en-us/wdsi/definitions/antimalware-definition-release-notes"

req = Request(url, headers={'User-Agent': 'Chrome'})
html = urlopen(req).read()
bs = BeautifulSoup(html, 'html.parser')

version = bs.find('ul', {'id': 'comboVersionList'}).get_text(',', strip=True).split(',')

# id=releaseDate_0 through releaseDate_19
date_tag_id = [f"releaseDate_{item}" for item in range(0, 20)]

dates = pd.Series([bs.find('p', {'id': thing}).get_text() for thing in date_tag_id])

df = pd.DataFrame({
    'Version': version,
    'Date (UTC)': pd.to_datetime(dates),
    'Date (EST)': pd.to_datetime(dates, utc=True).dt.tz_convert('US/Eastern').dt.tz_localize(None),
    'Date (CEN)': pd.to_datetime(dates, utc=True).dt.tz_convert('US/Central').dt.tz_localize(None)
}, columns=["Version", "Date (UTC)", "Date (EST)", "Date (CEN)"])

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html

df2 = pd.read_excel("try.xlsx")

df3 = pd.concat([df2, df]).drop_duplicates(subset="Version")
df3 = df3.sort_values("Date (UTC)")
print(df3)

with pd.ExcelWriter("try2.xlsx") as writer:
    try:
        df3.to_excel(writer, index=False, freeze_panes=(1, 0))
        writer.save()
    except Exception as err:
        print(err)
