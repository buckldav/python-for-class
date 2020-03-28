#######################################
# YOU CAN CHANGE THINGS WITHIN QUOTES #
#######################################
receiver_email = "david.buckley@meritacademy.org"

html = """

    <h1>Hi There!</h1>
    <p>You can write HTML here.</p>

"""

#######################################
#       DON'T CHANGE THIS STUFF       #
#######################################
import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from env.settings import merit_password

# Email Setup
port = 465  # For SSL
sender_email = "merit.apcs@gmail.com"
password = merit_password

text = f"""\
The email didn't send your HTML
"""

# Create a secure SSL context
context = ssl.create_default_context()

# Create message metadata
message = MIMEMultipart("alternative")
message["Subject"] = "Hello There"
message["From"] = sender_email
message["To"] = receiver_email

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    # Send email here
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent to:", receiver_email)
    server.quit()
