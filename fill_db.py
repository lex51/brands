import openpyxl
import json
import requests

xlsx_file = "data.xlsx"
wb_obj = openpyxl.load_workbook(xlsx_file)

# Read the active sheet:
sheet = wb_obj.active

for row in sheet.iter_rows(1):
    print(row[0].value, row[1].value, row[2].value)

    r = requests.post(
        "http://127.0.0.1:8002/save_item",
        json.dumps(
            {
                "articul": row[0].value,
                "strategy": row[1].value,
                "participants": row[2].value,
            }
        ),
    )
    print(r.status_code)
