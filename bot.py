# Imports do webbot e do plugin do whatsapp da Twilio
from botcity.web import WebBot, Browser, By
from botcity.plugins.twilio.whatsapp import BotTwilioWhatsappPlugin
import os

# Configura o plugin do whatsapp da Twilio
def whatsapp_auth():
    # Configuração das credenciais do Twilio
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")

    # Instancia o plugin do whatsapp
    whatsapp = BotTwilioWhatsappPlugin(account_sid, auth_token, whatsapp_number)
    return whatsapp


def main():
    # Lista de telefones para envio de mensagens
    phone_list = {
        "adm": "+5511999999999",
        "rh": "+5511999999999",
        "financeiro": "+5511999999999",
        "comercial": "+5511999999999",
    }

    # Instancia o bot e o plugin do whatsapp
    bot = WebBot()
    whatsapp = whatsapp_auth()

    # Seleciona o telefone para envio de mensagens
    to_phone = phone_list["comercial"]

    # Envia mensagem para o whatsapp informando o início do processo de login
    whatsapp.send_message(
        to_number=to_phone,
        msg_content="Atenção! O processo de login no site OrangeHRM foi iniciado. Por favor, aguarde."
    )

    # Configura o navegador para ser exibido
    bot.headless = False

    # Configura o navegador a ser utilizado
    bot.browser = Browser.FIREFOX

    # Configura o caminho do driver do navegador
    bot.driver_path = bot.get_resource_abspath("geckodriver.exe")

    # Abre o navegador e acessa o site
    bot.browse("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Procura pelo elemento campo de usuário do login 
    campo_usuario = bot.find_element(
        "div.oxd-form-row:nth-child(2) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)",
        by=By.CSS_SELECTOR)

    # Envio de mensagem para o whatsapp solicitando o usuário para o login
    whatsapp.send_message(
        to_number=to_phone,
        msg_content="Digite o usuário para o login no site OrangeHRM"
        )
    # Aguarda a resposta do usuário
    login_digitado = whatsapp.wait_for_new_message()
    # Preenche o campo de usuário com o valor digitado
    campo_usuario.send_keys(login_digitado.body)

    # Procura pelo elemento campo de senha do login
    campo_senha = bot.find_element(
        "div.oxd-form-row:nth-child(3) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)",
        by=By.CSS_SELECTOR)

    # Envio de mensagem para o whatsapp solicitando a senha para o login
    whatsapp.send_message(
        to_number=to_phone,
        msg_content="Digite a senha para o login no site OrangeHRM"
        )
    # Aguarda a resposta do usuário
    senha_digitada = whatsapp.wait_for_new_message()
    # Preenche o campo de senha com o valor digitado
    campo_senha.send_keys(senha_digitada.body)

    bot.enter()

    # Procura pela mensagem de erro de login
    alert = bot.find_element(".oxd-alert-content-text", by=By.CSS_SELECTOR)
    if alert and alert.text == "CSRF token validation failed":
        whatsapp.send_message(
            to_number=to_phone,
            msg_content="Erro: CSRF não validado"
        )
    else:
        whatsapp.send_message(
            to_number=to_phone,
            msg_content="Login efetuado com sucesso"
        )

    # Aguarda 3 segundos antes de fechar o navegador
    bot.wait(3000)
    bot.stop_browser()


if __name__ == '__main__':
    main()
