from sendgridEmail import Email
from twilioSMS import SMS


class sendMessage():


    email = Email("", "")
    sms = SMS("", "")


    name = "Lucas"

    html = """\
<table style="width:100%">
  <tr>
    <td>{name}</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>""".format(name=name)

    email.sendEmail("", "", "Your portfolio status", html)

    sms.sendSMS("", "Your share GSK has fallen in price, "
                                 "log in to www.lucasamos.pythonanywhere.com to check it")

