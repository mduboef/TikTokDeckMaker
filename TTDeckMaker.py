# python3 TTDeckMaker.py "input.csv" brandName nonapp 30 

import sys
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class Post:
    def __init__(self, name, month, day, pType, views, clicks, conversions, cost):
        self.name = name
        self.month = month
        self.day = day
        self.pType = pType
        self.views = views
        self.clicks = clicks
        self.conversions = conversions
        self.cost = cost


def parseAdGroup(post, str):
    # find name
    i = len(str)-1
    while str[i] != '|':
        i -= 1
    if(str[len(str)-1] != '|'):
        post.name = str[i+1:]

    # find month
    i = 0
    while str[i] != '.':
        i += 1
    if i-2 >= 0:
        if str[i-2].isdigit():               # 2 digit month
            post.month = int(str[i-2:i])
        else:                               # 1 digit month
            post.month = int(str[i-1])
    else:
        post.month = int(str[i-1])

    # find day
    if str[i+2].isdigit():                   # 2 digit day
        post.day = int(str[i+1:i+3])
    else:                                   # 1 digit day
        post.day = int(str[i+1])

    print("PARSED    Date:", post.month, '.', post.day, "    Type:", post.pType, "    Name:", post.name)

# ! TODO: CHANGE TO INSERT THEN CELL UPDATE
def printToSheet(post, cut, vidCount, sheet):
    # first line
    if(vidCount == 1):
        sheet.update_cell(8, 2, post.name)
        if(post.pType == 0):
            sheet.update_cell(8, 3, "Entertainment")
        else:
            sheet.update_cell(8, 3, "Product")
        sheet.update_cell(8, 5, str(post.month)+'/'+str(post.day))
        sheet.update_cell(8, 6, post.views)
        sheet.update_cell(8, 8, post.clicks)
        sheet.update_cell(8, 9, post.conversions)
        if post.clicks > 0:
            sheet.update_cell(8, 10, (post.cost/post.clicks)/cut)
        else:
            sheet.update_cell(8, 10, '-')
        if post.conversions > 0:
            sheet.update_cell(8, 11, (post.cost/post.conversions)/cut)
        else:
            sheet.update_cell(8, 11, '-')

    else:
        if post.pType == 0:
            newRow = ['', post.name, "Entertainment", "", str(post.month)+'/'+str(post.day), post.views, ""]
        else:
            if post.clicks == 0:
                newRow = ['', post.name, "Product", "", str(post.month)+'/'+str(post.day), post.views, "", 0, 0, '-', '-']
            else:
                if post.conversions == 0:
                    newRow = ['', post.name, "Product", "", str(post.month)+'/'+str(post.day), post.views, "", post.clicks, 0, (post.cost/post.clicks)/cut, '-']
                else:
                    newRow = ['', post.name, "Product", "", str(post.month)+'/'+str(post.day), post.views, "", post.clicks, post.conversions, (post.cost/post.clicks)/cut, (post.cost/post.conversions)/cut]                    

        sheet.insert_row(newRow, 7+vidCount)

# ! TODO: PLACE LAST LINE IN LAST ROW
def emptyLastRow(vCount):
    pass

# ! TODO: SLACK BOT
# ! TODO: EMAIL SCAN DAILY VERSION

# auththorize Google Sheets API & open sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("AutodeckTest").sheet1          # ! TODO: DUPLICATE SHEET1

# data = sheet.get_all_records()
# row = sheet.row_values(2)
# col = sheet.col_values(2)
# cell = sheet.cell(2,2).value
# insertRow = ["", 1, 2, "Sat", 6.5]
# sheet.insert_row(insertRow, 9)
# sheet.delete_row(4)
# sheet.update_cell(3,8, "Found")





# print(sys.argv)

# set varibles from command line args
brandName = sys.argv[2]
if("app" == sys.argv[3]):
    appBool = True
else:
    appBool = False
cut = (100-int(sys.argv[4]))/100
print(cut)
vidCount = -1

# open csv from TT
with open(sys.argv[1], 'r') as csv_file:
    csvReader = csv.reader(csv_file)

    for line in csvReader:

        if vidCount != -1:
            # if money spent & not follower
            if float(line[2]) > 0 and not("Follower" in line[0] or "Engagement" in line[0]):
                post = Post("NULL", -1, -1, -1, 0, 0, 0, -1)
                # CONVERSIONS
                if("Conversion" in line[0] or "Product" in line[0] or "Install" in line[0]):
                    post.pType = 1
                # FOLLOWERS
                elif("Follower" in line[0] or "Engagement" in line[0]):
                    post.pType = 2
                # ENTERTAINMENT
                else:
                    post.pType = 0

                parseAdGroup(post, line[1])
                post.cost = float(line[2])
                post.views = int(line[5])
                post.clicks = int(line[6])
                post.conversions = int(line[7])

                vidCount += 1

                printToSheet(post, cut, vidCount, sheet)
        else:
            vidCount = 0

print(vidCount)