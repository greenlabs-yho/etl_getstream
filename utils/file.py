import os, json

def make_file(dest_dir, mid_dir, file_name, content):
    if not os.path.exists(os.path.join(dest_dir, mid_dir)):
        os.makedirs(os.path.join(dest_dir, mid_dir))

    with open(os.path.join(dest_dir, mid_dir, file_name), 'w') as f:
        if content is str:
            f.write(content)
        elif isinstance(content, dict) or isinstance(content, list):
            json.dump(content, f, indent=4, ensure_ascii=False)