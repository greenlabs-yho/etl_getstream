import json, os, time, logging, traceback
from stream_chat import StreamChat
from utils.file import make_file


def extract(chat_list : list, dest_path : str, credentials : dict):
    logging.info("### start extract ###")
    client = StreamChat(api_key=credentials['KEY'], api_secret=credentials['SECRET'])

    success_list = []
    for i, chat_info in enumerate(chat_list):
        cid = chat_info['chat_channel_id']
        file_name = f'{cid}.json'
        try :
            result = client.query_channels(
                {"cid": cid}
            )

            time.sleep(0.05)
            make_file(dest_path, '', file_name, result)
            
            success_list.append(chat_info)
        except Exception as e:
            logging.error(f'cid : {cid}')
            make_file(dest_path, 'fail', file_name, traceback.format_exc())
            

        if ((i+1)%100) == 0:
            logging.info(f'[{i+1}/{len(chat_list)}] 작업 진행중')

    return success_list