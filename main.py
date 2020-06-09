import telebot
from telebot import types
from config import token
import datetime
import calendar


bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['calendar'])
def send_calendar(message):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    month_name = now.strftime("%B")
    keyboard = create_calendar(year, month, month_name)
    # --------------------
    # month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    #               'November', 'December']
    # for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
    #    keyboard.row(types.InlineKeyboardButton(day, callback_data='ignore'))

    bot.send_message(message.chat.id, 'Оберіть дату:', reply_markup=keyboard)


def create_calendar(year, month, month_name):
    keyboard = types.InlineKeyboardMarkup(row_width=7)
    month_button = types.InlineKeyboardButton(f'{month_name} {year}', callback_data=f'choose-month_{year}')
    my_calendar = calendar.Calendar(0)
    my_calendar = my_calendar.monthdayscalendar(year, month)
    keyboard.add(month_button)
    keyboard.add(types.InlineKeyboardButton("Mo", callback_data='ignore'),
                 types.InlineKeyboardButton("Tu", callback_data='ignore'),
                 types.InlineKeyboardButton("We", callback_data='ignore'),
                 types.InlineKeyboardButton("Th", callback_data='ignore'),
                 types.InlineKeyboardButton("Fr", callback_data='ignore'),
                 types.InlineKeyboardButton("Sa", callback_data='ignore'),
                 types.InlineKeyboardButton("Su", callback_data='ignore'))
    for week in my_calendar:
        list_day = []
        for day in week:
            if day != 0:
                list_day.append(types.InlineKeyboardButton(f"{day}", callback_data=f'{year}-{month}-{day}'))
            else:
                list_day.append(types.InlineKeyboardButton(" ", callback_data='ignore'))
        keyboard.add(list_day[0], list_day[1], list_day[2], list_day[3], list_day[4], list_day[5], list_day[6])
    keyboard.add(types.InlineKeyboardButton("<", callback_data=f'{year}-{month}<'),
                 types.InlineKeyboardButton("Cancel", callback_data='cancel'),
                 types.InlineKeyboardButton(">", callback_data=f'{year}-{month}>'))
    return keyboard


@bot.callback_query_handler(func=lambda callback: True)
def calendar_callback(callback):
    if 'setmonth_' in callback.data:
        index = callback.data.rfind('_')
        month = int(callback.data[9:index])
        year = int(callback.data[index+1:])
        date = datetime.date(year, month, 1)
        month_name = date.strftime("%B")
        my_calendar = calendar.Calendar(0)
        my_calendar = my_calendar.monthdayscalendar(year, month)
        keyboard = create_calendar(year, month, month_name)
        bot.edit_message_text('Оберіть дату:', callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)
    elif 'choose-month_' in callback.data:
        year = callback.data[-4:]
        month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
        keyboard = types.InlineKeyboardMarkup()
        month_list = []
        for month in enumerate(month_name):
            month_list.append(types.InlineKeyboardButton(f'{month[0]+1}. {month[1]}', callback_data=f'setmonth_{month[0]+1}_{year}'))
        keyboard.add(month_list[0], month_list[1], month_list[2], month_list[3], month_list[4], month_list[5],
                     month_list[6], month_list[7], month_list[8], month_list[9], month_list[10], month_list[11])
        bot.edit_message_text('Оберіть місяць', callback.message.chat.id, callback.message.message_id,
                              reply_markup=keyboard)
    elif '<' in callback.data:
        year = int(callback.data[:4])
        month = int(callback.data[5:-1])
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        date = datetime.date(year, month, 1)
        month_name = date.strftime("%B")
        my_calendar = calendar.Calendar(0)
        my_calendar = my_calendar.monthdayscalendar(year, month)
        keyboard = create_calendar(year, month, month_name)
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)
    elif '>' in callback.data:
        year = int(callback.data[:4])
        month = int(callback.data[5:-1])
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        date = datetime.date(year, month, 1)
        month_name = date.strftime("%B")
        my_calendar = calendar.Calendar(0)
        my_calendar = my_calendar.monthdayscalendar(year, month)
        keyboard = create_calendar(year, month, month_name)
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)
    elif callback.data == 'cancel':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'ignore':
        bot.answer_callback_query(callback.id, text='Оберіть дату:)')
    else:
        bot.answer_callback_query(callback.id, text=f'Ви обрали {callback.data}')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'Чудово! Ви обрали {callback.data}!')


if __name__ == '__main__':
    bot.infinity_polling()
