from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import rsa_impl
import gui_input

with open('keys.txt','r') as f:
    d,e,n = f.readline().split()
d = int(d)
e = int(e)
n = int(n)
private, public = (d,n),(e,n)


smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('124157027@sastra.ac.in', 'hlgxyjzcxrcccrtr')

msg = MIMEMultipart()
msg['Subject'] = "Machine generated mail"

#text = "07732584351 - Rodger Burns - MSG = We tried to call you re your reply to our sms for a free nokia mobile + free camcorder. Please call now 08000930705 for delivery tomorrow"
#text = "As per your request 'Melle Melle (Oru Minnaminunginte Nurungu Vettam)' has been set as your callertune for all Callers. Press *9 to copy your friends Callertune"
text = open('mail_to_be_sent.txt','r').read()
text = rsa_impl.encrypt(public,text)
text = [str(i) for i in text]
#print(type(text))
text = " ".join(text)
msg.attach(MIMEText(text))
#print(text)
smtp.set_debuglevel(True) 

#to = 'intidhiraj3103@gmail.com'
to = "124157027@sastra.ac.in"

smtp.sendmail(from_addr="124157027@sastra.ac.in",to_addrs=to, msg=msg.as_string())
smtp.quit()



""" attachment = "./Week 1 schedule.pdf"

with open(attachment, 'rb') as f:
    file = MIMEApplication(
        f.read(), name=os.path.basename(attachment)
    )
    file['Content-Disposition'] = f'attachment; \
    filename="{os.path.basename(attachment)}"'
    msg.attach(file) """