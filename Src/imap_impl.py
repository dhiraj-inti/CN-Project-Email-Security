import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import rsa_impl
import pickle

import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_183=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_183["font"] = ft
        GLabel_183["fg"] = "#333333"
        GLabel_183["justify"] = "center"
        GLabel_183["text"] = "Mail received:"
        GLabel_183.place(x=90,y=160,width=100,height=42)

        GLabel_120=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_120["font"] = ft
        GLabel_120["fg"] = "#333333"
        GLabel_120["justify"] = "center"
        GLabel_120["text"] = "Developed by Inti Dhiraj"
        GLabel_120.place(x=160,y=40,width=214,height=30)

        GLabel_554=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_554["font"] = ft
        GLabel_554["fg"] = "#333333"
        GLabel_554["justify"] = "center"
        GLabel_554["text"] = "Result: "
        GLabel_554.place(x=100,y=310,width=70,height=25)

    def GButton_63_command(self):

        status, messages = imap.search(None, 'FROM "124157027@sastra.ac.in"')
        messages = messages[0].split(b' ')
        for mail in messages:
            _, msg = imap.fetch(mail, "(RFC822)")
            # you can delete the for loop for performance if you have a long list of emails
            # because it is only for printing the SUBJECT of target email to delete
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes type, decode to str
                        subject = subject.decode()
                    print("Deleting", subject)
            # mark the mail as deleted
            imap.store(mail, "+FLAGS", "\\Deleted")
        # permanently remove mails that are marked as deleted
        # from the selected mailbox (in this case, INBOX)
        imap.expunge()
        root.destroy()


    def GButton_58_command(self):
        root.destroy()

with open('keys.txt','r') as f:
    d,e,n = f.read().split()

d = int(d)
e = int(e)
n = int(n)

private, public = (d,n),(e,n)


user = '124157027@sastra.ac.in'
password = 'npxijznbuwvdmpwk'
host = 'imap.gmail.com'

# Connect securely with SSL
imap = imaplib.IMAP4_SSL(host)

## Login to remote server
imap.login(user, password)
#imap.debug = 5
status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 1
# total number of emails
messages = int(messages[0])

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        #print(body)
                        print()
                    elif "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    print(body)
            #print(content_type)
            #print(body)
            if content_type == "text/html":
                # if it's HTML, create a new HTML file and open it in browser
                folder_name = clean(subject)
                if not os.path.isdir(folder_name):
                    # make a folder for this email (named after the subject)
                    os.mkdir(folder_name)
                filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "w").write(body)
                # open in the default browser
                webbrowser.open(filepath)
            print("="*100)

#load model
model = pickle.load(open('model.pkl', 'rb'))
body = body.split()
body = [int(i) for i in body]
body = rsa_impl.decrypt(private,body)
print(body)
input_mail = [body]

# convert text to feature vectors and load vectorizer
feature_extraction = pickle.load(open('vectorizer.pickle', 'rb'))
input_data_features = feature_extraction.transform(input_mail)

# making prediction
prediction = model.predict(input_data_features)
print("It is a",end=' ')

if prediction[0] == 1:
    print('Ham mail')
    spam_ham = 'Ham'
else:
    print('Spam mail')
    spam_ham = 'Spam'

print("="*100)




root = tk.Tk()
app = App(root)
GMessage_468=tk.Message(root)
ft = tkFont.Font(family='Times',size=10)
GMessage_468["font"] = ft
GMessage_468["fg"] = "#333333"
GMessage_468["justify"] = "center"
GMessage_468["text"] = body
GMessage_468.place(x=230,y=90,width=270,height=199)

GLabel_932=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_932["font"] = ft
GLabel_932["fg"] = "#333333"
GLabel_932["justify"] = "center"
GLabel_932["text"] = spam_ham
GLabel_932.place(x=320,y=310,width=70,height=25)

if spam_ham=='Spam':
    GLabel_831=tk.Label(root)
    ft = tkFont.Font(family='Times',size=10)
    GLabel_831["font"] = ft
    GLabel_831["fg"] = "#333333"
    GLabel_831["justify"] = "center"
    GLabel_831["text"] = "Delete the mail?(yes/no)"
    GLabel_831.place(x=90,y=400,width=130,height=41)

    GButton_63=tk.Button(root)
    GButton_63["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times',size=10)
    GButton_63["font"] = ft
    GButton_63["fg"] = "#000000"
    GButton_63["justify"] = "center"
    GButton_63["text"] = "Yes"
    GButton_63.place(x=290,y=410,width=70,height=25)
    GButton_63["command"] = app.GButton_63_command

    GButton_58=tk.Button(root)
    GButton_58["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times',size=10)
    GButton_58["font"] = ft
    GButton_58["fg"] = "#000000"
    GButton_58["justify"] = "center"
    GButton_58["text"] = "No"
    GButton_58.place(x=400,y=410,width=70,height=25)
    GButton_58["command"] = app.GButton_58_command
root.mainloop()


# close the connection and logout
imap.close()
imap.logout()