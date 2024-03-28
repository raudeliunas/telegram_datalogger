import telebot
import os

# Recuperar o token do ambiente
TOKEN = os.environ.get('TOKEN')

# Diretório onde está o arquivo de log
LOG_FILE_PATH = '/caminho/teste.log'

# Lista de usernames permitidos
USERS_ALLOWED = ["raudeliunas", "username2", "username3"]

# Criar instância do bot
bot = telebot.TeleBot(TOKEN)

# Comando para enviar o arquivo de log
@bot.message_handler(commands=['enviarlog'])
def enviar_log(message):
    try:
        # Verificar se o remetente está na lista de usernames permitidos
        if message.from_user.username in USERS_ALLOWED:
            with open(LOG_FILE_PATH, 'rb') as log_file:
                bot.send_document(message.chat.id, log_file)
                bot.reply_to(message, "Arquivo de log enviado com sucesso!")
        else:
            bot.reply_to(message, "Você não tem permissão para usar este comando.")
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
