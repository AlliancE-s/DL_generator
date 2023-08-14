import datetime

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random
import radar




def getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust):
    # 判断偏移量向上还是向下（大于0为向下，小于0为向上）
    if offset2 >= 0:
        point1 = [int(back_point[0] - adjust), int(back_point[1] - adjust)]
        point2 = [int(point_x + offset1 + length + adjust), int(back_point[1] - adjust)]
        point3 = [int(point_x + offset1 + length + adjust), int(point_y + offset2 + int(hight) - adjust)]
        point4 = [int(back_point[0] - adjust), int(point_y + offset2 + int(hight) - adjust)]
    elif offset2 < 0:
        point1 = [int(back_point[0] - adjust), int(point_y + offset2 - adjust)]
        point2 = [int(point_x + offset1 + length + adjust), int(point_y + offset2 - adjust)]
        point3 = [int(point_x + offset1 + length + adjust), int(back_point[1] + int(hight) - adjust)]
        point4 = [int(back_point[0] - adjust), int(back_point[1] + int(hight) - adjust)]

    return [point1, point2, point3, point4]


def gbk_trans_utf8(file_path):  #存在bug，弃用
    with open(file_path, 'r', encoding='gbk') as f:
        content = f.read()
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(content)


def random_name():
    # 删减部分小众姓氏
    firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
                "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
                "龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
    # 百家姓姓氏
    # firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平" \
    #             "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董粱杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮" \
    #             "龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴欎胥能苍" \
    #             "双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空" \
    #             "曾毋沙乜养鞠须丰巢关蒯相查後荆红游竺权逯盖益桓公晋楚闫法汝鄢涂钦归海帅缑亢况后有琴梁丘左丘商牟佘佴伯赏南宫墨哈谯笪年爱阳佟言福百家姓终"
    # 百家姓中双姓氏
    firstName2 = "万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒" \
                 "司空亓官司寇仉督子颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫南宫"
    # 女孩名字
    girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧' \
           '璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
    # 男孩名字
    boy = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友' \
          '裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
    # 名
    name = '中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝'

    # 10%的机遇生成双数姓氏
    if random.choice(range(100)) > 10:
        firstName_name = firstName[random.choice(range(len(firstName)))]
    else:
        i = random.choice(range(len(firstName2)))
        firstName_name = firstName2[i:i + 2]
        # firstName_name = firstName[random.choice(range(len(firstName)))]

    sex = random.choice(range(2))
    name_1 = ""
    # 生成并返回一个名字
    if sex > 0:
        girl_name = girl[random.choice(range(len(girl)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + girl_name
    else:
        boy_name = boy[random.choice(range(len(boy)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + boy_name


######################################

# 调试labely和filestate文件
# with open("DL_output/Label.txt", "w") as file:
#     file.write('')
# with open("DL_output/fileState.txt", "w") as file:
#     file.write('')

# 生成图片数量以及文字颜色
num_pic = 1000
set_color = (125, 125, 125)

for i in range(num_pic):
    # 图片字体初始化,选择背景
    typeCode = 11  # 用于不同背景的调整
    bk_img = cv2.imread("backgroud/back_digit_1.jpg")
    font_path = "font_song.ttc"
    font = ImageFont.truetype(font_path, 45)

    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)

    # 保存文件名，四位数
    temp_filename = str(i + 1)
    filename = temp_filename.zfill(4)

    # 印刷随机偏移量，1为x轴，2为y轴
    offset1 = random.uniform(-20,20)
    offset2 = random.uniform(-20,20)
    # offset1 = 0
    # offset2 = 0

    # 内容
    name = random_name()
    sex = random.choice(('男', '女'))
    birthday = radar.random_date("1950-01-01", "2005-12-30").date()
    startIssue = birthday + datetime.timedelta(days=6570)
    endIssue = birthday + datetime.timedelta(days=18250)
    issue_date = radar.random_date(str(startIssue), str(endIssue)).date()
    cartype = random.choice(('A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4', 'D', 'E', 'F', 'M', 'N', 'P'))
    startValid = issue_date + datetime.timedelta(days=random.randint(0, 3650))
    endValid = startValid + datetime.timedelta(days=2190)
    penalty = random.randint(0,12)
    file_code = random.randint(100000000000,999999999999)

    # 生成证号
    cid1 = str(random.randint(100000, 999999))

    if random.choice("01") == "0":
        k = str(random.randint(0, 9999))
        cid2 = k.zfill(4)
    else:
        k = str(random.randint(0, 999)).zfill(3)
        cid2 = k + "X"
    cid = cid1 + str(birthday.year) + str(birthday.month).zfill(2) + str(birthday.day).zfill(2) + cid2

    # 生成住址
    address = random.choice((
        '北京市', '天津市', '河北省石家庄市', '山西省太原市', '内蒙古自治区呼和浩特市', '辽宁省沈阳市', '吉林省长春市',
        '黑龙江省哈尔滨市', '上海市', '江苏省南京市', '浙江省杭州市', '安徽省合肥市', '福建省福州市', '江西省南昌市',
        '山东省济南市', '河南省郑州市', '湖北省武汉市', '湖南省长沙市',
        '广东省广州市', '广西壮族自治区南宁市', '海南省海口市', '贵州省贵阳市', '云南省昆明市', '西藏自治区拉萨市',
        '陕西省西安市',
        '甘肃省兰州市', '青海省西宁市', '宁夏回族自治区银川市', '新疆维吾尔自治区乌鲁木齐市'))

    # 填充内容

    # label.txt开头初始化
    with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
        file.write("DL_output/" + filename + ".jpg\t[")

    # 生成图片以及坐标
    if typeCode == 1:
        # 初始化文字高度以及宽度
        # 数字及字母直接写长度，不需要计算文字宽度
        # adjust是坐标调整量
        hight = 60
        width = 45
        adjust = 5

        # 证号
        # back point是背景上文字的左上角坐标
        # point xy 是生成文字左上角坐标
        back_point = [375, 140]
        point_x = 500
        point_y = 145
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 465
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [100, 210]
        point_x = 210
        point_y = 210
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [590, 210]
        point_x = 690
        point_y = 210
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [785, 210]
        point_x = 950
        point_y = 210
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 住址
        back_point = [100, 285]
        point_x = 220
        point_y = 290
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [355, 445]
        point_x = 550
        point_y = 450
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 245
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [355, 525]
        point_x = 600
        point_y = 530
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 240
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [355, 610]
        point_x = 600
        point_y = 620
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 40
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效期
        back_point = [105, 690]
        point_x = 330
        point_y = 700
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 540
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效起始日期' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')



    elif typeCode == 2:
        hight = 60
        width = 45
        adjust = 5

        # 证号
        back_point = [390, 165]
        point_x = 510
        point_y = 160
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 470
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [150, 225]
        point_x = 240
        point_y = 225
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [590, 225]
        point_x = 680
        point_y = 225
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [770, 225]
        point_x = 940
        point_y = 225
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [150, 295]
        point_x = 280
        point_y = 290
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [380, 435]
        point_x = 550
        point_y = 430
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 245
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [380, 510]
        point_x = 600
        point_y = 510
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 240
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [380, 585]
        point_x = 600
        point_y = 590
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 40
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [155, 665]
        point_x = 330
        point_y = 665
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 540
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')


    elif typeCode == 3:
        font = ImageFont.truetype(font_path, 55)
        hight = 70
        width = 60
        adjust = 7

        # 证号
        back_point = [455, 235]
        point_x = 570
        point_y = 230
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 570
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 名字
        back_point = [178, 308]
        point_x = 280
        point_y = 300
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [675, 305]
        point_x = 780
        point_y = 300
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [875, 310]
        point_x = 1050
        point_y = 300
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [175, 385]
        point_x = 350
        point_y = 380
        draw.text((350 + offset1, 380 + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [435, 545]
        point_x = 600
        point_y = 540
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 290
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [435, 630]
        point_x = 650
        point_y = 625
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 290
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [435, 715]
        point_x = 650
        point_y = 710
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 50
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效期
        back_point = [175, 800]
        point_x = 330
        point_y = 800
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 660
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')



    elif typeCode == 4:
        hight = 22
        width = 18
        adjust = 2
        font = ImageFont.truetype(font_path, 17)
        set_color = (85, 85, 85)
        offset1 = random.uniform(-5, 5)
        offset2 = random.uniform(-5, 5)

        # 证号
        back_point = [131, 60]
        point_x = 180
        point_y = 60
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 177
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [30, 86]
        point_x = 65
        point_y = 85
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [212, 86]
        point_x = 245
        point_y = 85
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [286, 86]
        point_x = 350
        point_y = 85
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [30, 115]
        point_x = 70
        point_y = 115
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [126, 173]
        point_x = 185
        point_y = 170
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 92
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [125, 203]
        point_x = 215
        point_y = 202
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 92
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [126, 234]
        point_x = 217
        point_y = 232
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 30
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效期
        back_point = [34, 267]
        point_x = 130
        point_y = 266
        draw.text((point_x + offset1, point_y + offset2), str(startValid), font=font,
                  fill=set_color)
        length = 90
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效起始日期' + str(startValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效期
        back_point = [216, 261]
        point_x = 278
        point_y = 264
        draw.text((point_x + offset1, point_y + offset2), '6年', font=font, fill=set_color)
        length = len("6年") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限6年", "points": ' + str(point_all) + ', "difficult": false}')


    elif typeCode == 5:
        hight = 60
        width = 45
        adjust = 5

        # 证号
        back_point = [337, 144]
        point_x = 433
        point_y = 148
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 470
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [120, 200]
        point_x = 189
        point_y = 198
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [513, 200]
        point_x = 570
        point_y = 200
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [670, 200]
        point_x = 800
        point_y = 200
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [120, 260]
        point_x = 220
        point_y = 260
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [320, 389]
        point_x = 455
        point_y = 388
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 245
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [320, 450]
        point_x = 500
        point_y = 450
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 240
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [320, 520]
        point_x = 505
        point_y = 520
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 40
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [122, 590]
        point_x = 250
        point_y = 590
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 540
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')


    elif typeCode == 6:
        hight = 24
        width = 20
        adjust = 2
        font = ImageFont.truetype(font_path, 18)
        set_color = (100,100,100)

        # 证号
        back_point = [219, 94]
        point_x = 263
        point_y = 94
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 189
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [114, 121]
        point_x = 148
        point_y = 120
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [302, 121]
        point_x = 335
        point_y = 118
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [379, 121]
        point_x = 426
        point_y = 118
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [114, 150]
        point_x = 156
        point_y = 148
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [213, 213]
        point_x = 273
        point_y = 212
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 100
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [213, 242]
        point_x = 298
        point_y = 240
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 100
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [212, 273]
        point_x = 300
        point_y = 271
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 40
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [116, 309]
        point_x = 176
        point_y = 309
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 222
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')



    elif typeCode == 7:
        hight = 24
        width = 20
        adjust = 2
        font = ImageFont.truetype(font_path, 17)
        set_color = (50,50,50)

        # 证号
        back_point = [206, 125]
        point_x = 248
        point_y = 125
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 179
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [107, 152]
        point_x = 146
        point_y = 152
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [286, 151]
        point_x = 320
        point_y = 151
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [359, 150]
        point_x = 430
        point_y = 150
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [107, 180]
        point_x = 154
        point_y = 180
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [198, 238]
        point_x = 254
        point_y = 238
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 93
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [199, 267]
        point_x = 288
        point_y = 267
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 93
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [198, 297]
        point_x = 280
        point_y = 297
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 22
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [96, 336]
        point_x = 151
        point_y = 336
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 212
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')



    elif typeCode == 8:
        hight = 33
        width = 28
        adjust = 3
        font = ImageFont.truetype(font_path, 25)


        # 证号
        back_point = [173, 93]
        point_x = 233
        point_y = 93
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 256
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [35, 127]
        point_x = 77
        point_y = 123
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [284, 127]
        point_x = 325
        point_y = 123
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [384, 127]
        point_x = 460
        point_y = 123
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [36, 168]
        point_x = 93
        point_y = 164
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [164, 250]
        point_x = 244
        point_y = 246
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [163, 292]
        point_x = 271
        point_y = 288
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [162, 332]
        point_x = 277
        point_y = 328
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 30
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [35, 376]
        point_x = 110
        point_y = 372
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 300
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')




    elif typeCode == 9:
        hight = 33
        width = 28
        adjust = 3
        font = ImageFont.truetype(font_path, 25)

        # 证号
        back_point = [182, 94]
        point_x = 238
        point_y = 92
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 256
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [52, 130]
        point_x = 107
        point_y = 130
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [284, 127]
        point_x = 325
        point_y = 123
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [384, 127]
        point_x = 460
        point_y = 123
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [36, 168]
        point_x = 93
        point_y = 164
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [164, 250]
        point_x = 244
        point_y = 246
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [163, 292]
        point_x = 271
        point_y = 288
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [162, 332]
        point_x = 277
        point_y = 328
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 30
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [35, 376]
        point_x = 110
        point_y = 372
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 300
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')


    elif typeCode == 10:
        hight = 33
        width = 28
        adjust = 3
        font = ImageFont.truetype(font_path, 25)
        set_color = (110,110,110)

        # 证号
        back_point = [193, 103]
        point_x = 250
        point_y = 102
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 256
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 姓名
        back_point = [62, 138]
        point_x = 107
        point_y = 135
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 性别
        back_point = [298, 134]
        point_x = 336
        point_y = 132
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [392, 131]
        point_x = 460
        point_y = 130
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 地址
        back_point = [61, 172]
        point_x = 118
        point_y = 168
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [186, 246]
        point_x = 261
        point_y = 244
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [186, 285]
        point_x = 296
        point_y = 283
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 131
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [184, 327]
        point_x = 285
        point_y = 325
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 30
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 有效日期
        back_point = [59, 372]
        point_x = 135
        point_y = 370
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 300
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')


    elif typeCode == 11:
        hight = 80
        width = 65
        adjust = 8
        font = ImageFont.truetype(font_path, 60)
        set_color = (0,0,0)

        # 姓名
        back_point = [462, 332]
        point_x = 710
        point_y = 320
        draw.text((point_x + offset1, point_y + offset2), name, font=font, fill=set_color)
        length = len(name) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "姓名' + name + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 驾照类型
        back_point = [462, 480]
        point_x = 710
        point_y = 470
        draw.text((point_x + offset1, point_y + offset2), cartype, font=font, fill=set_color)
        length = len(cartype) * 40
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "准驾车型' + cartype + '", "points": ' + str(
                        point_all) + ', "difficult": false}, ')

        # 扣分
        back_point = [462, 627]
        point_x = 710
        point_y = 617
        draw.text((point_x + offset1, point_y + offset2), (str(penalty) + '分'), font=font, fill=set_color)
        length = len(str(penalty)) * 40 + 65
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "累计记分' + str(penalty) + '分' + '", "points": ' + str(
                        point_all) + ', "difficult": false}, ')

        # 签发日期
        back_point = [462, 780]
        point_x = 777
        point_y = 770
        draw.text((point_x + offset1, point_y + offset2), str(issue_date), font=font, fill=set_color)
        length = 328
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "初次领证日期' + str(issue_date) + '", "points": ' + str(
                     point_all) + ', "difficult": false}, ')

        # 证号
        back_point = [50, 1040]
        point_x = 180
        point_y = 1030
        draw.text((point_x + offset1, point_y + offset2), cid, font=font, fill=set_color)
        length = 620
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "证号' + cid + '", "points": ' + str(point_all) + ', "difficult": false}, ')



        # 性别
        back_point = [50, 1155]
        point_x = 180
        point_y = 1145
        draw.text((point_x + offset1, point_y + offset2), sex, font=font, fill=set_color)
        length = len(sex) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "性别' + sex + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 生日
        back_point = [500, 1155]
        point_x = 700
        point_y = 1145
        draw.text((point_x + offset1, point_y + offset2), str(birthday), font=font, fill=set_color)
        length = 330
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')

        # 国籍
        back_point = [50, 1270]
        point_x = 180
        point_y = 1260
        draw.text((point_x + offset1, point_y + offset2), '中国', font=font, fill=set_color)
        length = len("中国") * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "国籍中国", "points": ' + str(point_all) + ', "difficult": false}, ')

        #档案编号
        back_point = [500, 1270]
        point_x = 700
        point_y = 1260
        draw.text((point_x + offset1, point_y + offset2), str(file_code), font=font, fill=set_color)
        length = 400
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "出生日期' + str(birthday) + '", "points": ' + str(
                    point_all) + ', "difficult": false}, ')


        # 有效日期
        back_point = [50, 1385]
        point_x = 250
        point_y = 1375
        draw.text((point_x + offset1, point_y + offset2), str(startValid) + " 至 " + str(endValid), font=font,
                  fill=set_color)
        length = 738
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "有效期限' + str(startValid) + " 至 " + str(endValid) + '", "points": ' + str(
                    point_all) + ', "difficult": false}')


    elif typeCode == 12:
        hight = 80
        width = 65
        adjust = 8
        font = ImageFont.truetype(font_path, 60)
        set_color = (0,0,0)

        # 地址
        back_point = [50, 390]
        point_x = 257
        point_y = 380
        draw.text((point_x + offset1, point_y + offset2), address, font=font, fill=set_color)
        length = len(address) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "住址' + address + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        # 签发机关
        back_point = [50, 560]
        point_x = 257
        point_y = 550
        draw.text((point_x + offset1, point_y + offset2), address + '公安局', font=font, fill=set_color)
        length = (len(address) + 3) * width
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "发证机关' + address + '公安局' + '", "points": ' + str(point_all) + ', "difficult": false}, ')

        #记录
        back_point = [50, 728]
        point_x = 257
        point_y = 718
        draw.text((point_x + offset1, point_y + offset2), str(cartype + '自' + str(issue_date.year) + '年' + str(issue_date.month) + '月' + str(issue_date.day)) + '日起。', font=font, fill=set_color)
        length = (len(cartype) - 2) * 40 + 330 + (5 * width)
        point_all = getFourPoint(back_point, point_x, point_y, length, hight, offset1, offset2, adjust)
        with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "' + cartype + '自' + str(issue_date.year) + '年' + str(
                    issue_date.month) + '月' + str(issue_date.day) + '日起。' + '", "points": ' + str(
                    point_all) + ', "difficult": false}')

    bk_img = np.array(img_pil)

    # 输出

    # label.txt结尾
    with open("DL_output/Label.txt", "a", encoding='utf-8') as file:
        file.write("]\n")

    # 写入确认信息
    with open("DL_output/fileState.txt", "a", encoding='utf-8') as file:
        file.write('D:\文件\JH\DLgenerator\DL_output\\' + filename + ".jpg\t1\n")


    # cv2.imshow(filename, bk_img)
    # cv2.waitKey()
    cv2.imwrite("DL_output/" + filename + ".jpg", bk_img)

# gbk_trans_utf8('DL_output/Label.txt')
# gbk_trans_utf8('DL_output/fileState.txt')
