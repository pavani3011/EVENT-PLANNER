# 📅 Event Planner – Flask + Google Calendar + Gmail

This is a simple yet powerful Event Planner web app built with **Flask**, integrated with **Google Calendar API** and **Gmail SMTP**. It allows users to schedule events, send Gmail invites to multiple recipients, and automatically create calendar events with attendee invitations.

---

## 🚀 Features

- 📧 **Gmail Validation** – Only accepts `@gmail.com` addresses
- 📅 **Google Calendar Integration** – Adds event to the user’s calendar
- 👥 **Invite Multiple People** – Invite multiple Gmail users to the event
- 🔒 **OAuth 2.0 Authentication** – Secure Google sign-in to access calendar
- 💌 **Email Notifications** – Send event invite emails via Gmail SMTP
- ✅ **JavaScript Form Parsing** – Handle comma-separated emails in frontend
- 🎨 **Clean UI** – Styled HTML/CSS form with feedback messages

---

## 🛠 Tech Stack

| Layer        | Tech |
|--------------|------|
| Backend      | Python (Flask) |
| Frontend     | HTML, CSS, JavaScript |
| APIs Used    | Google Calendar API, Gmail SMTP |
| Auth         | OAuth 2.0 (via Google) |
| Deployment   | (Planned: Render / Railway / Vercel) |

---

## 🔐 Prerequisites

- Python 3.x
- Flask
- Google Cloud Project with:
  - Calendar API enabled
  - OAuth 2.0 Credentials (JSON)
  - Test User added (your Gmail)

---


🔧 Setup Instructions
Create a project on Google Cloud Console

Enable the Google Calendar API

Configure the OAuth consent screen

Create OAuth credentials (Client ID) and download the JSON

Add http://127.0.0.1:5000/oauth2callback to authorized redirect URIs

Add your Gmail to Test Users

Place the downloaded JSON as oauth_credentials.json in your project folder



✨ Author
Pavani S.
Connect on LinkedIn | GitHub

