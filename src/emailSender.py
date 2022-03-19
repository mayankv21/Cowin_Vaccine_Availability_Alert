import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os


def sendEmail(appConfigDict, subject, html, attachmentFpath = None) :
        """send mail to recepients
        Args:
            receiverAdressBook : list of target mail addresses
            subject : mail subject 
            html : mail body
            attachmentFpaths : file path of attachment file
        """
    
        isMailSent = False
        msg = MIMEMultipart()
        msg['From'] = appConfigDict['sendersMail']
        msg['To'] = ','.join(appConfigDict['receiverAdressBook'])
        msg['Subject'] = subject

        # msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        if not(attachmentFpath==None):
            # fPath = cast(str, filePath)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachmentFpath, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{0}"'.format(os.path.basename(attachmentFpath)))
            msg.attach(part)
            
        text = msg.as_string()
        # Send the message via our SMTP server
        session = smtplib.SMTP(appConfigDict['emailHost'], appConfigDict['port'])
        session.starttls()
        # handling exception or error during login or sednign mail
        try:
            session.login(appConfigDict['sendersUsername'], appConfigDict['sendersPass'])
            session.sendmail(appConfigDict['sendersMail'], appConfigDict['receiverAdressBook'], text)
            isMailSent =True
        except Exception as err:
            print("Error while sending mail", err)
        finally:
            session.quit()

        return isMailSent
