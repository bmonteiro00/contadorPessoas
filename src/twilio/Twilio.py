from twilio.rest import Client


class SMSSender:

    def __init__(self):
        self.account_sid = 'AC3be570f54aa0ffd4b4bb2fb0b4ab7bbe'
        self.auth_token = '8b35e8eeabbee8b4bdd0f03b0b6088ed'

    def conectarTwilio(self):
        self.client = Client(self.account_sid, self.auth_token)

    def enviarmensagem(self, msg, cel1, cel2):
        message = self.client.messages \
                        .create(
                             body=msg,
                             from_=cel1 ,
                             to=cel2
                         )

        print(message.sid)


if __name__ == "__main__":
    sender = SMSSender()
    sender.conectarTwilio()
    sender.enviarmensagem("Vila Cruzeiro - Linha:6422-10 com 30 passageiros", "+16095214368", "+5511986373109")