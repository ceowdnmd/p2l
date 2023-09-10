import logging
import re
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 导入Phone库
from phone import Phone

# 设置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 你的 Telegram Bot Token
TOKEN = ''

# 创建 Updater 对象并传入 Telegram Bot Token
updater = Updater(token=TOKEN, use_context=True)

# 创建 Dispatcher 对象
dispatcher = updater.dispatcher

# 处理 /start 命令
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="欢迎使用归属地查询 Bot！发送一个手机号码以查询归属地。")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# 处理用户发送的消息
def get_location(update, context):
    user_message = update.message.text.strip()
    
    # 使用正则表达式验证用户输入是否是有效的11位数字手机号码
    if not re.match(r'^\d{11}$', user_message):
        context.bot.send_message(chat_id=update.message.chat_id, text="请输入正确的手机号码（11位数字）。")
        return
    
    # 使用Phone库查询归属地
    phone = Phone()
    data = phone.find(user_message)
    
    if data:
        response = f"`手机号码 {user_message} 的归属地信息：\n"
        response += f"省份: {data['province']}\n"
        response += f"城市: {data['city']}\n"
        response += f"邮政编码: {data['zip_code']}\n"
        response += f"区号: {data['area_code']}\n"
        response += f"运营商: {data['phone_type']}`"
        # 直接发送内容为 Markdown 格式
        context.bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode=ParseMode.MARKDOWN)
    else:
        response = f"无法查询手机号码 {user_message} 的归属地信息。"
        context.bot.send_message(chat_id=update.message.chat_id, text=response)

message_handler = MessageHandler(Filters.text & (~Filters.command), get_location)
dispatcher.add_handler(message_handler)

# 启动 Bot
updater.start_polling()

# 让 Bot 一直运行
updater.idle()
