import telebot
import os
import zipfile
import subprocess

# Recuperar o token do ambiente
TOKEN = os.environ.get('TOKEN')

# Diretório onde está o arquivo de log
LOG_FILE_PATH = '/caminho/datalog.log'

# Obter a lista de usernames autorizados do arquivo .env
users_allowed_str = os.environ.get('USERS_ALLOWED')

# Lista de usernames permitidos
USERS_ALLOWED = users_allowed_str.split(',')

# Criar instância do bot
bot = telebot.TeleBot(TOKEN)


# Comando para enviar o arquivo de log
@bot.message_handler(commands=['enviarlog'])
def enviar_log(message):
    try:
        # Verificar se o remetente está na lista de usernames permitidos
        if message.from_user.username in USERS_ALLOWED:
            # Compactar o arquivo de log
            with zipfile.ZipFile('log.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(LOG_FILE_PATH, arcname=os.path.basename(LOG_FILE_PATH))

            # Enviar o arquivo zip
            with open('log.zip', 'rb') as zip_file:
                bot.send_document(message.chat.id, zip_file)

            # Remover o arquivo zip temporário
            os.remove('log.zip')

            bot.reply_to(message, "Arquivo de log enviado com sucesso!")
        else:
            bot.reply_to(message, "Você não tem permissão para usar este comando.")
    except Exception as e:
        bot.reply_to(message, f"Erro ao enviar arquivo de log: {e}")


# Executar o script Bash
@bot.message_handler(commands=['executar_script'])
def executar_script(message):
    try:
        # Se o remetente não estiver na lista de usernames permitidos, sair
        if message.from_user.username not in USERS_ALLOWED:
            bot.reply_to(message, "Você não tem permissão para usar este comando.")
            return

        # Executar o script Bash
        subprocess.run("./acessoremoto.sh", shell=True, check=True)

        bot.reply_to(message, "Script Bash executado com sucesso!")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Erro ao executar o script Bash: {e}")


# Lidar com mensagens recebidas para capturar o chat ID
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Se a mensagem veio de uma conversa (não de um grupo, por exemplo)
    if message.chat.type == 'private':
        # Responder com uma mensagem de boas-vindas ou qualquer outra coisa
        bot.reply_to(message, "Olá! Você pode usar os comandos /executar_script ou /enviarlog.")


# Iniciar o bot
bot.polling()
