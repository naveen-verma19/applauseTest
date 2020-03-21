import json
import string
import time
from tabulate import tabulate

from myfibheap import fheappush, makefheap


def shorten(url):
    url = url.strip()
    if url in original_processed_urls:
        print("\nalready processed url", url, "IGNORING IT")
        return
    last_code = ""
    with open("last_code_used.txt", 'r') as f2:
        x = f2.read().strip()
        if x != "":
            last_code = x
    f_urls = open("last_code_used.txt", 'w')

    if last_code != "":  # abdghj12  #999abc
        print("\nProcessing url", url)
        good_index = len(last_code) - 1
        while last_code[good_index] == alphabets[-1]:
            good_index -= 1
            if good_index == -1:
                break
        if good_index == -1:
            # INDEX IS FULL..REACHED VOCABULARY LIMIT
            old_node = heap1.extract_min()
            key = old_node.key
            code = key[3]

            print("Dictionary full, overwriting oldest accessed url", key[1], "with access code", code)
            # OVERWRITING URL
            original_processed_urls.remove(key[1])
            tup = [time.time(), url, 1, code]
            nodeInserted = fheappush(heap1, tup)
            url_dict[code] = nodeInserted
            f_urls.write(last_code)
        else:
            # THERE IS STILL SPACE...INSERT NEW URL
            this_char = last_code[good_index]
            next_char = alphabets[alphabets.index(this_char) + 1]
            new_list = list(last_code)
            new_list[good_index] = next_char
            for i in range(good_index + 1, len(new_list)):
                new_list[i] = alphabets[0]  # azz->baa
            next_code = "".join(new_list)
            print("code", next_code)
            tup = [time.time(), url, 1, next_code]
            node = fheappush(heap1, tup)
            url_dict[next_code] = node
            f_urls.write(next_code)
    else:
        print("first url")
        next_code = alphabets[0] + alphabets[0]
        print("code", next_code)
        tup = [time.time(), url, 1, next_code]
        node = fheappush(heap1, tup)
        url_dict[next_code] = node
        f_urls.write(next_code)

    f_urls.close()
    original_processed_urls.add(url)


def retrieve(shortened_url):
    print("retrieving", shortened_url)
    code = shortened_url[-2:]
    if code in url_dict:
        old_node = url_dict[code]
        key = old_node.key
        heap1.delete(old_node)
        key[0] = time.time()
        key[2] += 1
        node_new = fheappush(heap1, key)
        url_dict[code] = node_new
        return key[1]


def get_dict():
    json_format_dict = {}
    for k, v in url_dict.items():
        json_format_dict[k] = {
            "last_accessed_time": v.key[0],
            "original_url": v.key[1],
            "access_counts": v.key[2]
        }
    return json_format_dict


def show_all_urls():
    json_format_dict = get_dict()
    json_format_dict = {k: v for k, v in
                        sorted(json_format_dict.items(), key=lambda item: item[1]["access_counts"], reverse=True)}
    print("All stored urls SORTED BY CALL COUNTS(DESC)")
    lili=[["Shortened_URL","ORIGINAL_URL","CALL_COUNTS(DESC)","LAST_ACCESSED_TIME(ms)"]]
    for k, v in json_format_dict.items():
        # print("shortened_url: ", k, "original_url: ", v["original_url"], "call_count", v["access_counts"],
        #       "last_access_time", v["last_accessed_time"])
        li=[k,v["original_url"],v["access_counts"],v["last_accessed_time"]]
        lili.append(li)
    print(tabulate(lili))


if __name__ == "__main__":

    #################RETRIEVING CACHE #######################
    url_dict = {}
    original_processed_urls = set()
    heap1 = makefheap()
    with open("shortened_urls.json", 'r') as f:
        if f.read().strip() != "":
            f.seek(0)
            url_dict_loaded = json.load(f)
            for k, v in url_dict_loaded.items():
                tup = [v["last_accessed_time"], v["original_url"], v["access_counts"], k]
                node = fheappush(heap1, tup)
                url_dict[k] = node
                original_processed_urls.add(v["original_url"])

    alphabets = list(string.ascii_uppercase) + list(string.ascii_lowercase) + list(map(lambda x: str(x), range(0, 10)))
    char_length = len(alphabets)

    ############ OPERATION COMMANDS here link SHORTEN RETRIEVE #################
    test_urls = open("test_urls.txt", 'r').read().split("\n")
    for u in test_urls[0:50]:
        shorten(u)
    print(retrieve("bit.ly/Aa"))
    print(retrieve("bit.ly/Aa"))
    print(retrieve("bit.ly/AD"))
    print(retrieve("bit.ly/Ar"))
    print(retrieve("bit.ly/A1"))
    for u in test_urls[51:]:
        shorten(u)
    show_all_urls()
    # ADD MORE COMMANDS HERE
    ##################### POST OPERATION SAVING CACHE #################
    # All operations finished dumping json file
    json_format_dict = get_dict()

    json_format_dict = {k: v for k, v in
                        sorted(json_format_dict.items(), key=lambda item: item[1]["last_accessed_time"], reverse=True)}
    with open("shortened_urls.json", 'w') as shortened_url_file:
        json.dump(json_format_dict, shortened_url_file)
