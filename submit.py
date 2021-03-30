from requests_toolbelt import MultipartEncoder
from requests_toolbelt.multipart import encoder
import requests
import json
import os
from os.path import join, isdir, isfile
import fnmatch

#####################################################################################################################################################################
assignment_url = ""
authenticity_token = ""
cookie = ""
#####################################################################################################################################################################

def my_callback(monitor):
    # Your callback function
    pass

def should_exclude(path, patterns):
    skip = False
    for p in patterns:
        if fnmatch.fnmatch(path,p):
            skip = True
            break
    return skip

def get_file_list(working_path, excludes):
    all_files = []
    for root, dirs, files in os.walk(working_path):
        for e in excludes:
            dirs[:] = [ d for d in dirs if not fnmatch.fnmatch(d, e)]

        for f in files:
            if should_exclude(f, excludes):
                continue
            path = join(root, f)
            all_files.append(path.lstrip('./'))
    return all_files
        
if __name__ == "__main__":
    excludes = set(['node_modules','.DS_Store','*.zip','*.sh','*.*.swp', '*.py'])
    fields_list = []
    for f in get_file_list('.', excludes):
        fields_list.append(['submission[files][]', (f, open(f, 'rb'), 'text/plain')])
        print("Added: " + f)
    fields_list.append(['authenticity_token', authenticity_token])
    fields_list.append(['submission[method]', 'upload'])
    e = encoder.MultipartEncoder(
        fields= fields_list
    )
    m = encoder.MultipartEncoderMonitor(e, my_callback)
    url = assignment_url
    headers = {
        'Content-Type': m.content_type,
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": cookie
    }
    r = requests.post(url, data=m,
                    headers=headers)
    # print(r.text)
    print("\n")
    res = json.loads(r.text)
    try:
        errorres = res['error']
        if errorres:
            print("Submission Failed, please check your cookie/authenticity_token")
    except KeyError as e:
        if res["success"]:
                print("Submission Successful!")
                print("Results: " + "https://www.gradescope.com" + str(res["url"]))
        else:
            print("Submission Failed, please check your cookie/authenticity_token")