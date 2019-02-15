# coding=utf-8
import pymysql
import datetime
import math

# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWD = "MyNewPass4!"
MYSQL_DB = "mysite"
# MYSQL_PASSWD = ""
# MYSQL_DB = "scrapy_db"
sitemap_path = "/usr/share/nginx/html/"
# sitemap_path = ""
index_url = "http://www.bbgo.xyz/"
fopen = open('{sitemap_path}bbgo_sitemap.xml'.format(sitemap_path=sitemap_path, ), 'w')
fopen.write('<?xml version="1.0" encoding="UTF-8"?>\n')
fopen.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
fopen.write('  <url>\n')
fopen.write('    <loc>{index_url}</loc>\n'.format(index_url=index_url))
fopen.write('    <lastmod>%s</lastmod>\n' % datetime.date.today())
fopen.write('    <priority>1.00</priority>\n')
fopen.write('  </url>\n')
fopen.write('</urlset>\n')
fopen.close()
conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, charset='utf8mb4', )
cur = conn.cursor()

sql = "select book_title from book_desc where is_enable=1 "
num = cur.execute(sql)
detail_res = cur.fetchall()

sitemap_size = 8000
for i in range(1, int(math.ceil(num / sitemap_size)) + 2):
    fopen = open('{sitemap_path}bbgo_sitemap{index}.xml'.format(sitemap_path=sitemap_path, index=i), 'w')
    fopen.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fopen.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for re in detail_res[(i - 1) * sitemap_size:i * sitemap_size]:
        url = "{index_url}detail/1/{book_title}/".format(index_url=index_url, book_title=re[0])
        fopen.write('  <url>\n')
        fopen.write('    <loc>{url}</loc>\n'.format(url=url))
        fopen.write('  </url>\n')
        url = "{index_url}detail/2/{book_title}/".format(index_url=index_url, book_title=re[0])
        fopen.write('  <url>\n')
        fopen.write('    <loc>{url}</loc>\n'.format(url=url))
        fopen.write('  </url>\n')
    fopen.write('</urlset>\n')
fopen.close()
