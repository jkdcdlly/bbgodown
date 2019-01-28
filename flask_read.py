from io import BytesIO

from flask import Flask, render_template, request, make_response, session
import pymysql
# from flask import render_template
# from flask.ext.yzm import Captcha
from flask_yzm import Captcha

mysql_host = "localhost"
mysql_user = "root"
mysql_passwd = ""
mysql_db = "scrapy_db"
conn = None
cur = None
app = Flask(__name__)
get_book_by_title = "select * from book_desc where book_title = %s"
book_detail_sql = "select classify,keywords,description,book_id,book_url, book_title, book_author, book_translator, book_copyright, book_datePublished, book_grade, book_score, book_rating, new_price, old_price, book_img, book_content, book_catalogue from book_desc where book_title = '{book_title}' limit 1"
book_classify_sql = "select distinct classify from book_desc WHERE classify is not null"
book_list_sql = "select book_id,book_title, book_author, book_translator, book_grade, book_score, book_rating, new_price, old_price, book_img from book_desc limit 20"

book_list_sql_filter = "select book_id,book_title, book_author, book_translator, book_grade, book_score, book_rating, new_price, old_price, book_img from book_desc where classify='{classify}'limit 20"

bestseller_list_sql = "select book_title, book_author from book_desc limit 10"
best_comment_list_sql = "select book_title, book_author from book_desc limit 10"
best_seller_list_sql = "select book_title, book_author from book_desc limit 10"


def res_2_dict(res, sql):
    cols_str = sql[7:sql.index("from")]
    print("提取字段的字符串========:", cols_str)
    cols = cols_str.replace(" ", "").split(",")
    print("截取的列========:", cols)
    arr = []
    for re in res:
        dicts = {}
        for i in range(0, len(re)):
            dicts[cols[i]] = re[i]
        arr.append(dicts)
    return arr


@app.route('/index/<page_type>')
@app.route('/')
def index(page_type='1'):
    book_cage = {

    }

    book_list = res_2_dict(query(book_list_sql), book_list_sql)
    bestseller_list = res_2_dict(query(bestseller_list_sql), bestseller_list_sql)
    best_comment_list = res_2_dict(query(best_comment_list_sql), best_comment_list_sql)
    bestseller_list_m = res_2_dict(query(best_seller_list_sql), best_seller_list_sql)
    return render_template('index.html',
                           bestseller_list=bestseller_list,
                           best_comment_list=best_comment_list,
                           bestseller_list_m=bestseller_list_m,
                           book_list=book_list, page_type=page_type)


@app.route('/detail/<page_type>/<book_title>')
def detail(page_type, book_title):
    title = "亮剑【 PDF免费下载 】"
    book_detail_sql2 = book_detail_sql.format(book_title=book_title)
    book_detail = res_2_dict(query(book_detail_sql2), book_detail_sql2)[0]
    book_list = res_2_dict(query(book_list_sql), book_list_sql)

    comment_list = [
                       {
                           "comment_title": "冲作者来的",
                           "comment_detail": "我都不知道我什么时候买的这本书，今天睡不着就找了这本书看看，看起来真过瘾，正好宋史是我的缺失部分，趁着睡不着了解下。不知不觉都凌晨4点多了。评价一下，睡觉吧",
                           "comment_grade": 10,
                           "comment_times": "2天前",
                           "comment_smile": 10,
                           "comment_reply": 5
                       }
                   ] * 10

    verify_images = ["/static/image/yzm/code1.jpg",
                     "/static/image/yzm/code2.jpg",
                     "/static/image/yzm/code3.jpg",
                     "/static/image/yzm/code4.jpg"]
    return render_template('detail.html', page_type=page_type, title=title,
                           book_list=book_list,
                           book_detail=book_detail,
                           verify_images=verify_images[random.randint(0, 3)],
                           comment_list=comment_list
                           )


@app.route('/榜单家族')
def bangdan():
    return render_template('hello.html')


@app.route('/list')
@app.route('/list/<classify>')
def list(classify=''):
    if classify != '':
        sql = book_list_sql_filter.format(classify=classify)
    else:
        sql = book_list_sql
    book_list = res_2_dict(query(sql), sql)
    classifys = res_2_dict(query(book_classify_sql), book_classify_sql)

    return render_template('list.html', book_list=book_list, classifys=classifys, classify=classify)


@app.route('/yzm/')
def profile():
    return render_template('yzm.html')


# 蓝图返回图形验证码.py
@app.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    # 缓存
    print("图形验证码是：", text.lower())
    # zlcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    return resp


from io import BytesIO


@app.route('/code/')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response


#
#
# @app.route('/login2', methods=['GET', 'POST'])
# def login2():
#     if request.method == 'POST':
#         pass
#     else:
#         pass


from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def get_verify_code():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)

    image.save('code2.jpg', 'jpeg')
    # return image, "code"


def query(sql):
    print("--------执行SQL-----------", sql)
    cur.execute(sql)
    return cur.fetchall()


def save(table, cols, values):
    insert_sql = "replace into {table} ({cols}) values ({values})".format(table=table, cols=cols, values=values)
    cur.execute(insert_sql)


if __name__ == '__main__':
    conn = pymysql.connect(mysql_host, mysql_user, mysql_passwd, mysql_db, charset='utf8mb4', )
    cur = conn.cursor()
    app.run(host='0.0.0.0', debug=True)
    app.logger.debug('server running')
