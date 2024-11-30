import requests
import re

API_URL_MailTM = "https://api.mail.tm"

def login(email, pwd):
    response = requests.post(f"{API_URL_MailTM}/token", json={
        "address": email,
        "pwd": pwd
    })
    if response.status_code == 200:
        return response.json().get("token")
    return None

def fetchLatestMail(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL_MailTM}/messages", headers=headers)
    if response.status_code == 200:
        emails = response.json().get("hydra:member", [])
        if emails:
            return emails[0]
    return None

def extractOTP(emailContent):
    otpPatt = r"\b\d{6}\b"
    match = re.search(otpPatt, emailContent)
    if match:
        return match.group(0)
    return None

def main():
    email_file = "email.txt"
    try:
        with open(email_file, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(":")
        email = parts[0]
        pwd = parts[1] if len(parts) > 1 else "Walmart@"

        token = login(email, pwd)
        if token:
            latestEmail = fetchLatestMail(token)
            if latestEmail:
                emailID = latestEmail["id"]
                emailResp = requests.get(f"{API_URL_MailTM}/messages/{emailID}", headers={"Authorization": f"Bearer {token}"})
                if emailResp.status_code == 200:
                    emailContent = emailResp.json().get("text", "")
                    otp = extractOTP(emailContent)
                    if otp:
                        return otp
    return None
