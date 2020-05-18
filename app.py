import gspread

client = gspread.service_account(filename='snhs-points-checker-2c4f229c7577.json')
db = client.open("Member Database 2020-21")


def get_member(id):
    # Get master workbook
    sheet = db.worksheet("Master")

    # Extract and filter by id
    list_of_hashes = sheet.get_all_records()
    member = list(filter(lambda i: i["Student ID"] == int(id), list_of_hashes))[0]

    return member


def get_specifics(id, sheet_name='Meeting Attendance'):
    sheet = db.worksheet(sheet_name)
    all_values = sheet.get_all_values()

    # transpose array
    transposed = list(map(list, zip(*all_values)))

    attended_meetings = []

    # look for items where member participated
    for item in transposed:
        if str(id) in item:
            attended_meetings.append(item[0])

    return attended_meetings


print(get_specifics(342899, "Events"))
