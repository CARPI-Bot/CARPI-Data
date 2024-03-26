import requests
import datetime
import os

from bs4 import BeautifulSoup

def date_format(date):
    if date.find(" - ") != -1:
        split_date = date.split(" - ")
        return_date = "'"
        return_date += datetime.datetime.strptime(split_date[0], r"%B %d, %Y").strftime(r"%Y-%m-%d")
        return_date += "', '"
        return_date += datetime.datetime.strptime(split_date[1], r"%B %d, %Y").strftime(r"%Y-%m-%d")
        return_date += "'"
    else:
        return_date = "'"
        return_date += datetime.datetime.strptime(date, r"%B %d, %Y").strftime(r"%Y-%m-%d")
        return_date += "', NULL"
    return return_date

if __name__ == "__main__":
    URL = "https://info.rpi.edu/registrar/academic-calendar"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    status_code = 0
    with requests.Session() as session:
        while status_code != 200:
            resp = session.get(
                url = URL,
                headers = HEADERS,
                timeout = 10
            )
            status_code = resp.status_code
            print(f"Response code: {status_code}")
    soup = BeautifulSoup(resp.content, "html5lib")
    calendar_div = soup.find("div", id="academicCalendar")
    assert calendar_div
    year = 1970

    sql_start = "INSERT INTO acad_cal_events (title, date_start, date_end) VALUES\n\t"
    sql_mid_arr = []
    sql_end = ";"

    for month_table in calendar_div.find_all("table", class_="acadcal"):
        assert month_table.thead.text and month_table.tbody
        assert month_table.thead.text.count(" ") == 1
        year = month_table.thead.text.split()[1]
        month_name = month_table.thead.text.split()[0]
        for event in month_table.tbody.find_all("tr"):
            date_cell = event.find("td", class_="date")
            assert date_cell
            anchor = event.find("a")
            assert anchor
            assert anchor["href"]
            event_date = date_cell.text.strip()
            # Replaces unicode right single quotation mark
            event_name = anchor.text.replace("\u2019", "'")
            sql_mid_arr.append("('" + event_name.replace("'", "\\'") + "', " + date_format(event_date) + "),\n\t")
    
    sql_mid = ""
    for event in set(sql_mid_arr):
        sql_mid += event
    sql_mid = sql_mid[:-3]
    with open(os.path.dirname(os.path.abspath(__file__)) + "/data_insertion_sql/acad_cal_insert.sql", "w") as outfile:
        outfile.write(sql_start + sql_mid + sql_end)
