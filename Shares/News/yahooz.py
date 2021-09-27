from News import News
from datetime import datetime as dt
from manage import db
from Shares.models import Userownedshare
import datetime



class yahooz():

    share = Userownedshare.query.get_or_404("1")
    alerttime = share.lastalert
    currenttime = dt.today()

    delta = currenttime - alerttime

    print (delta.total_seconds() // 60 /60)




    #print datetime.timedelta(time)
