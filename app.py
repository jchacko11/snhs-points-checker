import gspread
from flask import Flask, render_template

client = gspread.service_account(filename='snhs-points-checker-2c4f229c7577.json')
db = client.open("Member Database 2020-21")

app = Flask(__name__)


def get_member(member_id):
    # Get master workbook
    sheet = db.worksheet("Master")

    # Extract and filter by id
    list_of_hashes = sheet.get_all_records()
    member = list(filter(lambda i: i["Student ID"] == int(member_id), list_of_hashes))[0]

    return member


def get_specifics(member_id, sheet_name='Meeting Attendance'):
    sheet = db.worksheet(sheet_name)
    all_values = sheet.get_all_values()

    # transpose array
    transposed = list(map(list, zip(*all_values)))

    attended_meetings = []

    # look for items where member participated
    for item in transposed:
        if str(member_id) in item:
            attended_meetings.append(item[0])

    return attended_meetings


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
