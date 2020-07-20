import json
import glob
from tqdm import tqdm
from pprint import pprint
import random 


MESSAGES = []
files = glob.glob("./conv_messages/message_*.json")


def open_bad_word_dict():
    with open('badword.txt') as bad_word_file:
        return bad_word_file.read().split('\n')


def create_messages_list():
    m = []
    for f in files:
        with open(f) as json_file:
            data = json.load(json_file)
            m.extend(data['messages'])
    return m

def find_messages(bad_word, messages):
    res = []
    for m in tqdm(messages):
        if m['type'] == "Generic" and "content" in m:
            msg = m["content"]
            matches = []
            for word in bad_word:
                if word != "" and msg.find(" " + word + " ") > 0:
                    matches.append(word)
            if len(matches) > 0:
                res.append(
                    {
                        "msg": msg,
                        "matches": matches,
                        "author": m["sender_name"]
                    })
    return res


def print_message(m):
    print(m["msg"].encode('latin1').decode('utf8'))
    print(m["author"])
    print(m["matches"])



if __name__ == "__main__":
    bad_word = open_bad_word_dict()
    messages = create_messages_list()
    print("{} messages found".format(len(messages)))
    resutats = find_messages(bad_word, messages)
    print("{} messages found containing bad word".format(len(resutats)))


    print_message(random.choice(resutats))
    while True:
        input("an other message ?")
        print_message(random.choice(resutats))
