import smtplib
 
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
 
EMAIL = "tennismanz100@gmail.com"
PASSWORD = "ewalufubdznpohnv"

def send_message(message):
    print("Sending message...")
    recipient = '646******' + CARRIERS['verizon']
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)
