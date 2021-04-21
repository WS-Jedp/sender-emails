from dotenv import load_dotenv
from email.message import EmailMessage
import imghdr
import smtplib
import os


def create_message(user_email, dest_email):
    msg = EmailMessage()
    msg['Subject'] = 'Example'
    msg['From'] = user_email
    msg['To'] = dest_email

    msg.add_alternative("""\
        <!DOCTYPE html>
        <html lang="en">
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <h1 style="font-size: 1rem; margin-bottom: 2rem;">
                Hello world with a test
            </h1>
            <p style="padding: 2rem; color: rgba(0,0,0,.7);">
                This is a good and pretty message from example
            </p>
        </body>
        </html>
        """, subtype='html')

    return msg

def add_images_to_msg(msg, imgs):

    for img in imgs:
        with open(img, 'rb') as img:
            img_data = img.read()
            img_type = imghdr.what(img.name)
            img_name = img.name
            
        msg.add_attachment(img_data, maintype="image", subtype=img_type, filename=img_name)

    return msg

def run():

    load_dotenv()
    CLIENT_EMAIL = os.getenv("CLIENT_EMAIL") 
    CLIENT_PASS = os.getenv("CLIENT_PASS")
    emails = ['']
    imgs = ['example']

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()

        smtp.login(CLIENT_EMAIL, CLIENT_PASS)

        for email in emails:
            msg = create_message(CLIENT_EMAIL, email)
            msg = add_images_to_msg(msg, imgs)
            smtp.send_message(msg)


if __name__ == '__main__':
    run()