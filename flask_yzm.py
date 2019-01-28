# coding=utf-8
import random, os
import string

from PIL import Image, ImageDraw, ImageFont


# Image：一个画布
# ImaeDraw：一个画笔
# ImageFont:画笔的字体
# pip install pillow
#
# Captcha验证码g
class Captcha(object):
    # 生成几位数的验证码
    number = 4
    # 验证码图片的宽度和高度
    size = (100, 30)
    # 验证码字体大小
    fontsize = 25
    # 加入干扰线的条数
    line_number = 2
    # 构建一个验证码源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 用来绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        # 开始点     x                              y
        begin = (random.randint(0, width), random.randint(0, height))
        # 结束点    x                              y
        end = (random.randint(0, width), random.randint(0, height))
        # 画线条   开始点  结束点            线条颜色              线条宽度
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
        if tmp > 100 - chance:
            draw.point((w, h), fill=cls.__gene_random_color())

    # 生成随机的颜色
    @classmethod
    #                          起始颜色 最终颜色
    def __gene_random_color(cls, start=0, end=255):
        # 初始化随机数
        random.seed()
        #              按范围生成随机输R ,         G                         B
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    # 随机选择一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Courgette-Regular.ttf',
            'LHANDW.TTF',
            'Lobster-Regular.ttf',
            'verdana.ttf'
        ]
        # 随机选一个 字体
        font = random.choice(fonts)
        # 当前路径
        realpath = os.path.dirname(os.path.realpath(__file__))
        # 返回字体路径
        return realpath + '/' + font

    # 用来随机生成一个字符串(包括英文和数字)
    @classmethod
    def gene_text(cls, number):
        # cls.SOURCE生成list A-Z a-z 0-9 与短信验证码一致  number是生成验证码的位数
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的宽和高
        width, height = cls.size
        # 创建图片
        # R：Red（红色）0-255
        # G：G（绿色）0-255
        # B：B（蓝色）0-255
        # A：Alpha（透明度）
        # Image.new('RGBA',(width,height),cls.__gene_random_color(0,100))
        #           颜色    宽     高          背景颜色  __gene_random_color(0,100)随机产生
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        # 验证码的字体                 随机产生字体           字体大小
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 随机生成4为字符串
        text = cls.gene_text(cls.number)
        # 获取字体的尺寸
        font_width, font_height = font.getsize(text)
        # 填充字符串    x                            y坐标               文本    字体                字体颜色
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        # 绘制干扰线           绘制多少条干扰线
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
            # 绘制噪点
            cls.__gene_points(draw, 10, width, height)
            # with open('captcha.png','wb') as fp:
            #     image.save(fp)
        return (text, image)
