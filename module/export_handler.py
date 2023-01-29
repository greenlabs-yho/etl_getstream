import os, json, traceback, csv, logging
from utils.file import make_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json, time, traceback, csv
from datetime import datetime, timedelta, timezone


def export_csv(chat_info, source_path, dest_path):
    try:
        cid = chat_info['chat_channel_id']
        file_name = f'{cid}.json'
        with open(os.path.join(source_path, file_name), 'r') as f:
            msg_list = json.load(f)

        ym = msg_list[0]['post_created_at'][:7]
        with open(f"{dest_path}/{ym}.csv", "a") as csv_file:
            writer = csv.DictWriter(csv_file, list(msg_list[0].keys()))
            for loop, msg in enumerate(msg_list):
                writer.writerow(msg)

            writer.writerow({key:'' for key in msg.keys()})
    except:
        logging.error(f'cid: {cid}')
        make_file(dest_path, 'fail', file_name, traceback.format_exc())


def upload_googlesheet(source_path, gcp_credential_path, gsheet_name, gsheet_column_list):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcp_credential_path, scope)
    gc = gspread.authorize(credentials).open(gsheet_name)


    ws_dict = {ws.title: ws for ws in gc.worksheets()}
    file_list = [file for file in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, file))]
    file_list.sort()
    for file in file_list:
        with open(os.path.join(source_path, file), 'r') as f:
            sheet_name = file.split('.')[0]
            if sheet_name not in ws_dict:
                sheet = gc.add_worksheet(sheet_name, 2, 20)
                ws_dict[sheet_name] = sheet
            else:
                sheet = ws_dict[sheet_name]
            sheet.append_row(gsheet_column_list)
            time.sleep(1)

            gc.values_append(
                sheet_name,
                params={'valueInputOption': 'USER_ENTERED'},
                body={'values': list(csv.reader(f))}
            )


def export_gsheet(chat_list, source_path, dest_path, gcp_credential_path, gsheet_name, gsheet_column_list):
    logging.info("### start export csv ###")

    for i, chat_info in enumerate(chat_list):
        export_csv(chat_info, source_path, dest_path)
            
        if ((i+1)%100) == 0:
            logging.info(f'[{i+1}/{len(chat_list)}] 작업 진행중')

    logging.info("### start export gsheet ###")
    upload_googlesheet(dest_path, gcp_credential_path, gsheet_name, gsheet_column_list)
    
