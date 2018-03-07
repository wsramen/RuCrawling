# -*- coding: utf-8 -*-
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup as Soup

#selector = '#board_list > div > div.board_main.theme_defalut > table > tbody'
Post_list = 'http://bbs.ruliweb.com/market/board/1020'


res_list = requests.get(Post_list)
soup = Soup(res_list.content, "html.parser")
##table = soup.select(selector)

rows = soup.find_all('tr', class_='table_body')
for row in rows:
    r_classes = row.get('class')        #테이블 row를 가져가는데 notice(공지사항)은 뺀다.
    if u'notice' in r_classes:
        continue
    post = row.find_all('td')
    POST_ID = row.find(class_='id').get_text().strip()
    POST_subject = row.find(class_='subject').a.get_text().strip()
    POST_Time = row.find(class_='time').get_text().strip()
    POST_REC = int(row.find(class_='recomd').get_text().strip())

    if POST_REC >= 5:
##      DTPC = "/read/"
##      Post_reply = Post_list+DTPC+row.find(class_='id').get_text().strip()
        reply_link = post[2].a.get('href')
        res_reply = requests.get(reply_link)
        soup2 = Soup(res_reply.content, "html.parser")
        tmphighs = soup2.find('div', class_='comment_view best row')
        highs = tmphighs.find_all('tr')
        print u"{0} | {1} | {2}".format(POST_ID, POST_subject, POST_Time)
        aa = soup2.find('div', class_='comment_view best row').get_text()
        if not aa == u"\n":
            for high in highs:
                try:
                    Nck = high.find(class_='nick').get_text().strip()
                    tmp = high.find(class_='comment')
                    Rcm = tmp.find(class_='text').get_text().strip()
                    print "===============B E S T  C O M M E N T==============="
                    print u"ID = {0}\nCOMMENT\n{1}\n".format(Nck, Rcm)
                except:
                    pass