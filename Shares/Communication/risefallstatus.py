import sys
sys.path.append("/home/lucasamos/FYP")

from Shares.models import User, Userownedshare
from twilioSMS import SMS
from sendgridEmail import Email

from manage import db
from Shares.share_data import share_data
from datetime import datetime as dt
import datetime
from EmailFallRise import EmailFallRise


class risefallstatus():
    email = Email("", "")
    sms = SMS("", "")
    session = db.session()
    today = datetime.datetime.today().isoweekday()

    if today is not 6 and today is not 7:
        for user in session.query(User):

            if user.smsenabled:

                print ""
                print "** sms's enabled for: %s **" %(user.username)
                print ""

                for share in session.query(Userownedshare).filter_by(user=user.username):

                    if share.smsalert or share.emailalert:

                        alerttime = share.lastalert
                        currenttime = dt.today()
                        delta = currenttime - alerttime
                        hourssincelastalert = delta.total_seconds() // 60 /60

                        if hourssincelastalert > 10:

                            ticker = share.ticker
                            name = str(share.name.name)
                            print name
                            change = float(share_data.JSONShareFall(ticker)['query']['results']['quote']['Change'])
                            print "rise/fall: %s" %change

                            print "triggerlevel: %s" \
                                  " " %share.triggerlevel

                            if share.triggerlevel < 0:

                                if change < share.triggerlevel:

                                    data = {"risefall": "fallen", "name": name, "change": change}
                                    html = EmailFallRise.emailnotification(data)

                                    if share.emailalert:
                                        email.sendEmail(user.email, "alerts@lucasamos.net", "Share alert for %s" %name, html)

                                    if share.smsalert:
                                        sms.sendSMS(user.phonenumber, "Your share %s has fallen by %sp" % (name, change))

                                    share.lastalert = dt.today()
                                    db.session.add(share)
                                    db.session.commit()

                                    print "alert: Sent"
                                    print""

                                else:
                                    print "alert: False"
                                    print""

                            elif share.triggerlevel > 0:
                                if change > share.triggerlevel:

                                    data = {"risefall": "risen", "name": name, "change": change}
                                    html = EmailFallRise.emailnotification(data)

                                    if share.emailalert:
                                        email.sendEmail(user.email, "alerts@lucasamos.net", "Share alert for %s" %name, html)

                                    if share.smsalert:
                                        sms.sendSMS(user.phonenumber, "Your share %s has risen by %s" % (name, change))

                                    share.lastalert = dt.today()
                                    db.session.add(share)
                                    db.session.commit()

                                    print "alert: Sent"
                                    print""

                                else:
                                    print "alert: False"
                                    print""

                        else: print "alert already sent today for: %s" %share.name.name

                    else: print ""\
                            "alert disabled for %s" %share.name.name

            else:
                print ""
                print "** alerts disabled for: %s **" %(user.username)
                print""