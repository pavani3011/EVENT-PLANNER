from flask import Flask, render_template, request, redirect, flash, session, url_for
import re
import smtplib
from email.message import EmailMessage
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.auth.exceptions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key= os.getenv("SECRET_KEY")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

#OAuth setup
CLIENT_SECRETS_FILE= "oauth_credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

#validation fn
# def is_valid_gmail(email):
#     return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$",email)


@app.route('/')
def index():
    return render_template("index.html")



@app.route("/create", methods=["POST"])
def create():
    session['event_data'] = {
        "title": request.form["title"],
        "dsc": request.form["dsc"],
        "date": request.form["date"],
        "time": request.form["time"],
        "emails": request.form.getlist("emails")
    }
        

    # for email in session['event_data']["emails"]:
    #     if not is_valid_gmail(email):
    #         flash(f"invalid email: {email}. Only GMAIL is allowed!!")
    #         return redirect("/")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri= url_for('oauth2callback', _external= True)
    ) 
    authorization_url,state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    ) 
    session['state']= state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    service = build("calendar", "v3", credentials=credentials)
    data = session['event_data']
    
    
    #send mail to each guest
    for email in data["emails"]:
        send_email_invite(email,data["title"],data['dsc'],data['date'], data['time'])

    #Create event on calendar
    create_calendar_event(service, data["title"], data["dsc"], data["date"], data["time"], data["emails"])

    flash("Event created and invites sent!")
    return redirect("/")
           

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email_invite(to_email, title, dsc, date, time):
    msg = EmailMessage()  #obj to structure mail
    msg['Subject']= f"Event invite {title}"
    msg['From']= EMAIL_USER
    msg['To']= to_email
    msg.set_content(f"You are invited!! \n \n Event: {title} \n Description: {dsc} \n Date: {date} \n Time: {time}")

    # to send mail / secure connection to mail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465 ) as smtp:    # smtp.gmail.com - gmail server , 465 -  SSL port
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)


def create_calendar_event( service, title, dsc, date_str, time_str, guest_emails):
    # DATETIME -> ISO FORMAT
    start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(hours=1)

    event = {
        'summary': title,
        'description': dsc,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in guest_emails],
        'reminders': {
            'useDefault': True,
        },

    }

    event = service.events().insert(calendarId = 'primary', body= event, sendUpdates ='all').execute()
    print(f"Event created: { event.get('htmlLink')}")  

if __name__ == "__main__":
    app.run(debug=True)

     