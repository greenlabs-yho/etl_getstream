import os, json, traceback, logging
from datetime import datetime, timedelta
from utils.file import make_file
timedelta_kst = timedelta(hours=9)



def translate_json(chat_info, source_file_path, dest_dir):
    with open(source_file_path, 'r') as f:
        j_data = json.load(f)

    file_name = os.path.basename(source_file_path)
    cid = chat_info['chat_channel_id']
    
    try:
        channel = j_data['channels'][0]['channel']
        if channel['cid'] != cid:
            raise Exception(f"different file - file_name : {cid} / file_content : {channel['cid']}")
    
        if len(j_data['channels'][0]['messages']) == 0:
            raise Exception(f"not exists chat messages")

        owner = []
        member = []
        for j_member in j_data['channels'][0]['members']:
            if j_member['role'] == 'owner':
                owner.append((j_member['user']['id'], j_member['user']['name']))
            else:
                member.append((j_member['user']['id'], j_member['user']['name']))

        body_list = []
        body = {}
        body['channel'] = cid
        body['owner'] = str(tuple(owner[0])) if len(owner) == 1 else str([tuple(u) for u in owner])
        body['member'] = str(tuple(member[0])) if len(member) == 1 else str([tuple(u) for u in member])
        body['post_created_at'] = (datetime.strptime(chat_info['created_at'], '%Y-%m-%d %H:%M:%S') + timedelta_kst).strftime('%Y-%m-%d')
        body['post_user'] = chat_info['user_id']
        body['post_type'] = chat_info['name']
        body['title'] = chat_info['title']

        for msg in j_data['channels'][0]['messages']:
            body['message_user'] = msg['user']['name']
            body['message_time'] = msg['created_at']
            body['message_type'] = msg['type']
            body['message'] = msg['text']
            body_list.append(body.copy())

        make_file(dest_dir, '', file_name, body_list)
        return True
    except :
        logging.error(f'cid: {cid}')
        make_file(dest_dir, 'fail', file_name, traceback.format_exc())
        return False



def translate(chat_list, source_path, dest_path):
    logging.info("### start translate ###")
    success_list = []
    for i, chat_info in enumerate(chat_list):
        if translate_json(chat_info, os.path.join(source_path, chat_info['chat_channel_id'] + '.json'), dest_path):
            success_list.append(chat_info)

        if ((i+1)%100) == 0:
            logging.info(f'[{i+1}/{len(chat_list)}] 작업 진행중')

    return success_list