import sendgrid


class Email():
    def __init__(self, UserID, UserPassword):

       self.UserID = UserID
       self.UserPassword = UserPassword


    def sendEmail(self, add_to, set_from, set_subject, set_html):

        # using SendGrid's Python Library - https://github.com/sendgrid/sendgrid-python

        sg = sendgrid.SendGridClient(self.UserID, self.UserPassword, secure=True)
        message = sendgrid.Mail()
        message.add_to(add_to)
        message.set_from(set_from)
        message.set_subject(set_subject)
        message.set_html(set_html)

        sg.send(message)



