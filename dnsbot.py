import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import dns.resolver

# 设置Telegram Bot的API Token
bot_token = '6171747835:AAFuqWfh8dqpVgt1_laVUCnf5qLiu4GKOaE'

# 创建Bot实例
bot = telegram.Bot(token=bot_token)

# 创建Updater实例
updater = Updater(token=bot_token, use_context=True)

# 定义start指令的处理函数
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="欢迎使用域名解析查询机器人，请输入要查询的域名")

# 定义查询指令的处理函数
def query(update, context):
    domain_name = update.message.text.strip()
    try:
        # 获取A记录
        a_record = dns.resolver.resolve(domain_name, 'A')
        a_records = [str(record) for record in a_record]

        # 获取AAAA记录
        aaaa_record = dns.resolver.resolve(domain_name, 'AAAA')
        aaaa_records = [str(record) for record in aaaa_record]

        # 获取CNAME记录
        cname_record = dns.resolver.resolve(domain_name, 'CNAME')
        cname_records = [str(record) for record in cname_record]

        # 获取MX记录
        mx_record = dns.resolver.resolve(domain_name, 'MX')
        mx_records = [str(record.exchange) for record in mx_record]

        # 获取SRV记录
        srv_record = dns.resolver.resolve(domain_name, 'SRV')
        srv_records = [str(record.target) for record in srv_record]

        # 发送查询结果给用户
        message = 'A记录: {}\n\nAAAA记录: {}\n\nCNAME记录: {}\n\nMX记录: {}\n\nSRV记录: {}'.format(
            ', '.join(a_records) if a_records else '无',
            ', '.join(aaaa_records) if aaaa_records else '无',
            ', '.join(cname_records) if cname_records else '无',
            ', '.join(mx_records) if mx_records else '无',
            ', '.join(srv_records) if srv_records else '无',
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except dns.resolver.NXDOMAIN:
        context.bot.send_message(chat_id=update.effective_chat.id, text="该域名不存在")
    except dns.resolver.NoAnswer:
        context.bot.send_message(chat_id=update.effective_chat.id, text="该域名无法解析")
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text="查询出错，请稍后再试")

# 创建CommandHandler实例
start_handler = CommandHandler('start', start)

# 创建MessageHandler实例
query_handler = MessageHandler(Filters.text & (~Filters.command), query)

# 将Handler添加到Updater中
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(query_handler)

# 启动Bot
updater.start_polling()
updater.idle()
