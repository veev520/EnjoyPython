from PIL import Image

HTML_T = '''
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style type="text/css">
        body {
            margin: 0px; padding: 0px; line-height:100%; letter-spacing:0px; text-align: center;
            min-width: 1920px;
            width: auto !important;
            font-size: 10px;
            background-color: #000000;
            font-family: monospace;
        }
    </style>
</head>
<body>
<div>
'''
HTML_B = '''
</div>
</body>
</html>'''

# 新图片尺寸
SIZE = (160, 100)

# 要显示的文字
FONT_LIST = '超级'


def get_new_size(xy):
    """
    获取新图片尺寸
    :param xy: 
    :return: 
    """
    b = tuple()
    scale = 1
    if xy[0] <= SIZE[0] and xy[1] <= SIZE[1]:
        b = xy
    else:
        if xy[1] / xy[0] < SIZE[1] / SIZE[0]:
            scale = SIZE[0] / xy[0]
            x = SIZE[0]
            y = xy[1] * scale
            b = (int(x), int(y))
        elif xy[1] / xy[0] > SIZE[1] / SIZE[0]:
            scale = SIZE[1] / xy[1]
            y = SIZE[1]
            x = xy[0] * scale
            b = (int(x), int(y))
        else:
            b = SIZE
    return b


def rgb2hex(pixel):
    return '{:02x}{:02x}{:02x}'.format(*pixel)


def render(new):
    new_img = Image.open(new)
    html_list = list()
    print('渲染中, 请稍后')
    for y in range(new_img.size[1]):
        for x in range(new_img.size[0]):
            p = rgb2hex(new_img.getpixel((x, y)))
            font = FONT_LIST[(x + y) % len(FONT_LIST)]
            html_list.append('<font color="#%s">%s</font>' % (p, font))
        html_list.append('\n<br>\n')
    with open('Img.html', 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(HTML_T + '\n')
        htmlfile.write(''.join(html_list) + '\n')
        htmlfile.write(HTML_B)
    print('渲染完成')
    pass


def scale_img(src):
    img = Image.open(src)
    a = img.size
    img.resize(get_new_size(a), Image.ANTIALIAS).save('new_img.jpg', quality=100)
    return 'new_img.jpg'


if __name__ == '__main__':
    new_image = scale_img('img.jpg')
    render(new_image)

