import csv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
merit_password = "akong18pangeskwela"

# Email Setup
port = 465  # For SSL
sender_email = "david.buckley@meritacademy.org"
password = merit_password

# Create a secure SSL context
context = ssl.create_default_context()

myFile = open("fees.csv", 'r', newline='')  
with myFile:  
    reader = csv.reader(myFile)

    header = []
    for row in reader:
        header = row
        break
    for row in reader:
        # Create message metadata
        receiver_email = row[0]
        message = MIMEMultipart("alternative")
        message["Subject"] = "Fees for Merit Ultimate Frisbee"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"""\
        Hello!

        You are receiving this email because {row[2]} {row[1]} has remaining fees for Ultimate Frisbee at Merit Academy.
        T-Shirts (dark and light): {row[3]}
        Tournaments and USAU Membership Fees: {row[4]}

        If you are on the middle school team and have already paid but see a $20 tournament fee, it is for the state tournament which was not initially included in the fee calculation.
        If you see tournament fees but did not participate in those tournaments, they are still charged because you were registered for the tournaments.

        Please pay with cash or check at the front office. These fees are not through Aspire because we did not get them preapproved last year.

        Please email Mr. Buckley at {sender_email} if you have any questions.
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            # Send email here
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent to:", receiver_email)
            server.quit()