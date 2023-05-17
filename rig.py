import optparse
from requests import get
import os
from PIL import Image
import io
import random

'''
"RIG": Retrieve Images on Google
'''

rig_path = os.path.dirname(os.path.abspath(__file__))
dirs = os.listdir(".")

def check_tracking():
    tracking_key = ".rig"
    is_tracking = False
    track_key = None
    for key in dirs:
        if key[:5] == ".rigs":
            tracking_key = key
            is_tracking = True
            track_key = key
    
    tracked = []
    for bucket in os.listdir(rig_path):
        try:
            if tracking_key in os.listdir(bucket):
                tracked.append(bucket)
        except: pass
    return tracked, track_key, is_tracking

tracking = check_tracking()

def account():
    for bucket in tracking[0]:
        if tracking[2]:
            print(f"Number of {bucket} Images: " + str(len(os.listdir(os.path.join(rig_path, bucket))) - 2))
        else:
            print(f"Number of {bucket} Images: " + str(len(os.listdir(os.path.join(rig_path, bucket))) - 1))

def gimgurls(query, quantity=1):
    '''
    "gimgs" may be interpreted as "get images" or "google images"
    returns a list whose first component is a list of site urls 
    and whose second component is the list of corresponding images
    (the ones that are shown by a google image search)
    The quantity argument is how many search results should appear,
    The query is the string that you want to search for.
    '''
    content = str(get(f'https://google.com/search?q={query}&tbm=isch').content)
    img_urls = []
    iterator = 0
    while content.find("<a href") != -1 and iterator < quantity:
        index = content.find("<a h")
        content = content[index:]
        index = content.find('"')
        content = content[index+1:]
        index = content.find('?')
        index = content.find('src="')
        content = content[index:]
        index = content.find('"')
        content = content[index+1:]
        index = content.find('"')
        img_urls.append(content[:index])
        iterator += 1
    return img_urls

def store(query, dir, quantity=1, value=None):
    '''
    This populates a folder "dir" with images from a search query.
    The number of images is the "quantity" argument,
    "store_keys" allows you to store the keys to the images in a csv
    file at "csv_path", and "value" is the value that serves as 
    an index to the keys in the csv file.
    '''
    if os.path.exists(f"{rig_path}/{dir}") == False:
        os.system(f"mkdir {rig_path}/{dir}")
        os.system(f"mkdir {rig_path}/{dir}/.rig")
    if os.path.exists(f"{rig_path}/references.csv") == False:
        os.system(f"touch {rig_path}/references.csv")
    imgs = gimgurls(query, quantity)
    with open(f"{rig_path}/references.csv", "a") as f:
        for img in imgs:
            i = random.randint(0, 99999999)
            temp = get(img).content
            temp = io.BytesIO(temp)
            temp = Image.open(temp)
            temp.save(f"{dir}/{i}.jpg")   
            f.write(f"{value},{dir}/{i}.jpg,{query}\n")
        f.close()

def remove(dir, quantity=1, label=None, query=None):
    if os.path.exists(f"{rig_path}/references.csv"):
        count = 0
        with open(f"{rig_path}/references.csv") as f:
            lines = f.readlines()
            f.close()
        for it in range(len(lines)-1, -1, -1):
            line = lines[it].split(",")
            if dir == line[1].split("/")[0]:
                fated = line[1]
                if not label and not query:
                    os.system(f"rm {rig_path}/{fated}")
                    lines.remove(lines[it])
                    count += 1
                if label and not query:
                    if line[0] == label:
                        os.system(f"rm {rig_path}/{fated}")
                        lines = lines.remove(lines[it])
                        count += 1
                if query and not label:
                    if line[2] == query:
                        os.system(f"rm {rig_path}/{fated}")
                        lines.remove(lines[it])
                        count += 1
                else:
                    if line[0] == label and line[2] == query:
                        os.system(f"rm {rig_path}/{fated}")
                        lines.remove(lines[it])
                        count += 1
            if count >= quantity:
                break
        
        if len(lines) == 0:
            os.system(f"rm {rig_path}/references.csv")
        else:
            with open(f"{rig_path}/references.csv", "w") as f:
                f.writelines(lines)
                f.close()
    if tracking[2]:    
        if len(os.listdir(f"{rig_path}/{dir}")) == 2:
            os.system(f"rm -r {rig_path}/{dir}")
    else:
        if len(os.listdir(f"{rig_path}/{dir}")) == 1:
            os.system(f"rm -r {rig_path}/{dir}")

def read(dir, ext_file, quantity=1, value=None):
    with open(ext_file) as f:
        lines = f.readlines()
        f.close()
    for line in lines:
        store(dir, quantity=quantity, value=value, query=line[:-1])

def track(bucket):
    if os.path.exists(f"{rig_path}/{bucket}") == False:
        os.system(f"mkdir {rig_path}/{bucket}")
        os.system(f"mkdir {rig_path}/{bucket}/.rig")
    if bucket not in tracking[0]:
        if tracking[2]:
            os.system(f"mkdir {rig_path}/{bucket}/{tracking[1]}")
        else:
            key = random.randint(0, 99)
            os.system(f"mkdir {rig_path}/.rigs{key}")
            if os.path.exists(f"{rig_path}/{bucket}") == False:
                os.system(f"mkdir {rig_path}/{bucket}")
            os.system(f"mkdir {rig_path}/{bucket}/.rigs{key}")
    print(bucket + " is now being tracked by this directory.")

def untrack():
    os.system(f"rm -r {rig_path}/{tracking[1]}")
    for bucket in tracking[0]:
        os.system(f"rm -r {rig_path}/{bucket}/{tracking[1]}")
    print("This directory is no longer tracking any buckets.")

def install():
    os.system("touch RIG.py")
    with open("RIG.py", "w") as f:
        f.writelines(f'''import numpy as np
from PIL import Image
from PIL import ImageOps
import random
import math
import os

rig_path = os.path.dirname(os.path.abspath(__file__))
dirs = os.listdir(".")

def pad_to_size(img_array, height, width, grayscale):
    #Takes in and outputs a numpy array
    if grayscale == False:
        h, w, c = img_array.shape
        img_array = np.concatenate((img_array, np.zeros((h, math.ceil((width-w)/2), c))), axis=1)
        img_array = np.concatenate((np.zeros((h, (width-w)//2, c)), img_array), axis=1)
        img_array = np.concatenate((img_array, np.zeros((math.ceil((height-h)/2), width, c))), axis=0)
        img_array = np.concatenate((np.zeros(((height-h)//2, width, c)), img_array), axis=0)
        return img_array
    else:
        h, w = img_array.shape
        img_array = np.concatenate((img_array, np.zeros((h, math.ceil((width-w)/2)))), axis=1)
        img_array = np.concatenate((np.zeros((h, (width-w)//2)), img_array), axis=1)
        img_array = np.concatenate((img_array, np.zeros((math.ceil((height-h)/2), width))), axis=0)
        img_array = np.concatenate((np.zeros(((height-h)//2, width)), img_array), axis=0)
        return img_array

def trim(img_array, img_w, img_h, grayscale):
    #Takes in and outputs a numpy array
    if grayscale == True:
        h, w = img_array.shape
    else:
        h, w, c = img_array.shape
    if h > img_h:
        img_array = img_array[img_array.shape[0]//2 - img_h//2:img_array.shape[0]//2 + img_h//2]
    if w > img_w:
        img_array = img_array[:, img_array.shape[1]//2 - img_w//2: img_array.shape[1]//2 + img_w//2]
    return img_array

class Data():
    def __init__(self, grayscale=False, img_dim=256, shuffle=False):
        with open("{rig_path}/references.csv") as f:
            lines = f.readlines()
            f.close()
            tracking_key = ".rig"
        for key in dirs:
            if key[:5] == ".rigs":
                tracking_key = key

        tracked = []
        for bucket in os.listdir("{rig_path}"):
            try:
                if tracking_key in os.listdir(bucket):
                    tracked.append(bucket)
            except: pass
        lines = [line for line in lines if line.split(",")[1].split("/")[0] in tracked]
        if shuffle == True:
            random.shuffle(lines)
        self.labels = []
        self.images = []
        for line in lines:
            line = line.split(",")
            self.labels.append(line[0])
            line = Image.open("{rig_path}/{"{line[1]}"}")
            if grayscale == True:
                line = ImageOps.grayscale(line)
            line = trim(np.array(line), img_dim, img_dim, grayscale)
            line = pad_to_size(line, img_dim, img_dim, grayscale)
            if grayscale == True:
                line = line.reshape((img_dim, img_dim, 1))
            self.images.append(line/255)''')
        f.close()  

p = optparse.OptionParser()
p.add_option('--quantity', '-q', default=1)
p.add_option('--label', '-l', default=None)
p.add_option('--query', '-Q', default=None)
opt, args = p.parse_args()
opt = vars(opt)

if len(args) == 0:
    print('''
NAME:
    RIG: "Retrieve Images on Google"

USAGE:
    rig [command] [flags]

DESCRIPTION:
    RIG is a set of tools designed to allow for the gathering and managing of image data found using Google. 
    RIG was created because of a need for quick image data collection to evaluate image-recognition models on. 
    In accordance with the use case for which it was created, the user is principally encouraged to use RIG as 
    a means of gathering temporary image data to evaluate models in development, while models reserved for 
    production should be trained on more carefully procured data.

COMMANDS:

    store               To populate the bucket with query results. Buckets are automatically 
                        created if the directory specified doesn't already exist.

        rig store <Bucket> <Query> -q <Quantity, Default to 1> -l <Label, Default to 0>


    remove              To remove images. The optional arguments function as filters for the removal.

        rig remove <Bucket> -q <Quantity, Default to 1> -l <Label> -Q <Originating Query>
    

    read                To populate a bucket with a list of results from a file.

        rig read <Bucket> <File> -q <Quantity per Line> -l <Label>

    track               Tracks specific directories while within the current directory.

        rig track <Bucket>

    untrack             Removes all directory-tracking for the current directory.

        rig untrack

    install             Copies the RIG.py file to the current directory so that the buckets may be read.

        rig install

Support:
    sactoa@gmail.com
    ''')

else:
    try:
        if args[0] == 'store':
            store(dir=args[1], query=args[2], quantity=opt['quantity'], label=opt['label'])
        if args[0] == 'remove':
            remove(dir=args[1], quantity=opt["quantity"], label=opt["label"], query=opt['query'])
        if args[0] == 'track':
            track(args[1])
        if args[0] == 'untrack':
            untrack()
        if args[0] == 'install':
            install()
    except:
        print('Invalid Input. See proper usage instructions by executing the "rig" command.')
    tracking = check_tracking()
    account()