# RIG
## RIG Command Line Tools
Download and add the RIG folder somewhere to your device.

Add the "rig" command as an alias:

First, open up the ```~/.bashrc``` file:
```
nano ~/.bashrc
```
Then, add rig as an alias by typing into the file:
```
alias rig="python <RIG Absolute Path>" 
```
Finally, run the ```~./bashrc``` file:
```
source ~/.bashrc
```
## RIG with Python
To use RIG with Python, simply import the RIG class from RIG.py after running ```rig install```.
## What is RIG?
RIG: "Retrieve Images on Google"

RIG is a set of tools designed to allow for the gathering and managing of image data found using Google. RIG was created because of a need for quick image data collection to evaluate image-recognition models on. In accordance with the use case for which it was created, the user is principally encouraged to use RIG as a means of gathering temporary image data to evaluate models in development, while models reserved for production should be trained on more carefully procured data.
## What does it do?
The user populates directories by specifying Google queries and labels. The user may also delete the most recently-added images from each folder. Displayed at the end of each action completed is the number of images within each folder. When data is ready to be fed to a model, the user can use the RIG class to read specified buckets, obtaining an array consisting of the images and their associated labels. 
## Documentation
To populate the bucket with query results:
```
rig store <Bucket> <Query> -q <Quantity, Default to 1> -l <Label, Default to 0>
```
Buckets are automatically created if the directory specified doesn't already exist.

To remove images:
```
rig remove <Bucket> -q <Quantity, Default to 1> -l <Label> -Q <Originating Query>
```
The optional arguments function as filters for the removal.

To populate a bucket with a list of results from a file:
```
rig read <Bucket> <File> -q <Quantity per Line> -l <Label>
```
The sample_files directory contains some sample text files that may be used with this command.

To track specific buckets while within the current directory:
```
rig track <Bucket>
```

To remove all bucket-tracking for the current directory:
```
rig untrack
```
To copy the RIG.py file to the current directory so that the buckets may be read:
```
rig install
```

## Drawbacks
While calling "store", you may notice that not the number of images stored is not that you input. This may be because some results provided by Google are not in a format easily converted into JPEG. Additionally, the program only tracks references in the "references.csv" file. Thus, if this file gets deleted or a change occurs to the image references that is not reflected in this file, errors may be thrown.

## Dependencies
Dependencies: Pillow, requests, numpy

If you have any questions or would like to collaborate, contact me at sactoa@gmail.com.
