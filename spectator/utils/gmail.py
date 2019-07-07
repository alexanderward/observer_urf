import json
import smtplib


def send_email(subject, text):
    if isinstance(text, dict):
        text = json.dumps(text, indent=4, sort_keys=True)
    to = 'observer.urf@gmail.com'
    subject = 'An Error Has Occurred - {}'.format(subject)

    # Gmail Sign In
    gmail_sender = 'observer.urf@gmail.com'
    gmail_passwd = '!!SandGnome18!!'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    body = '\r\n'.join(['To: %s' % to,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % subject,
                        '', text])

    try:
        server.sendmail(gmail_sender, [to], body)
    except Exception as e:
        print('error sending mail')

    server.quit()
