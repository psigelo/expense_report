This repository is for expense report, the main idea is to extract text from receipt images 

## Installation instructions

For the moment only ubuntu has been tested. It is probably that the software could run in any
Operation System because is writed in python code.

Instalation instructions:

1. install mongodb from https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
2. clone this repository
3. from root of this repository, create the virtual environment.
4. source the virtual environment.
5. pip install -r requirement
6. run python setup.py develop or python setup.py install (any of these options works)  

Is also important to download two pre-trained models and move them to the following folders:


download https://drive.google.com/file/d/1Jk4eGD7crsqCCg9C9VjCLkMN3ze8kutZ/view and move the file into 
./ai/CRAFT/

download https://www.dropbox.com/sh/j3xmli4di1zuv3s/AAArdcPgz7UFxIHUuKNOeKv_a?dl=0&preview=TPS-ResNet-BiLSTM-Attn-case-sensitive.pth and move the file into ./ai/extract_info
