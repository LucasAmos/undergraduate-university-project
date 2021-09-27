from twilio.rest import TwilioRestClient

class SMS():

    def __init__(self, account_sid, auth_token ):
        self.account_sid = account_sid
        self.auth_token = auth_token

    def sendSMS(self, phonenumber, message):
        # Your Account Sid and Auth Token from twilio.com/user/account
        # account_sid = "ACb3d2405e15df8441919994ce553eae4b"
        # auth_token  = "41e85a6638606f578860825b750462c1"
        client = TwilioRestClient(self.account_sid, self.auth_token)
        message = client.messages.create(body=message,
        to=phonenumber,    # Replace with your phone number
        from_="+441256830314") # Replace with your Twilio number
        #print message.sid




