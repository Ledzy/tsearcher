# tsearcher
This is the source website file of tsearcher.

## Introduction
Tsearcher is a information-sharing platform, which aim to shrink the information asymmetry of education.<br>
Teachers could share slides/teaching plans, and exchange ideas by posting blogs here. High-quality resources would be filtered for teachers.<br>
The creation of the platform is enlightened by **Deloitte digital competition 2019.**


**Group Name**: 别数了就六字 <br>
**Problem**: 乡村教师好助手 <br>
**IP-address**: 120.78.15.54 <br>

## How to run
You directly can visit our website's ip address 120.78.15.54 <br>
If you want to run our website in your own server, firstly clone the project:
```python
git clone https://github.com/Ledzy/tsearcher.git
```

you have to install required package:
```python
pip install -r requirement.txt
```

then run the code below
```python
cd tsearcher
python manage.py
```
you can then access the website on your local host: 127.0.0.1:8000

**Attention:**
The HEAD version is only for **server with GPU**, which is used for running ON-LSTM. Therefore, we strongly suggest you to reset to previous (no ON-LSTM) version. To do this, run the command below before run manage.py:
```shell
git reset --hard e4cb9ce186a80c4155d2a8e65758e072e786fd43
```


## Project Framework
* **Backend**: Django 2.2.3 <br>
* **Frontend**: HTML+CSS+Javascript <br> <br>
The frontend code is partially based on https://colorlib.com/download/2195/, which is a free model provided by colorlib

## TO-DO
- [ ] transfer allow CPU server run the model
- [x] allow comment
- [ ] add mooc function
- [ ] allow multi-type resources' uploading
- [ ] refine mobile interface

## Contact us
If you have any problem about the project, feel free to contact us: qijunluo@link.cuhk.edu.cn
