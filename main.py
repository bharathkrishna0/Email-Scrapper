from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import imaplib
import email
import requests
load_dotenv()

username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def connect_to_mail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username,password)
    mail.select("Inbox")
    return mail

def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content,"html_parser")
    links = [link["href"]for link in soup.find_all("a",href = True) if "unsubscribe" in link["href"].lower()]
    return links

def click_link(link):
    try:
        response = requests.get(link)
        if response.status_code ==200:
            print("Sucessfully visited",link)
        else:
            print("failed to visit",link,"error code",response.status_code)
    except Exceptions as  e :
        print("Error with",link,str(e))

def search_for_mail():
    mail = connect_to_mail()
    _,search_data = mail.search(None,'(BODY "unsubscribe")')
    data = search_data[0].split()
    links = []

    for num in data:
        _, data = mail.fetch(num,"(RFC822)") 
        msg = email.message_from_bytes(data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode = True).decode()
                    links.extend(extract_links_from_html(html_content))
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True).decode()

            if content_type == "text/html":
                links.extend(extract_links_from_html(content))

    mail.logout()
    return links


def save_links(Links):
    with open("links.txt","w") as f:
        f.write("/n".join(Links))
links = search_for_mail
for link in links:
    click_link(link)
search_for_mail

 




