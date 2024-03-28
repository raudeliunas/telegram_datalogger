import telebot
import os
import zipfile

# Recuperar o token do ambiente
TOKEN = os.environ.get('TOKEN')

# Diretório onde está o arquivo de log
LOG_FILE_PATH = '/caminho/datalog.log'

# Criar instância do bot
bot = telebot.TeleBot(TOKEN)


# Comando para enviar o arquivo de log
@bot.message_handler(commands=['enviarlog'])
def enviar_log(message):
    try:
        # Compactar o arquivo de log
        with zipfile.ZipFile('log.zip', 'w') as zipf:
            zipf.write(LOG_FILE_PATH, arcname=os.path.basename(LOG_FILE_PATH))

        # Enviar o arquivo zip
        with open('log.zip', 'rb') as zip_file:
            bot.send_document(message.chat.id, zip_file)

        # Remover o arquivo zip temporário
        os.remove('log.zip')

        bot.reply_to(message, "Arquivo de log enviado com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"Erro ao enviar arquivo de log: {e}")


# Lidar com mensagens recebidas para capturar o chat ID
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Se a mensagem veio de uma conversa (não de um grupo, por exemplo)
    if message.chat.type == 'private':
        # Responder com uma mensagem de boas-vindas ou qualquer outra coisa
        bot.reply_to(message, "Olá! Para receber o arquivo de log, use o comando /enviarlog.")


# Iniciar o bot
bot.polling()
