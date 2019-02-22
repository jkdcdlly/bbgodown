from flask import Flask, render_template, request, make_response, session
import pymysql
from flask_yzm import Captcha

app = Flask(__name__)


def get_conn():
    mysql_host = "localhost"
    mysql_user = "root"
    # mysql_passwd = "MyNewPass4!"
    # mysql_db = "mysite"
    mysql_passwd = ""
    mysql_db = "scrapy_db"
    return pymysql.connect(mysql_host, mysql_user, mysql_passwd, mysql_db, charset='utf8mb4', )


get_book_by_title = "select * from book_desc where is_enable=1 and book_title = %s "
book_detail_sql = "select classify,keywords,description,book_id,book_url, book_title, book_author, book_translator, book_copyright, book_datePublished, book_grade, book_score, book_rating, '限时免费' as new_price, old_price, book_img, book_content, book_catalogue from book_desc where is_enable=1 and book_title = '{book_title}' limit 1"
book_classify_sql = "select distinct classify from book_desc WHERE is_enable=1 and classify is not null"
book_list_sql = "select book_id,book_title, book_author, book_translator, book_grade, book_score, book_rating, '限时免费' as new_price, old_price, book_img from book_desc where is_enable=1 limit {skip_num},{page_size}"
book_count_sql = "select count(1) as book_num from book_desc where is_enable=1 "
book_list_sql_filter = "select book_id,book_title, book_author, book_translator, book_grade, book_score, book_rating, '限时免费' as new_price, old_price, book_img from book_desc where is_enable=1 and classify='{classify}' limit {skip_num},{page_size}"
book_count_sql_filter = "select count(1) as book_num from book_desc where is_enable=1 and classify='{classify}'"

bestseller_list_sql = "select book_title, book_author from book_desc where is_enable=1 and book_id%15=weekday(now())+0 limit 10"
best_comment_list_sql = "select book_title, book_author from book_desc where is_enable=1 and book_id%15=weekday(now())+1 limit 10"
best_seller_list_sql = "select book_title, book_author from book_desc where is_enable=1 and book_id%15=weekday(now())+2 limit 10"

best_more_list_sql = "select book_id,book_title, book_author, book_translator, book_grade, book_score, book_rating, '限时免费' as new_price, old_price, book_img from book_desc where is_enable=1 and book_id%15=weekday(now())+3 limit 20"

page_size = 20


def res_2_dict(res, sql):
    col_str = sql[7:sql.index("from")].strip()
    col_list = col_str.split(",")
    cols = list(map(lambda x: x.strip().split(" ")[-1], col_list))
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
    list_sql = book_list_sql.format(skip_num=0, page_size=page_size)
    book_list = res_2_dict(query(list_sql), list_sql)
    bestseller_list = res_2_dict(query(bestseller_list_sql), bestseller_list_sql)
    best_comment_list = res_2_dict(query(best_comment_list_sql), best_comment_list_sql)
    bestseller_list_m = res_2_dict(query(best_seller_list_sql), best_seller_list_sql)
    return render_template('index.html',
                           bestseller_list=bestseller_list,
                           best_comment_list=best_comment_list,
                           bestseller_list_m=bestseller_list_m,
                           book_list=book_list, page_type=page_type)


@app.route('/m/')
def m_index():
    bestseller_list = res_2_dict(query(bestseller_list_sql), bestseller_list_sql)
    best_comment_list = res_2_dict(query(best_comment_list_sql), best_comment_list_sql)
    return render_template('m_index.html',
                           bestseller_list=bestseller_list,
                           best_comment_list=best_comment_list,
                           )


@app.route('/detail/<page_type>/<book_title>/')
def detail(page_type, book_title):
    title = "亮剑【 PDF免费下载 】"
    book_detail_sql2 = book_detail_sql.format(book_title=book_title)
    book_detail = res_2_dict(query(book_detail_sql2), book_detail_sql2)[0]
    book_list = res_2_dict(query(best_more_list_sql), best_more_list_sql)

    # comment_list = [
    #                    {
    #                        "comment_title": "冲作者来的",
    #                        "comment_detail": "我都不知道我什么时候买的这本书，今天睡不着就找了这本书看看，看起来真过瘾，正好宋史是我的缺失部分，趁着睡不着了解下。不知不觉都凌晨4点多了。评价一下，睡觉吧",
    #                        "comment_grade": 10,
    #                        "comment_times": "2天前",
    #                        "comment_smile": 10,
    #                        "comment_reply": 5
    #                    }
    #                ] * 10

    verify_images = ["/static/image/yzm/code1.jpg",
                     "/static/image/yzm/code2.jpg",
                     "/static/image/yzm/code3.jpg",
                     "/static/image/yzm/code4.jpg"]
    return render_template('detail.html', page_type=page_type, title=title,
                           book_list=book_list,
                           book_detail=book_detail,
                           verify_images=verify_images[random.randint(0, 3)],
                           # comment_list=comment_list
                           )


@app.route('/榜单家族')
def bangdan():
    return render_template('hello.html')


@app.route('/list/<cur_page_num>/')
@app.route('/list/<cur_page_num>/<cur_classify>/')
def list2(cur_page_num='1', cur_classify=''):
    skip_num = (int(cur_page_num) - 1) * page_size
    if cur_classify != '':
        sql = book_list_sql_filter.format(classify=cur_classify, skip_num=skip_num, page_size=page_size)
        count_sql = book_count_sql_filter.format(classify=cur_classify)
    else:
        sql = book_list_sql.format(skip_num=skip_num, page_size=page_size)
        count_sql = book_count_sql
    app.logger.debug(sql)
    book_list = res_2_dict(query(sql), sql)
    # 分类
    classifys = res_2_dict(query(book_classify_sql), book_classify_sql)
    # 总条数
    total = res_2_dict(query(count_sql), count_sql)

    import math

    total_page_num = math.ceil(int(total[0]["book_num"]) / page_size)
    print("total_page_num=====", total_page_num)
    return render_template(
        'list.html',
        book_list=book_list,
        classifys=classifys,
        cur_classify=cur_classify,
        total_page_num=int(total_page_num),
        cur_page_num=int(cur_page_num),
        xianshi_page_num1=2 if int(cur_page_num) < 4 else int(cur_page_num) - 2,
        xianshi_page_num2=total_page_num if int(cur_page_num) + 3 >= total_page_num else int(cur_page_num) + 3,
        pre_page_num=1 if int(cur_page_num) == 1 else int(cur_page_num) - 1,
        next_page_num=int(total_page_num) if int(cur_page_num) == total_page_num else int(cur_page_num) + 1,
    )


@app.route('/yzm/')
def profile():
    return render_template('yzm.html')


# 蓝图返回图形验证码.py
@app.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    # 缓存
    # print("图形验证码是：", text.lower())
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
    app.logger.debug('server sql={sql}'.format(sql=sql))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return cur.fetchall()


def save(table, cols, values):
    insert_sql = "replace into {table} ({cols}) values ({values})".format(table=table, cols=cols, values=values)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    app.logger.debug('server running')
