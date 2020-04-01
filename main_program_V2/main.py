'''
Check for whether goods arrived or not in this special situation;
You can use it to check for surgical mask, hand sanitizer, medical exam gloves.   
'''

import requests
import time
import re #regular expressions 
import smtplib  # use for email

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

from lxml import html 


# Number of products need for each category
product_num = 5

# urls for productss want in amazon
url = []

ama_link = 'https://www.amazon.com/dp/'

# recommand urls in amazon
recommand_url= [
    # best sellers for surgical mask
    'https://www.amazon.com/Best-Sellers-Industrial-Scientific-Surgical-Masks/zgbs/industrial/11312315011',

    # best sellers for hand sanitizer
    'https://www.amazon.com/Best-Sellers-Health-Personal-Care-Hand-Sanitizers/zgbs/hpc/2265897011',

    # best sellers for medical exam gloves
    'https://www.amazon.com/Best-Sellers-Industrial-Scientific-Medical-Exam-Gloves/zgbs/industrial/8404645011'
]


# FUnction to send email
# def sendMail(url):
def sendMail():
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # email address used to send to; any email address is fine
    TO = 'XXXXX@outlook.com'
    # email subject
    SUBJECT = 'Here is the summary for products you are interested in!!'
    # contents of email
    # Send an attachment for report
    TEXT = "Please download the attached txt file for your report."

    # Gmail Sign In
    gmail_sender = 'XXXX@gmail.com'
    gmail_passwd = 'XXXXXX'

    # storing the senders email address   
    msg['From'] = gmail_sender 
    # storing the receivers email address  
    msg['To'] = TO
    # storing the subject  
    msg['Subject'] = SUBJECT
    # string to store the body of the mail 
    body = TEXT
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # open the file to be sent  
    filename = "report.txt"
    attachment = open(filename, "rb") 
  
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
    # encode into base64 
    encoders.encode_base64(p) 
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 


    # creates SMTP session 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security  
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    '''
    BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])
    '''

    # Converts the Multipart msg into a string 
    cont = msg.as_string() 

    try:
        server.sendmail(gmail_sender, [TO], cont)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()

# list for in stock, not in stock, final merged.
List_P = []
List_N = []
#List_M = []

# check for category for in-stock product
def cat_check_P(p_num, product_num):
    if (p_num // product_num == 0):
        List_P.append("surgical mask. ")
    if (p_num // product_num == 1):
        List_P.append("hand sanitizer. ")
    if (p_num // product_num == 2):
        List_P.append("medical exam gloves. ")

# check for category for none-product
def cat_check_N(p_num, product_num):
    if (p_num // product_num == 0):
        List_N.append("surgical mask. ")
    if (p_num // product_num == 1):
        List_N.append("hand sanitizer. ")
    if (p_num // product_num == 2):
        List_N.append("medical exam gloves. ")

# array for positive results
def posArr(url):
    List_P.append('Currently can purchase!! Be quick to buy ： ' + url)


# array for negative results
def negArr(url):
    List_N.append('Cannot purchase now： ' + url)


# merge 2 arrays
def mergeArr(LP, LN):
    # initialize an empty string 
    str_temp = "" 

    for ele in List_P:
        str_temp += ele
        str_temp += '\n' 

    str_temp += "\n"
    str_temp += "\n"
    str_temp += "Below are NOT in-stock products: "
    str_temp += "\n"
    str_temp += "\n"

    for e in List_N:
        str_temp += e
        str_temp += '\n' 

    # List_M = List_P + List_N
    return str_temp


# append data in txt file
def createAttach(str_temp):
    # FIrst add in current contents
    f=open("report.txt", "a+")
    f.write(str_temp) # no need for new line, str_temp has
    f.close()

    # send email with current report here
    sendMail()

    # Every time clear contents of report at the end
    file = open("report.txt","r+")
    file.truncate(0)
    file.close()

    # Clear contents of all lists
    List_P[:] = []
    List_N[:] = []
    # List_M[:] = []


# headers needed for page request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Connection": "keep-alive"
  }

# auto detect links in best sellers page
def autoDetect(recommand_url):
    # only iterate once
    for i in recommand_url: 
        # because continuous checks in milliseconds or few seconds blocks your request 
        time.sleep(1)  

        # adding headers to show that you are a browser who is sending GET request 
        page = requests.get(i, headers = headers)  
          
        # parsing the html content 
        doc = html.fromstring(page.content) 
    
        # check for product link in href
        XPATH_HREF = '//span[@class = "aok-inline-block zg-item"]/a[@class ="a-link-normal"]/@href'
        RAw_HREF = doc.xpath(XPATH_HREF) 
        #print(type(RAw_ama_link)) # list

        # Only need target number of products
        for j in range(product_num):
            strrr = str(RAw_HREF[j])

            # find product ID
            target = re.search('/dp/(.+?)/ref=', strrr)
      
            # if found, create new links
            if target:
                found = target.group(1)
                link = ama_link + found
                #print(link)

                url.append(link)
    # when finish iterating all links in recommand links, call check func
    check(url)


# check availiabity for product
def check(url): 
    # Function to check products on website, start with 1  
    flag = 1
    # Will check in a loop forever once program is running
    while (1):
        try:
            # print in terminal
            print('It is ' + str(flag) + ' try  ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            flag += 1

            # p_num to determine product in which category now
            p_num = -1
            for i in url: 
                # because continuous checks in milliseconds or few seconds blocks your request 
                time.sleep(1)  

                # adding headers to show that you are a browser who is sending GET request 
                page = requests.get(i, headers = headers)  
          
                # parsing the html content 
                doc = html.fromstring(page.content) 
          
                # checking availaility 
                XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
                RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY) 
                AVAILABILITY = ''.join(RAw_AVAILABILITY).strip()

                # AVAILABILITY is string
                print(AVAILABILITY)

                # p_num increases 1 for this product
                p_num += 1 #0,1,2,3,4

                # array for available results
                arr = [ 
                    'Only 1 left in stock', 
                    'Only 2 left in stock', 
                    'Available from these sellers',
                    'order soon',
                    'In stock',
                    'In Stock'] 

                # sto flag to determine in stock or not
                sto = False
                for j in arr:
                    if j in AVAILABILITY:
                        sto = True
                        print('Currently can purchase!! Be quick to buy ： ' + i)
                        cat_check_P(p_num, product_num)
                        posArr(i)
                        break
                    else:
                        continue
                
                if sto == False:
                    print('Cannot purchase now： ' + i)     
                    cat_check_N(p_num, product_num)  
                    negArr(i)      
            
            createAttach(mergeArr(List_P, List_N))
            # sendMail()
            # Everytime after this bunch of calls, sleep 3s
            time.sleep(3)


        # exception func
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print('Exception happens.')
            time.sleep(10)


if __name__ == '__main__':
    autoDetect(recommand_url)
