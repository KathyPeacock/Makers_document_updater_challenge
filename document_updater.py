import os
import shutil
import sys
import re

try:
    testdir = sys.argv[1]
    os.chdir(testdir)
except IndexError:
    print("ERROR: must supply a target directory as an argument")
    exit()

contents = os.listdir()
listfiletype = ""
top = pow(2,6)
try:
    lists_found = 0
    if "droplist" in contents:
        lists_found += 1
        listfiletype = "drop"
    if "allowlist" in contents:
        lists_found += 1
        listfiletype = "allow"
    if lists_found == 2:
        raise OSError
    elif lists_found == 0:
        raise FileNotFoundError
except FileNotFoundError:
    print("ERROR: no droplist nor allowlist found in target directory")
    exit()
except OSError:
    print("ERROR: both droplist and allowlist found in target directory")
    exit()

list_file = open(listfiletype + "list")
list_data = list_file.readlines()
list_file.close()
list_docs = []
chars = re.compile('[^a-zA-Z]')
line = list_data[0] if listfiletype == 'allow' else list_data
for line in list_data:
    list_docs.append(line.strip())

try:
    original_docs = os.listdir("originals")
except FileNotFoundError:
    print("ERROR: originals folder not found in target directory")
    exit()
try:
    update_docs = os.listdir("updates")
except FileNotFoundError:
    print("ERROR: updates folder not found in target directory")
    exit()

errorfile = ""
try:
    for original_doc in original_docs:
        f = open("originals/" + original_doc)
        contents = f.readlines()
        f.close()
        if not (4 <= len(contents) <= 5):
            errorfile = original_doc
            raise OSError
    for update_doc in update_docs:
        f = open("updates/" + update_doc)
        contents = f.readlines()
        f.close()
        if not (4 <= len(contents) <= 5):
            errorfile = update_doc
            raise OSError
except OSError:
    print("ERROR: document \"", errorfile, "\" doesn't contain an appropriately formatted address")
    exit()

if not os.path.exists("finals"):
    os.makedirs("finals")
else:
    final_docs = os.listdir("finals")
    for final_doc in final_docs:
        os.remove("finals/" + final_doc)

if listfiletype == "allow":
    in_update_as_well = False
    not_in_update_as_well = False
    to_drop = []
    for d in original_docs:
        if d in update_docs and d in list_docs:
            in_update_as_well = True
        elif d not in update_docs and d in list_docs:
            not_in_update_as_well = True
            to_drop.append(d)
    if in_update_as_well and not_in_update_as_well:
        for d in to_drop:
            original_docs.remove(d)

if listfiletype == "drop":
    for drop_doc in list_docs.copy():
        if drop_doc in original_docs:
            original_docs.remove(drop_doc)
else:
    for keep_doc in original_docs.copy():
        if keep_doc not in list_docs:
            original_docs.remove(keep_doc)

def blend(orig, update):
    out = []
    for i in range(0, max(len(orig), len(update))):
        if i < len(orig):
            first = orig[i].strip()
        else:
            first = ""
        if i < len(update):
            second = update[i].strip()
        else:
            second = ""
        out.append(second + first[len(second):] + "\n")
    return out

for update_doc in update_docs.copy():
    if update_doc in original_docs:
        if listfiletype == "drop":
            if not os.path.exists("blends"): os.makedirs("blends")
            orig_f = open("originals/" + update_doc)
            orig_data = orig_f.readlines()
            orig_f.close()
            update_f = open("updates/" + update_doc)
            update_data = update_f.readlines()
            update_f.close()
            blended = blend(orig_data, update_data)
            f = open("blends/" + update_doc, "w")
            f.writelines(blended)
            f.close()
            update_docs.remove(update_doc)
            original_docs.remove(update_doc)
        else:
            original_docs.remove(update_doc)

for original_doc in original_docs[:top]:
    shutil.copy("originals/" + original_doc, "finals/" + chars.sub('', original_doc))
for update_doc in update_docs[:top]:
    shutil.copy("updates/" + update_doc, "finals/" + chars.sub('', update_doc))

try:
    blend_docs = os.listdir("blends")
    for blend_doc in blend_docs:
        shutil.copy("blends/" + blend_doc, "finals/" + chars.sub('', blend_doc))
    shutil.rmtree("blends")
except FileNotFoundError:
    pass