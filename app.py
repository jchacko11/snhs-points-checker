import gspread
client = gspread.service_account(filename='snhs-points-checker-2c4f229c7577.json')


def get_member(id):
    # Get master workbook
    sheet = client.open("Member Database 2020-21").worksheet("Master")

    # Extract and filter by id
    list_of_hashes = sheet.get_all_records()
    member = list(filter(lambda i: i["Student ID"] == int(id), list_of_hashes))[0]

    return member


var = get_member(203046)["Full Name"]
print(var)