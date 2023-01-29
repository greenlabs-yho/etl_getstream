import json, logging, os
from datetime import datetime
from module.extract_handler import extract
from module.translate_handler import translate
from module.export_handler import export_gsheet, print_worksheet

CHAT_STREAM_KEY = 'KEY'
CHAT_STREAM_SECRET = 'SECRET'
GCP_CREDENTIAL_FILE_PATH = 'PATH'
GSHEET_NAME = "SHEET_NAME"
GSHEET_COLUMN_LIST = ["채팅 ID", "채팅 owner", "채팅 member", "판매글 등록", "판매글 등록 user", "판매글 구분", "판매글 제목", "대화 user", "대화 시점", "대화 종류", "대화 내용"]

CHAT_LIST_PATH = "./test/chat_list.json"
EXTRACT_PATH = "./test/extract"
TRANSLATE_PATH = "./test/translate"
EXPORT_PATH = "./test/export"
LOG_PATH = "./log"


def main():
    logging.info("## check chat list ##")
    if not os.path.exists(CHAT_LIST_PATH):
        raise Exception("not exists chat list json file")

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)


    logging.info('## loading check list ##')    
    with open(CHAT_LIST_PATH, 'r') as f:
        chat_list = json.load(f) 
    
    
    extract_list = extract(chat_list, EXTRACT_PATH, {'KEY': CHAT_STREAM_KEY, 'SECRET': CHAT_STREAM_SECRET})
    translate_list = translate(extract_list, EXTRACT_PATH, TRANSLATE_PATH)
    export_gsheet(translate_list, TRANSLATE_PATH, EXPORT_PATH, GCP_CREDENTIAL_FILE_PATH, GSHEET_NAME, GSHEET_COLUMN_LIST)



if __name__ == "__main__":
    logging.basicConfig(filename=os.path.join(LOG_PATH, datetime.now().strftime("%Y%m%d_%H%M%S")), 
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]\t%(message)s', 
                    datefmt='%Y/%m/%d %H:%M:%S')
    main()