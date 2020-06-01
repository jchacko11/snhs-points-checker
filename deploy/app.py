import gspread
from flask import Flask, render_template, request
import pathlib

filepath = pathlib.Path().absolute()
if filepath == "/app":
    client = gspread.service_account(filename="/app/snhs-points-checker-2c4f229c7577.json")
else:
    client = gspread.service_account(filename="snhs-points-checker-2c4f229c7577.json")

db = client.open("Member Database 2020-21")

app = Flask(__name__)


def get_member(member_id):
    # Get master workbook
    sheet = db.worksheet("Master")

    # Extract and filter by id
    list_of_hashes = sheet.get_all_records()
    try:
        member = list(filter(lambda i: i["Student ID"] == int(member_id), list_of_hashes))[0]
        return member
    except:
        return False


# returns an array of strings with the point output for a category
def get_specifics(member_id, sheet_name='Meeting Attendance'):
    sheet = db.worksheet(sheet_name)
    all_values = sheet.get_all_values()

    # transpose array
    transposed = list(map(list, zip(*all_values)))

    attended_meetings = []
    attended_meetings_weight = []
    modified_meetings = []

    # look for items where member participated
    for item in transposed:
        if str(member_id) in item:
            attended_meetings.append(item[0])
            attended_meetings_weight.append(item[1])

    for i in range(len(attended_meetings)):
        if attended_meetings_weight and attended_meetings_weight != 10:
            modified_meetings.append(attended_meetings[i] + " (" + attended_meetings_weight[i] + " points)")
        else:
            modified_meetings.append(attended_meetings[i])

    return modified_meetings


# gets the number of requested points
def get_requested(member_id):
    sheet = db.worksheet('Master')
    all_values = sheet.get_all_records()

    for record in all_values:
        if record['Student ID'] == member_id:
            return record['Points Request']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/member')
def member_data():
    try:
        member_id = int(request.args["member_id"])
    except:
        return render_template("index.html", valid=False)

    member = get_member(member_id)

    sheets = ['Meeting Attendance', 'Events', 'Shirts', 'Other']

    # populate array with get_specifics for each sheet
    sheet_info_array = list(map(lambda sheet: get_specifics(member_id, sheet_name=sheet), sheets))

    # combine all arrays
    member_details = []
    [member_details.extend(details) for details in sheet_info_array]

    # add special case for requested points
    requested_points = get_requested(member_id)
    if requested_points:
        member_details.append("Points Request (" + str(get_requested(member_id)) + " points)")

    if member is not False:
        return render_template("index.html", member=member, member_details=member_details, valid=True)
    else:
        return render_template("index.html", valid=False)


if __name__ == '__main__':
    app.run()
