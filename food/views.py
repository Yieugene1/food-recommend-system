import random
from recommend_food import UserCF
from django.shortcuts import render, HttpResponse, redirect
from food.models import Userinfo, Userinfo1
from food import models
from django import forms
from django.db.models import Q, QuerySet
import json
from django.http import JsonResponse
from 余弦相似度 import cosine_similarity


def index(request):
    return render(request, '主页面.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        hobby1 = request.POST.get('hobby1')
        user = Userinfo1.objects.filter(name=username)
        if user:
            message = "账号已经注册过"
            return render(request, '主页面.html', {'message': message})
        else:
            Userinfo1.objects.create(name=username, password=password, hobby1=hobby1)
            message = "账号注册成功"

            return render(request, '主页面.html', {'message': message})


def login(request):
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password1 = request.POST.get('password1')

        user = Userinfo1.objects.filter(name=username1).first()

        try:
            if username1 == user.name and password1 == user.password:
                hobby1 = user.hobby1
                message = "登录成功"

                request.session['info'] = {'username': username1, 'password': password1, 'hobby1': hobby1}
                return render(request, 'main2.html', {'message': message})
            else:
                message = "密码不正确"
                return render(request, '主页面.html', {'message': message})
        except:
            message = "账号不正确"
            return render(request, '主页面.html', {'message': message})


def main2(request):
    info = request.session.get('info')
    food = models.mypicture.objects.filter(class1=info["hobby1"])[0:6]
    username = info['username']
    browse = models.browse.objects.filter(user_name=username).values('main_id').order_by('-id')[0:3]
    aa = models.mypicture.objects.filter(user=111111113)
    for i in browse:
        foods_list = models.mypicture.objects.filter(id=i['main_id'])
        aa = foods_list | aa

    # mm = mm = ['Sophie Williams', 'George Edwards', 'Emily Brown', 'Harry Thompson', 'Olivia Davis', 'Lewis Clark',
    #            'Grace Green', 'Jack Wright', 'Charlotte Robinson', 'Samuel Taylor', 'Amelia Jackson',
    #            'William Anderson', 'Isabella White', 'Thomas Parker', 'Alice Carter', 'Benjamin Wilson',
    #            'Poppy Turner', 'Ethan Hill', 'Lily Scott', 'Edward Young', 'Ava Cooper', 'James Mitchell',
    #            'Ella King', 'Joseph Ward', 'Mia Collins', 'Jacob Lee', 'Freya Hall', 'Daniel Baker',
    #            'Maisie Bailey', 'Oscar Phillips', 'Chloe Foster', 'Alexander Wood', 'Millie Murphy', 'Henry Evans',
    #            'Imogen Price', 'Leo Fisher', 'Scarlett Hunter', 'Mason Brooks', 'Phoebe Hughes', 'Joshua Ellis',
    #            'Daisy Owen', 'Oliver Reed', 'Jasmine Palmer', 'Ryan Richardson', 'Holly Morgan', 'Noah Wright',
    #            'Matilda Kelly', 'Nathan Simpson', 'Rosie Harrison', 'Isaac Powell', 'Lucy Murray', 'Max Coleman',
    #            'Evie Foster', 'Felix Jenkins', 'Aria Long', 'Sebastian Baker', 'Elizabeth Cox', 'Elijah Cook',
    #            'Martha Russell', 'Adam Butler', 'Eleanor Ford', 'Patrick West', 'Maisy Mason', 'Toby Green',
    #            'Harriet Ellis', 'Charles Bell', 'Sienna Cox', 'Luke Atkins', 'Ruby Hunt', 'David Griffiths',
    #            'Erin Hayes', 'Freddie Clarke', 'Summer Patel', 'Christopher Stone', 'Elsie Richards',
    #            'Gabriel Whitehead', 'Leah Osborne', 'Louis Harrison', 'Faith Marshall', 'Noah Powell', 'Lydia Lowe',
    #            'Aaron Knight', 'Eva Fletcher', 'Ethan Woodcock', 'Eleanor Sharp', 'Aidan Burns', 'Isabelle Francis',
    #            'Henry Goodwin', 'Georgia Mills', 'Isaac Black', 'Lottie Johnstone', 'Samuel Holmes',
    #            'Jasmine Collins', 'Cameron Davenport', 'Poppy Kendall', 'Alexander Khan', 'Arabella Gallagher',
    #            'Joshua West', 'Matilda Holden', 'William Lloyd', 'Alice Harrison', 'Dylan Houghton', 'Bella Mills',
    #            'Isaac Cross', 'Gabrielle Gibson', 'Charlie Morrison', 'Phoebe Farrell', 'Thomas Parsons',
    #            'Amelia Howarth', 'Harry Connor', 'Imogen Atkins', 'Oscar Baker', 'Freya Bailey', 'Oliver Peterson',
    #            'Lily Burke', 'Jacob Barker', 'Sophie Slater', 'George Burton', 'Emily Bowers', 'Lewis Mcdonald',
    #            'Grace Ross', 'Jack Webster', 'Charlotte Sharpe', 'Samuel Quinn', 'Amelia Davidson',
    #            'William Foster', 'Isabella Short', 'Thomas Howard', 'Alice Ridley', 'Benjamin Spencer',
    #            'Poppy Flynn', 'Ethan Steele', 'Lily Matthews', 'Edward Crawford', 'Ava Hanson', 'James Fraser',
    #            'Ella Hyde', 'Joseph Rhodes', 'Mia Palmer', 'Jacob Mclean', 'Freya Gray', 'Daniel Davidson',
    #            'Maisie Walsh', 'Oscar Doyle', 'Chloe Blackwell', 'Alexander Harvey', 'Millie Higgins',
    #            'Henry Wilkins', 'Imogen Bevan', 'Leo Garner', 'Scarlett David', 'Mason Holloway', 'Phoebe OBrien',
    #            'Joshua Thornton', 'Daisy Marsh', 'Oliver Waters', 'Jasmine Hart', 'Ryan Price', 'Holly Knight', 'Noah'
    #                                                                                                             'Fitzgerald',
    #            'Matilda Griffiths', 'Nathan Byrne', 'Rosie Spencer', 'Isaac Collins', 'Lucy Bell', 'Max'
    #                                                                                                'Rayner',
    #            'Evie Houghton', 'Felix Randall', 'Aria Chapman', 'Sebastian Lloyd', 'Elizabeth Salter', 'Elijah'
    #                                                                                                     'Cunningham',
    #            'Martha Whitfield', 'Adam Kirk', 'Eleanor Abbott', 'Patrick Simpson', 'Maisy Hamilton', 'Toby'
    #                                                                                                    'Brown',
    #            'Harriet Shaw', 'Charles Parker', 'Sienna Yates', 'Luke Armstrong', 'Ruby Greene', 'eugene']
    #
    # for x in mm:
    #         for i in range(16):
    #             a = random.uniform(3.8, 5.0)
    #             score11 = float(round(a, 1))
    #             cc = random.randint(1, 383)
    #             xx = models.motivation.objects.filter(user_name=mm, food_id=cc)
    #             if not xx:
    #                 models.motivation.objects.create(user_name=x, food_id=cc, user_score=score11)
    return render(request, 'main2.html', {'info': info, 'food': food, 'browse': aa})


def updateinfo(request):
    if request.method == 'POST':
        a = random.uniform(4.7, 5.0)
        score = str(round(a, 1))
        user1 = request.FILES.get('photo').name.split('.')[0]
        class3 = request.POST.get('class2')
        c = models.mypicture.objects.filter(user=user1, class2=class3)
        c1 = models.mypicture.objects.filter(user=user1)

        if c:
            return HttpResponse("失败")
        else:
            if c1:
                score1 = models.mypicture.objects.filter(user=user1).values_list('score')[0]
                score = score1
            new_img = models.mypicture(
                photo=request.FILES.get('photo'),  # 拿到图片
                user=request.FILES.get('photo').name.split('.')[0],
                intro=request.POST.get('intro'),
                class1=request.POST.get('class1'),
                country=request.POST.get('country'),
                taste=request.POST.get('taste'),
                class2=request.POST.get('class2'),
                score=score
            )
            new_img.save()  # 保存图片
            return HttpResponse('上传成功！')

    return render(request, 'aaa.html')


def food1(request):
    return render(request, '美食1.html')


def food2(request):
    return render(request, '美食2.html')


def food3(request):
    return render(request, '美食3.html')


def food4(request):
    return render(request, '美食4.html')


def logout(request):
    request.session.clear()
    return redirect('/main/')


def g(request):
    return render(request, '继承.html')


def search(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["user__contains"] = search_data
        pi = models.mypicture.objects.filter(**data_dict, class2='pi').order_by('?')[0:9]
        fei = models.mypicture.objects.filter(**data_dict, class2='fei').order_by('?')[0:9]
        la = models.mypicture.objects.filter(**data_dict, taste='la').order_by('?')[0:9]
        yun = models.mypicture.objects.filter(**data_dict, class2='yun').order_by('?')[0:9]
        gao = models.mypicture.objects.filter(**data_dict, class2='gao').order_by('?')[0:9]
        tian = models.mypicture.objects.filter(**data_dict, taste='tian').order_by('?')[0:9]
        zhong = models.mypicture.objects.filter(**data_dict, taste='zhong').order_by('?')[0:9]
        xian = models.mypicture.objects.filter(**data_dict, taste='xian').order_by('?')[0:9]
        wai = models.mypicture.objects.filter(**data_dict, country='wai').order_by('?')[0:9]
        tian1 = []
        tian2 = []
        for i in tian:
            if i.user not in tian2:
                tian1.append(i)
                tian2.append(i.user)
        zhong1 = []
        zhong2 = []
        for i in zhong:
            if i.user not in zhong2:
                zhong1.append(i)
                zhong2.append(i.user)
        xian1 = []
        xian2 = []
        for i in xian:
            if i.user not in xian2:
                xian1.append(i)
                xian2.append(i.user)
        wai1 = []
        wai2 = []
        for i in wai:
            if i.user not in wai2:
                wai1.append(i)
                wai2.append(i.user)
        queryset = models.mypicture.objects.filter(~Q(class2='pi'), ~Q(class2='yun'),
                                                   ~Q(class2='gao'), **data_dict).order_by('?')[0:9]

    return render(request, 'search.html',
                  {"queryset": queryset, "yun": yun, "la": la, "gao": gao, "tian": tian1, "xian": xian1,
                   "zhong": zhong1,
                   "wai": wai1,
                   "fei": fei, "pi": pi, "search_data": search_data})


def 川菜(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 9
    end = (page) * 9
    next = "http://127.0.0.1:8000/chuan/?page={}".format(page + 1)
    food = models.mypicture.objects.filter(class1='1').order_by('?')[start:end]
    return render(request, '川菜.html', {"food": food, "next": next})


def 徽菜(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 9
    end = (page) * 9
    next = "http://127.0.0.1:8000/chuan/?page={}".format(page + 1)
    food = models.mypicture.objects.filter(class1='4').order_by('?')[start:end]
    return render(request, '徽菜.html', {"food": food})


def 西安菜(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 9
    end = (page) * 9
    next = "http://127.0.0.1:8000/zhe/?page={}".format(page + 1)
    food = models.mypicture.objects.filter(class1='6').order_by('?')[start:end]
    return render(request, '浙菜.html', {"food": food, "next": next})


def 湘菜(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 9
    end = (page) * 9
    next = "http://127.0.0.1:8000/xiang/?page={}".format(page + 1)
    food = models.mypicture.objects.filter(class1='3').order_by('?')[start:end]
    return render(request, '湘菜.html', {"food": food, "next": next})


def 粤菜(request):
    info = request.session.get("info")
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 9
    end = (page) * 9
    next = "http://127.0.0.1:8000/yue/?page={}".format(page + 1)
    food = models.mypicture.objects.filter(class1='2').order_by('?')[start:end]
    return render(request, '粤菜.html', {"food": food, "next": next})


def 韩国(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.filter(class1='han').order_by('?')[0:6]
    return render(request, '韩国.html', {"food": food})


def 法国(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.filter(class1='fa').order_by('?')[0:6]
    return render(request, '法国.html', {"food": food})


def 意大利(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.filter(class1='yi').order_by('?')[0:6]
    return render(request, '意大利.html', {"food": food})


def 日本(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.filter(class1='ri').order_by('?')[0:6]
    return render(request, '日本.html', {"food": food})


def 苏菜(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.all()
    return render(request, '苏菜.html', {"food": food})


def 闽菜(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.all()
    return render(request, '闽菜.html', {"food": food})


def 鲁菜(request):
    info = request.session.get("info")
    if not info:
        return redirect('/main/')
    food = models.mypicture.objects.all()
    return render(request, '鲁菜.html', {"food": food})


def detail_foods(request, gid):
    info = request.session.get('info')
    foods = models.mypicture.objects.get(pk=gid)
    oo = models.mypicture.objects.filter(id=gid).values('class2')[0]
    leisi = models.mypicture.objects.filter(class2=oo['class2']).order_by('?')[0:3]
    print(gid)
    username = info['username']
    cc = models.browse.objects.filter(main_id=gid, user_name=username)
    browse = models.browse.objects.filter(user_name=username).count()
    if browse >= 5:
        first_obj = models.browse.objects.filter(user_name=username).first()
        first_obj.delete()
    if not cc:
        models.browse.objects.create(main_id=gid, user_name=username)

    food_name = models.user_save.objects.filter(user_name=username, food_name=foods.user)
    if food_name:
        x = 0
    elif not food_name:
        x = 1
    return render(request, 'detail_foods.html', {'foods': foods, 'info': info, 'x': x, 'leisi': leisi})


def foods_save(request):
    info = request.session.get('info')
    if not info:
        return JsonResponse({'msg': 'unlogin'})
    username = info['username']
    id = request.GET.get('id')
    flag = request.GET.get('flag')
    foods = models.mypicture.objects.get(pk=id)
    if foods:
        if flag == 'unsave':
            foods.save_num -= 1
            models.user_save.objects.filter(food_name=foods.user).delete()
        elif flag == 'save':
            foods.save_num += 1
            models.user_save.objects.create(user_name=username, food_name=foods.user, food_photo=foods.photo,
                                            )
        foods.save()
        return JsonResponse({'msg': 'success', 'number': foods.save_num})
    else:
        return JsonResponse({'msg': 'fail'})


def user_save(request):
    info = request.session.get('info')
    username = info['username']
    foods_list = models.user_save.objects.filter(user_name=username).values('food_photo')

    aa = models.mypicture.objects.filter(user=111111113)
    for i in foods_list:
        foods_list = models.mypicture.objects.filter(photo=i['food_photo'])
        aa = foods_list | aa

    return render(request, 'user_save.html', {'info': info, 'foods_list': aa})


def recommend(request):
    page = request.GET.get("page", 1)
    info = request.session.get('info')


def submit_rating(request):
    info = request.session.get('info')
    username = info['username']
    score = request.GET.get("score")
    score = float(score)
    food_id = request.GET.get("id")
    comment = request.GET.get("comment")
    aa = models.motivation.objects.filter(user_name=username, food_id=food_id)
    if not aa:
        models.motivation.objects.create(user_name=username, food_id=food_id, food_comment=comment, user_score=score)
    # 在这里进行保存评分的操作
    return JsonResponse({"score": score, 'comment': comment})


def recommend_user(request):
    info = request.session.get('info')
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    username = info['username']
    databases = models.motivation.objects.all().values()
    aa = []
    for i in databases:
        user = i['user_name']
        food_id = i['food_id']
        user_score = i['user_score']
        data = (user, food_id, user_score)
        aa.append(data)

    result = {}
    for d in aa:
        if d[0] not in result:
            result[d[0]] = {}
        result[d[0]][str(d[1])] = d[2]
    user_cf = UserCF(result)
    sim_matrix = user_cf.similarity_matrix()
    recommendations = user_cf.recommend(username, sim_matrix)
    aa = models.mypicture.objects.filter(user=111111113)
    for i in recommendations[0:15]:
        id = int(i[0])
        print('美食：',id,'评分：',i[1])
        tuijian = models.mypicture.objects.filter(main_id=id)
        aa = tuijian | aa
    return render(request, 'recommend_user.html', {'food_recommend': aa})


def recommend_all(request):
    info = request.session.get('info')
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    return render(request, 'recommend_all.html')


def browse_user(request):
    info = request.session.get('info')
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    username = info['username']
    foods_list = models.browse.objects.filter(user_name=username).values('main_id').order_by('-id')
    aa = models.mypicture.objects.filter(user=111111113)
    for i in foods_list:
        foods_list = models.mypicture.objects.filter(id=i['main_id']).order_by('-id')
        aa = foods_list | aa
    return render(request, 'browse_user.html', {'info': info, 'foods_list': aa})


def 检索1(request):
    import jieba
    all_docs = [['腊', '味', '煲', '仔', '饭'], ['八', '宝', '饭'], ['广', '式', '腊', '味', '糯', '米', '饭'],
                ['咖', '喱', '豆', '腐', '虾', '仁', '盖', '浇', '饭'],
                ['简', '单', '又', '下', '饭', '肥', '牛', '饭'],
                ['电', '饭', '煲', '里', '美', '味', '焖', '饭', '夏', '天', '不', '再', '热', '火', '朝', '天'],
                ['日', '式', '肥', '牛', '饭'], ['梅', '菜', '五', '花', '豇', '豆', '饭'],
                ['酸', '甜', '菠', '萝', '饭'], ['台', '式', '卤', '肉', '饭', '瘦', '肉', '版'],
                ['什', '锦', '炒', '饭'], ['扬', '州', '炒', '饭'], ['自', '制', '蒲', '烧', '鳗', '鱼', '饭'],
                ['最', '香', '这', '碗', '卤', '肉', '饭'],
                ['这', '么', '美', '味', '芝', '士', '烤', '饭', '团', '带', '出', '去', '野', '餐', '都', '不', '够',
                 '分'], ['血', '糯', '米', '杂', '粮', '饭'], ['腊', '肉', '石', '锅', '拌', '饭'],
                ['红', '薯', '花', '生', '咸', '饭'],
                ['韩', '国', '辣', '白', '菜', '炒', '饭', '看', '韩', '剧', '必', '备', '宵', '夜', '简', '单', '快',
                 '手'], ['韩', '国', '拌', '饭'],
                ['传', '说', '中', '最', '受', '欢', '迎', '宝', '贝', '饭', '紫', '米', '肉', '松', '饭', '团'],
                ['蛋', '包', '饭'], ['咖', '喱', '牛', '肉', '日', '食', '记'], ['酱', '油', '炒', '饭'],
                ['照', '烧', '鸡', '腿', '饭'], ['羊', '排', '手', '抓', '饭'],
                ['香', '肠', '南', '瓜', '什', '锦', '焖', '饭'], ['海', '带', '黄', '豆', '煲', '小', '排'],
                ['鹅', '蛋', '虾', '仁', '蒜', '薹', '炒', '饭'],
                ['减', '脂', '餐', '柠', '檬', '手', '撕', '鸡', '鲜', '嫩', '入', '味', '超', '好', '吃'],
                ['彩', '虹', '沙', '拉', '增', '肌', '减', '脂', '两', '不', '误', '健', '身', '餐'],
                ['蛋', '塔', '水', '果', '减', '脂', '餐'], ['减', '脂', '餐'],
                ['减', '脂', '餐', '蔬', '菜', '丸', '子'], ['减', '脂', '餐', '推', '荐', '低', '脂', '沙', '拉'],
                ['减', '脂', '餐', '酸', '奶', '水', '果', '捞'], ['减', '脂', '餐', '丝', '瓜', '炒', '蛋'],
                ['减', '脂', '餐', '之', '黑', '胡', '椒', '香', '煎', '巴', '沙', '鱼', '柳'],
                ['减', '脂', '餐', '最', '健', '康', '盐', '水', '大', '虾'], ['减', '脂', '水', '果', '餐'],
                ['连', '吃', '三', '天', '都', '不', '腻', '减', '脂', '餐', '凉', '拌', '长', '豆'],
                ['连', '吃', '三', '天', '都', '不', '腻', '减', '脂', '餐', '鸡', '蛋', '炒', '长', '豆'],
                ['快', '手', '减', '脂', '餐', '免', '煮', '荞', '麦', '面'],
                ['三', '天', '都', '吃', '不', '腻', '减', '脂', '餐', '酱', '炖', '小', '鲅', '鱼'],
                ['盐', '水', '菜', '心', '减', '脂', '餐'],
                ['蒸', '玉', '米', '面', '菜', '团', '子', '减', '脂', '主', '食', '代', '餐', '不', '用', '揉', '面',
                 '擀', '皮', '饱', '腹', '低', '卡'], ['减', '脂', '餐', '茄', '子', '烧', '洋', '葱'],
                ['加', '拿', '大', '北', '极', '虾', '口', '蘑', '焗', '蛋', '盅', '减', '脂', '餐', '首', '选'],
                ['非', '油', '炸', '茄', '盒', '烤', '箱', '减', '脂', '餐', '低', '卡', '又', '美', '味'],
                ['低', '脂', '山', '药', '鸡', '肉', '丸', '子', '减', '重', '主', '食', '代', '餐', '好', '吃', '不',
                 '长', '胖'],
                ['减', '脂', '餐', '蒜', '香', '土', '豆', '泥', '凉', '拌', '秋', '葵', '白', '菜', '粉', '条'],
                ['减', '脂', '餐', '鲜', '虾', '蒸', '日', '本', '豆', '腐'],
                ['减', '脂', '餐', '凉', '拌', '紫', '甘', '蓝'], ['减', '脂', '餐', '凉', '拌', '紫', '甘', '蓝'],
                ['减', '脂', '餐', '香', '辣', '过', '瘾', '超', '好', '吃', '菠', '菜', '拌', '平', '菇'],
                ['减', '脂', '餐', '酸', '奶', '水', '果', '捞'], ['蛋', '塔', '水', '果', '减', '脂', '餐'],
                ['彩', '虹', '沙', '拉', '增', '肌', '减', '脂', '两', '不', '误', '健', '身', '餐'],
                ['减', '脂', '餐', '蘑', '菇', '汤'], ['减', '脂', '餐', '茄', '子', '烧', '洋', '葱'],
                ['虫', '草', '菇', '炖', '鸡', '提', '高', '免', '疫', '力', '健', '脾', '养', '胃'],
                ['春', '季', '补', '气', '养', '胃', '健', '脾', '汤'],
                ['春', '日', '限', '定', '健', '脾', '养', '胃', '紫', '薯', '山', '药', '糕'],
                ['脆', '皮', '山', '药', '奶', '酪', '棒', '健', '脾', '养', '胃', '还', '补', '钙'],
                ['低', '热', '量', '山', '药', '饼', '营', '养', '丰', '富', '健', '脾', '养', '胃'],
                ['健', '脾', '养', '胃', '养', '生', '小', '米', '粉', '藕', '糊'],
                ['健', '脾', '养', '胃', '紫', '薯', '淮', '山', '饮'], ['四', '珍', '糕', '健', '脾', '养', '胃'],
                ['五', '谷', '豆', '浆', '养', '生', '补', '血', '健', '脾', '养', '胃'],
                ['香', '糯', '南', '瓜', '小', '饼', '健', '脾', '养', '胃', '小', '零', '嘴'],
                ['健', '脾', '养', '胃', '益', '气', '祛', '湿', '四', '神', '汤'],
                ['健', '脾', '养', '胃', '鲈', '鱼', '浓', '汤'],
                ['健', '脾', '养', '胃', '北', '瓜', '桂', '圆', '粥'],
                ['健', '脾', '养', '胃', '山', '药', '鸡', '滑', '汤'],
                ['健', '脾', '养', '胃', '薏', '米', '山', '药', '汤'],
                ['健', '脾', '养', '胃', '鲈', '鱼', '汤', '超', '鲜'], ['健', '脾', '养', '胃', '粥'],
                ['美', '容', '养', '颜', '健', '脾', '养', '胃', '玫', '瑰', '花', '玉', '米', '西', '米', '羹'],
                ['排', '骨', '山', '药', '汤', '健', '脾', '养', '胃'],
                ['养', '胃', '健', '脾', '入', '秋', '神', '助', '攻', '栗', '子', '焖', '鸡'],
                ['猪', '肚', '鸡', '健', '脾', '养', '胃', '补', '虚', '损'],
                ['最', '适', '合', '秋', '天', '喝', '山', '药', '玉', '米', '排', '骨', '汤', '味', '道', '清', '甜',
                 '鲜', '美', '健', '脾', '养', '胃', '必', '备'],
                ['老', '少', '皆', '宜', '暖', '心', '暖', '胃', '健', '脾', '养', '胃', '小', '米', '山', '药', '粥'],
                ['健', '脾', '养', '胃', '补', '钙', '银', '鱼', '蔬', '菜', '双', '色', '粥', '宝', '宝', '辅', '食'],
                ['芈', '月', '传', '里', '安', '神', '补', '血', '健', '脾', '养', '胃', '红', '枣', '汤'],
                ['多', '妈', '爱', '下', '厨', '健', '脾', '养', '胃', '南', '瓜', '汁'],
                ['宝', '宝', '辅', '食', '比', '番', '茄', '维', '高', '比', '白', '粥', '更', '有', '营', '养', '这',
                 '样', '做', '还', '健', '脾', '养', '胃'],
                ['宝', '宝', '辅', '食', '比', '米', '粥', '米', '糊', '都', '更', '有', '营', '养', '健', '脾', '益',
                 '智', '还', '养', '胃'],
                ['宝', '宝', '健', '脾', '养', '胃', '辅', '食', '红', '枣', '山', '药', '蒸', '糕'],
                ['宝', '宝', '健', '脾', '养', '胃', '山', '药', '饼'],
                ['宝', '宝', '秋', '冬', '食', '疗', '营', '养', '汤', '健', '脾', '养', '胃', '止', '咳', '化', '痰'],
                ['超', '好', '吃', '川', '菜', '水', '煮', '肉', '片', '做', '法', '很', '简', '单', '呦'],
                ['川', '菜', '经', '典', '蚂', '蚁', '上', '树'], ['川', '菜', '经', '典', '太', '白', '鸡'],
                ['川', '菜', '明', '星', '辣', '子', '鸡', '丁'], ['川', '菜', '青', '椒', '回', '锅', '肉'],
                ['川', '菜', '泡', '椒', '猪', '肝', '滑', '嫩', '酸', '爽'],
                ['川', '菜', '鱼', '香', '茄', '饼', '做', '法', '简', '单', '口', '味', '老', '少', '皆', '宜'],
                ['川', '菜', '之', '魂', '回', '锅', '肉'], ['经', '典', '川', '菜', '宫', '保', '鸡', '丁'],
                ['经', '典', '川', '菜', '东', '坡', '肘', '子', '色', '泽', '红', '亮', '肥', '而', '不', '腻'],
                ['跳', '水', '蛙', '地', '道', '川', '菜', '绝', '对', '不', '容', '错', '过', '哦'],
                ['麻', '婆', '豆', '腐', '学', '会', '第', '一', '道', '川', '菜'],
                ['下', '饭', '菜', '鱼', '香', '肉', '丝', '经', '典', '川', '菜', '儿', '童', '家', '常', '版', '家',
                 '常', '菜', '快', '手', '菜', '鱼', '香', '肉', '丝'],
                ['最', '上', '瘾', '绝', '味', '川', '菜', '酸', '辣', '肥', '牛'],
                ['最', '上', '瘾', '绝', '味', '川', '菜', '宜', '宾', '燃', '面'],
                ['红', '油', '辣', '子', '川', '菜', '重', '头', '戏'],
                ['经', '典', '川', '菜', '江', '津', '肉', '片'],
                ['最', '上', '瘾', '绝', '味', '川', '菜', '麻', '婆', '山', '药'],
                ['最', '上', '瘾', '绝', '味', '川', '菜', '豆', '花', '鱼', '片'],
                ['徽', '菜', '臭', '鳜', '鱼', '在', '家', '做', '起', '来', '吃', '过', '都', '说', '不', '比', '杨',
                 '记', '兴', '差'], ['红', '烧', '鸡', '爪'], ['腐', '竹', '蒸', '排', '骨'],
                ['徽', '菜', '蒸', '辣', '椒', '蒸', '海', '带'], ['经', '典', '徽', '菜', '香', '菇', '酿', '肉'],
                ['巨', '巨', '巨', '好', '吃', '鱿', '鱼', '这', '个', '做', '法', '我', '怎', '么', '没', '早', '点',
                 '发', '现'], ['茶', '油', '炒', '土', '鸡', '经', '典', '湘', '菜'],
                ['超', '下', '饭', '经', '典', '湘', '菜', '金', '钱', '蛋'],
                ['经', '典', '湘', '菜', '酸', '豆', '角', '炒', '肉', '末'],
                ['川', '湘', '菜', '馆', '必', '点', '菜', '豆', '角', '炒', '茄', '子'],
                ['创', '意', '湘', '菜', '剁', '椒', '海', '参', '斑'],
                ['剁', '椒', '鱼', '头', '湘', '菜', '香', '韵'],
                ['经', '典', '湘', '菜', '擂', '辣', '椒', '茄', '子', '皮', '蛋', '开', '胃', '解', '腻'],
                ['经', '典', '湘', '菜', '萝', '卜', '干', '炒', '腊', '肉'],
                ['美', '食', '丨', '湘', '菜', '经', '典', '奇', '丑', '无', '比', '却', '美', '味', '无', '穷', '猪',
                 '血', '丸', '子'], ['芹', '菜', '炒', '肉', '组', '长', '教', '你', '做', '湘', '菜'],
                ['肉', '蛋', '卷', '组', '长', '教', '你', '做', '湘', '菜'],
                ['湘', '菜', '娇', '小', '可', '人', '一', '口', '酿', '豆', '腐'],
                ['湘', '菜', '经', '典', '农', '家', '小', '炒', '肉', '好', '吃', '秘', '诀'],
                ['湘', '菜', '剁', '椒', '蒸', '芋', '头', '剁', '辣', '椒', '蒸', '芋', '头', '仔'],
                ['湘', '菜', '剁', '椒', '鱼', '头', '正', '宗', '做', '法', '详', '解'],
                ['湘', '菜', '开', '味', '鱼', '头', '不', '一', '般', '好', '吃'],
                ['湘', '菜', '农', '家', '炒', '鸡', '丁', '迷', '迭', '香'],
                ['湘', '菜', '酸', '萝', '卜', '炒', '猪', '肚', '肚', '尖', '让', '猪', '肚', '爽', '脆', '秘', '诀'],
                ['茄', '子', '肉', '末', '组', '长', '教', '你', '做', '湘', '菜'],
                ['经', '典', '湘', '菜', '擂', '辣', '椒', '茄', '子', '皮', '蛋', '开', '胃', '解', '腻'],
                ['菠', '萝', '鸡', '夏', '日', '清', '爽', '开', '胃', '粤', '菜'],
                ['避', '风', '塘', '茄', '子', '在', '家', '也', '能', '做', '出', '粤', '菜', '馆', '里', '港', '味',
                 '菜', '品'], ['超', '下', '饭', '粤', '菜', '梅', '菜', '剁', '猪', '肉'],
                ['虫', '草', '花', '蒸', '鸡', '滋', '补', '粤', '菜'],
                ['大', '厨', '风', '味', '粤', '菜', '早', '餐', '宵', '夜', '叉', '烧', '炒', '河', '粉'],
                ['广', '东', '人', '从', '小', '吃', '到', '大', '经', '典', '粤', '菜', '玉', '米', '蒸', '肉', '饼'],
                ['广', '东', '粤', '菜', '之', '红', '枣', '枸', '杞', '香', '菇', '蒸', '鲜', '鸡'],
                ['广', '州', '文', '昌', '鸡', '粤', '菜', '十', '大', '名', '菜', '之', '一'],
                ['教', '你', '快', '手', '做', '粤', '菜', '经', '典', '上', '汤', '菜', '心'],
                ['皆', '食', '得', '粤', '菜', '豆', '角', '炒', '植', '物', '蛋'],
                ['经', '典', '粤', '菜', '豆', '豉', '鸭'], ['经', '典', '粤', '菜', '话', '梅', '猪', '手'],
                ['向', '粤', '菜', '大', '师', '傅', '学', '做', '干', '炒', '牛', '河'],
                ['粤', '菜', '醇', '香', '味', '玫', '瑰', '醉', '鸽'],
                ['粤', '菜', '月', '子', '食', '谱', '驱', '寒', '暖', '胃', '猪', '脚', '姜', '醋'],
                ['粤', '菜', '茶', '点', '芋', '丝', '鲮', '鱼', '球'],
                ['粤', '菜', '上', '汤', '豆', '苗', '做', '好', '上', '汤', '窍', '门'],
                ['粤', '菜', '沙', '姜', '焖', '鸡'], ['粤', '菜', '南', '乳', '鸡'],
                ['粤', '菜', '丝', '瓜', '蒸', '鱼', '片'],
                ['粤', '菜', '咕', '咾', '肉', '咕', '噜', '肉', '小', '酥', '肉', '努', '力', '做', '香', '酥', '小',
                 '肉', '肉', '吃', '记', '方', '法'], ['粤', '菜', '广', '式', '烧', '鸭', '腿', '快', '手', '版'],
                ['粤', '菜', '手', '打', '鲮', '鱼', '丸', '鲮', '鱼', '滑'],
                ['粤', '菜', '咸', '鱼', '茄', '子', '煲', '附', '茄', '子', '不', '油', '腻', '小', '窍', '门'],
                ['粤', '式', '白', '切', '鸡', '粤', '菜', '师', '傅', '做', '法'],
                ['啫', '啫', '鸡', '肉', '煲', '鲜', '嫩', '多', '汁', '超', '好', '吃', '粤', '菜'],
                ['经', '典', '粤', '菜', '豆', '豉', '鸭'], ['经', '典', '粤', '菜', '话', '梅', '猪', '手'],
                ['清', '蒸', '石', '斑', '鱼', '粤', '菜', '各', '种', '蒸', '鱼', '都', '适', '用'],
                ['粤', '菜', '油', '条', '蒸', '水', '蛋', '秒', '光', '碗', '饭'],
                ['麻', '辣', '鸡', '丝', '特', '别', '过', '瘾', '经', '典', '川', '菜'],
                ['川', '菜', '不', '用', '片', '鱼', '酸', '菜', '鱼', '龙', '利', '鱼', '新', '吃', '法'],
                ['最', '上', '瘾', '绝', '味', '川', '菜', '麻', '婆', '山', '药'],
                ['中', '国', '八', '大', '菜', '系', '鲁', '菜', '系', '列', '之', '锅', '塌', '豆', '腐'],
                ['中', '国', '八', '大', '菜', '系', '鲁', '菜', '系', '列', '之', '锅', '塌', '豆', '腐'],
                ['菜', '借', '饼', '香', '饼', '借', '菜', '味', '经', '典', '鲁', '菜', '地', '锅', '鸡', '连', '锅',
                 '端', '着', '上', '桌', '吃', '更', '有', '味', '道'],
                ['葱', '烧', '蘑', '菇', '传', '统', '鲁', '菜'], ['家', '常', '鲁', '菜', '萝', '卜', '咸', '汤'],
                ['家', '常', '嫩', '滑', '木', '须', '肉', '片', '传', '统', '木', '须', '肉', '家', '常', '菜', '下',
                 '饭', '菜', '鲁', '菜'],
                ['家', '常', '制', '作', '鲁', '菜', '传', '统', '名', '菜', '木', '樨', '肉'],
                ['鲁', '菜', '系', '列', '油', '焖', '大', '虾'],
                ['鲁', '菜', '名', '吃', '黄', '焖', '鸡', '米', '饭'],
                ['鲁', '菜', '经', '典', '家', '常', '黄', '焖', '鸡'],
                ['鲁', '菜', '经', '典', '葱', '爆', '海', '参'],
                ['鲁', '菜', '前', '三', '名', '之', '咸', '汤', '徐', '志', '胜', '何', '广', '智', '强', '推'],
                ['凉', '拌', '八', '瓜', '鱼', '家', '传', '咸', '鲜', '鲁', '菜'],
                ['经', '典', '鲁', '菜', '之', '蒜', '爆', '羊', '肉'],
                ['健', '脾', '养', '胃', '花', '生', '猪', '肚', '汤'],
                ['健', '脾', '养', '胃', '南', '瓜', '小', '米', '糊'],
                ['健', '脾', '养', '胃', '山', '药', '红', '枣', '小', '米', '藜', '麦', '粥'],
                ['降', '火', '祛', '湿', '健', '脾', '养', '胃', '咸', '猪', '骨', '莲', '子', '芡', '实', '粥'],
                ['美', '容', '养', '颜', '健', '脾', '养', '胃', '玫', '瑰', '花', '玉', '米', '西', '米', '羹'],
                ['小', '米', '紫', '薯', '南', '瓜', '粥', '冬', '季', '健', '脾', '养', '胃', '好', '粥', '道', '威',
                 '厨', '艺'], ['养', '胃', '健', '脾', '山', '药', '红', '枣', '枸', '杞', '粥'],
                ['养', '胃', '健', '脾', '猴', '头', '菇', '山', '药', '排', '骨', '汤'],
                ['养', '胃', '健', '脾', '炒', '时', '蔬'],
                ['养', '生', '豆', '浆', '之', '养', '胃', '健', '脾', '养', '血', '安', '神', '豆', '浆', '破', '壁',
                 '机', '版'],
                ['小', '米', '紫', '薯', '南', '瓜', '粥', '冬', '季', '健', '脾', '养', '胃', '好', '粥', '道', '威',
                 '厨', '艺'],
                ['最', '适', '合', '秋', '天', '喝', '山', '药', '玉', '米', '排', '骨', '汤', '味', '道', '清', '甜',
                 '鲜', '美', '健', '脾', '养', '胃', '必', '备'],
                ['老', '少', '皆', '宜', '暖', '心', '暖', '胃', '健', '脾', '养', '胃', '小', '米', '山', '药', '粥'],
                ['健', '脾', '养', '胃', '山', '药', '鸡', '滑', '汤'],
                ['奶', '香', '浓', '郁', '健', '脾', '养', '胃', '椰', '蓉', '蔓', '越', '莓', '山', '药', '球'],
                ['山', '药', '芙', '蓉', '汤', '健', '脾', '又', '养', '胃'],
                ['健', '脾', '山', '药', '鸡', '蛋', '汤', '宝', '宝', '养', '胃', '羹', '提', '高', '免', '疫', '力'],
                ['宝', '宝', '辅', '食', '宝', '宝', '便', '秘', '千', '万', '别', '急', '着', '用', '开', '塞', '露',
                 '食', '疗', '先', '行', '还', '能', '健', '脾', '养', '胃'],
                ['最', '适', '合', '秋', '天', '喝', '山', '药', '玉', '米', '排', '骨', '汤', '味', '道', '清', '甜',
                 '鲜', '美', '健', '脾', '养', '胃', '必', '备'],
                ['健', '脾', '养', '胃', '鲈', '鱼', '汤', '超', '鲜'],
                ['健', '脾', '养', '胃', '板', '栗', '山', '药', '排', '骨', '汤'],
                ['藜', '麦', '小', '米', '南', '瓜', '粥', '健', '脾', '养', '胃', '减', '脂', '粥'],
                ['香', '菇', '虾', '仁', '粥', '味', '道', '极', '其', '鲜', '美', '养', '胃', '健', '脾', '灵', '魂',
                 '搭', '配'], ['健', '脾', '养', '胃', '暖', '身', '生', '姜', '板', '栗', '山', '药', '甜', '汤'],
                ['健', '脾', '养', '胃', '花', '生', '猪', '肚', '汤'],
                ['重', '庆', '街', '头', '人', '气', '小', '吃', '章', '鱼', '丸', '子'],
                ['延', '吉', '小', '吃', '沾', '串', '在', '家', '打', '造', '风', '美', '食'],
                ['胭', '脂', '藕', '片', '能', '排', '毒', '养', '颜', '小', '吃'],
                ['胭', '脂', '藕', '片', '能', '排', '毒', '养', '颜', '小', '吃'],
                ['旋', '风', '土', '豆', '塔', '夜', '市', '小', '吃', '完', '美', '拿', '捏', '烤', '箱', '版', '更',
                 '健', '康', '酥', '脆', '够', '味', '超', '过', '瘾'],
                ['小', '吃', '界', '香', '饽', '饽', '街', '边', '桥', '头', '排', '骨', '在', '家', '可', '以', '自',
                 '己', '做', '呢'], ['驴', '打', '滚', '北', '京', '小', '吃'],
                ['驴', '打', '滚', '老', '北', '京', '小', '吃', '在', '家', '就', '能', '做', '一', '口', '一', '个',
                 '糯', '叽', '叽'], ['暖', '冬', '小', '吃', '芝', '心', '地', '瓜', '丸'],
                ['年', '货', '小', '吃', '一', '一', '猫', '耳', '朵'],
                ['停', '不', '下', '来', '海', '苔', '花', '生', '年', '味', '小', '吃'],
                ['老', '北', '京', '传', '统', '小', '吃', '艾', '窝', '窝'],
                ['看', '球', '追', '剧', '必', '备', '辣', '卤', '小', '吃'],
                ['风', '味', '小', '吃', '麻', '辣', '花', '生'],
                ['地', '方', '特', '色', '小', '吃', '金', '华', '酥', '饼'],
                ['老', '北', '京', '小', '吃', '驴', '打', '滚'],
                ['上', '海', '名', '小', '吃', '家', '庭', '版', '葱', '油', '拌', '面', '操', '作', '简', '单', '又',
                 '好', '吃'],
                ['外', '酥', '里', '嫩', '鲜', '蔬', '土', '豆', '饼', '简', '单', '快', '手', '营', '养', '早', '餐',
                 '可', '做', '小', '吃', '可', '做', '主', '食'],
                ['麻', '辣', '藕', '湖', '南', '街', '边', '小', '吃'],
                ['分', '享', '美', '味', '小', '吃', '加', '拿', '大', '北', '极', '虾', '烧', '麦'],
                ['弹', '软', '糯', '椰', '蓉', '紫', '薯', '糯', '米', '糍', '宝', '宝', '喜', '欢', '简', '单', '快',
                 '手', '小', '吃', '下', '午', '茶'], ['营', '养', '丰', '富', '豆', '腐', '鲫', '鱼', '汤'],
                ['营', '养', '丰', '富', '豆', '腐', '鲫', '鱼', '汤'],
                ['一', '清', '二', '白', '小', '白', '菜', '豆', '腐', '汤'],
                ['一', '清', '二', '白', '小', '白', '菜', '豆', '腐', '汤'], ['小', '白', '菜', '肉', '丸', '汤'],
                ['小', '白', '必', '学', '快', '手', '菜', '蒜', '蓉', '油', '麦', '菜'],
                ['小', '白', '菜', '肉', '丸', '汤'], ['香', '蕉', '牛', '奶'], ['香', '煎', '鳕', '鱼'],
                ['清', '炒', '虾', '仁'], ['赛', '螃', '蟹'], ['水', '嫩', '蒸', '蛋'], ['丝', '瓜', '鸡', '蛋', '汤'],
                ['丝', '瓜', '鸡', '蛋', '汤'], ['西', '兰', '花', '炒', '口', '蘑'],
                ['排', '骨', '莲', '藕', '养', '生', '汤'], ['排', '骨', '莲', '藕', '养', '生', '汤'],
                ['家', '庭', '简', '易', '鸭', '血', '粉', '丝', '汤'],
                ['家', '庭', '简', '易', '鸭', '血', '粉', '丝', '汤'], ['家', '常', '疙', '瘩', '汤'],
                ['家', '常', '疙', '瘩', '汤'], ['鸡', '蛋', '羹', '超', '详', '细'], ['黑', '芝', '麻', '糊', '粉'],
                ['韩', '式', '海', '带', '汤'], ['韩', '式', '海', '带', '汤'],
                ['教', '你', '熬', '浓', '稠', '南', '瓜', '小', '米', '粥'],
                ['家', '庭', '小', '炒', '菜', '番', '茄', '炒', '蛋'], ['鲫', '鱼', '豆', '腐', '汤'],
                ['奶', '香', '馒', '头'], ['山', '药', '排', '骨', '汤'], ['南', '瓜', '发', '糕'],
                ['红', '枣', '补', '血', '养', '颜', '粥'], ['菠', '菜', '猪', '肝', '汤'],
                ['低', '脂', '美', '味', '丝', '瓜', '菌', '菇', '鸡', '蛋', '汤'],
                ['低', '脂', '美', '味', '丝', '瓜', '菌', '菇', '鸡', '蛋', '汤'],
                ['冬', '日', '养', '生', '暖', '胃', '粥', '之', '蔬', '菜', '海', '鲜', '粥'],
                ['番', '茄', '肥', '牛', '汤'], ['番', '茄', '肥', '牛', '汤'],
                ['自', '制', '冬', '日', '热', '饮', '水', '果', '茶', '酸', '甜', '好', '喝', '又', '解', '渴', '暖',
                 '胃', '又', '健', '康'],
                ['黄', '豆', '猪', '蹄', '汤', '滋', '补', '可', '以', '如', '此', '简', '单'],
                ['黄', '豆', '猪', '蹄', '汤', '滋', '补', '可', '以', '如', '此', '简', '单'],
                ['鲜', '香', '浓', '郁', '香', '菇', '炖', '鸡', '汤'],
                ['鲜', '香', '浓', '郁', '香', '菇', '炖', '鸡', '汤'], ['蒜', '蓉', '油', '麦', '菜'],
                ['零', '失', '败', '南', '瓜', '发', '糕', '做', '法'],
                ['懒', '人', '减', '肥', '熬', '夜', '必', '备', '紫', '薯', '银', '耳', '汤', '美', '容', '养', '颜',
                 '瘦', '身', '佳', '品'],
                ['素', '素', '鲜', '鲜', '汤', '减', '脂', '防', '癌', '抗', '癌', '营', '养', '汤', '蜜', '桃', '爱',
                 '营', '养', '师', '私', '厨'],
                ['素', '素', '鲜', '鲜', '汤', '减', '脂', '防', '癌', '抗', '癌', '营', '养', '汤', '蜜', '桃', '爱',
                 '营', '养', '师', '私', '厨'], ['菠', '菜', '鱼', '丸', '汤'],
                ['地', '道', '闽', '南', '味', '花', '生', '汤'], ['低', '脂', '健', '康', '鸡', '肉', '丸', '汤'],
                ['冬', '瓜', '海', '带', '汤'], ['冬', '瓜', '丸', '子', '汤'], ['冬', '阴', '功', '海', '鲜', '汤'],
                ['冬', '瓜', '薏', '米', '排', '骨', '汤'], ['番', '茄', '鸡', '胸', '肉', '丸', '子', '汤'],
                ['番', '茄', '金', '针', '菇', '汤'], ['番', '茄', '牛', '尾', '汤'], ['芙', '蓉', '鲜', '蔬', '汤'],
                ['芙', '蓉', '鲜', '蔬', '汤'], ['枸', '杞', '叶', '猪', '肝', '汤'], ['蛤', '蜊', '丝', '瓜', '汤'],
                ['黄', '豆', '苦', '瓜', '汤', '清', '热', '去', '火'],
                ['黄', '豆', '苦', '瓜', '汤', '清', '热', '去', '火'],
                ['家', '庭', '版', '奶', '油', '蘑', '菇', '汤'], ['菌', '菇', '鸽', '子', '汤'],
                ['菌', '菇', '肉', '片', '白', '菜', '汤'], ['开', '胃', '酸', '萝', '卜', '老', '鸭', '汤'],
                ['萝', '卜', '羊', '排', '汤'], ['南', '瓜', '土', '豆', '汤'],
                ['暖', '胃', '祛', '寒', '猪', '肚', '包', '鸡'], ['暖', '胃', '祛', '寒', '猪', '肚', '包', '鸡'],
                ['暖', '胃', '祛', '寒', '猪', '肚', '包', '鸡'], ['清', '甜', '椰', '子', '鸡'],
                ['秋', '季', '营', '养', '滋', '补', '海', '参', '汤'], ['肉', '丸', '丝', '瓜', '汤'],
                ['山', '药', '枸', '杞', '鸡', '汤'], ['山', '药', '枸', '杞', '鸡', '汤'],
                ['丝', '瓜', '豆', '腐', '蛋', '汤'], ['泰', '式', '冬', '阴', '功', '汤'],
                ['外', '婆', '味', '道', '菜', '心', '芋', '头', '汤'], ['鲜', '虾', '蔬', '菜', '疙', '瘩', '汤'],
                ['椰', '子', '鸡', '汤'], ['椰', '子', '鸡', '汤'], ['椰', '子', '鸡', '汤'],
                ['猪', '蹄', '莲', '藕', '汤'], ['鱼', '头', '豆', '腐', '汤'], ['滋', '补', '鸡', '汤', '煲'],
                ['花', '开', '富', '贵', '之', '番', '茄', '菌', '菇', '虾', '滑', '汤'],
                ['花', '开', '富', '贵', '之', '番', '茄', '菌', '菇', '虾', '滑', '汤'],
                ['花', '开', '富', '贵', '之', '番', '茄', '菌', '菇', '虾', '滑', '汤'],
                ['筒', '骨', '海', '带', '汤'], ['滋', '补', '鸡', '汤', '煲'], ['猪', '蹄', '莲', '藕', '汤'],
                ['鸭', '血', '豆', '腐', '汤'], ['筒', '骨', '海', '带', '汤'],
                ['酸', '甜', '开', '胃', '番', '茄', '金', '针', '菇', '冬', '瓜', '汤'],
                ['酸', '甜', '开', '胃', '番', '茄', '金', '针', '菇', '冬', '瓜', '汤'],
                ['酸', '甜', '开', '胃', '番', '茄', '金', '针', '菇', '冬', '瓜', '汤'],
                ['奶', '油', '蘑', '菇', '汤'], ['奶', '油', '蘑', '菇', '汤'], ['萝', '卜', '羊', '排', '汤'],
                ['秋', '季', '营', '养', '滋', '补', '海', '参', '汤'],
                ['好', '喝', '到', '停', '不', '下', '来', '罗', '宋', '汤'],
                ['韩', '式', '五', '花', '肉', '辣', '白', '菜', '豆', '腐', '汤', '思', '密', '达', '看', '韩', '剧',
                 '必', '备', '宵', '夜'], ['冬', '阴', '功', '海', '鲜', '汤'], ['枸', '杞', '叶', '猪', '肝', '汤'],
                ['枸', '杞', '叶', '猪', '肝', '汤'], ['萝', '卜', '羊', '排', '汤'],
                ['丝', '瓜', '豆', '腐', '蛋', '汤'], ['丝', '瓜', '豆', '腐', '蛋', '汤'], ['肉', '丝', '炒', '面'],
                ['一', '蔬', '一', '饭', '皆', '告', '白', '葱', '油', '拌', '面'],
                ['最', '强', '宵', '夜', '香', '辣', '牛', '肉', '拌', '面'],
                ['爆', '好', '吃', '韩', '式', '冷', '面'], ['北', '京', '炸', '酱', '面'],
                ['冬', '天', '天', '冷', '来', '碗', '暖', '身', '开', '胃', '酸', '汤', '面'],
                ['番', '茄', '鸡', '蛋', '拌', '面'], ['海', '鲜', '炒', '乌', '冬', '面'],
                ['好', '吃', '到', '舔', '碗', '香', '菇', '卤', '肉', '面'],
                ['好', '吃', '简', '单', '油', '泼', '面'],
                ['饸', '饹', '面', '做', '法', '图', '解', '红', '薯', '面', '饸', '饹'],
                ['红', '烧', '牛', '肉', '面'], ['胡', '胡', '胡', '胡', '油', '辣', '面'],
                ['火', '腿', '肠', '炒', '面'], ['凉', '拌', '面'], ['凉', '拌', '鸡', '丝'],
                ['来', '吃', '这', '碗', '销', '魂', '葱', '油', '拌', '面'],
                ['咖', '喱', '鲜', '虾', '乌', '冬', '面'], ['家', '常', '蛋', '炒', '面'], ['家', '常', '拌', '面'],
                ['酸', '辣', '荞', '麦', '面', '夏', '日', '减', '肥', '必', '备'],
                ['酸', '辣', '荞', '麦', '面', '夏', '日', '减', '肥', '必', '备'], ['茄', '子', '打', '卤', '面'],
                ['培', '根', '豆', '芽', '炒', '面'],
                ['牛', '油', '果', '意', '面', '佐', '伊', '比', '利', '亚', '火', '腿', '片'],
                ['牛', '肉', '丸', '热', '汤', '面'], ['牛', '肉', '面'], ['牛', '肉', '肠', '意', '大', '利', '面'],
                ['奶', '油', '蛤', '蜊', '意', '面'], ['蘑', '菇', '培', '根', '意', '面'],
                ['肉', '酱', '面', '附', '肉', '酱', '详', '细', '做', '法'], ['陕', '西', '人', '酸', '汤', '面'],
                ['陕', '西', '油', '泼', '面'], ['什', '锦', '炒', '面'],
                ['蔬', '菜', '火', '腿', '炒', '刀', '削', '面'], ['鲜', '虾', '鸡', '蛋', '卷', '面'],
                ['芸', '豆', '排', '骨', '焖', '面'], ['香', '菇', '肉', '丁', '炸', '酱', '面'],
                ['油', '泼', '扯', '面'], ['一', '碗', '榨', '菜', '面'],
                ['一', '人', '食', '手', '擀', '裤', '带', '面'], ['早', '餐', '吃', '碗', '面'],
                ['芝', '麻', '酱', '鸡', '丝', '凉', '面'],
                ['分', '钟', '烹', '制', '法', '国', '名', '菜', '白', '酒', '淡', '菜', '贻', '贝', '做', '法'],
                ['法', '国', '庄', '园', '风', '味', '红', '酒', '炖', '牛', '肉', '配', '土', '豆', '泥'],
                ['不', '用', '枫', '糖', '浆', '法', '国', '吐', '司'],
                ['低', '油', '低', '脂', '亚', '麻', '籽', '法', '国', '球'],
                ['低', '糖', '低', '脂', '法', '国', '球'],
                ['减', '脂', '少', '糖', '少', '油', '蒜', '香', '奶', '酪', '法', '国', '球', '外', '酥', '内', '软'],
                ['创', '意', '面', '包', '酸', '奶', '种', '布', '里', '欧', '修', '经', '典', '法', '国', '阶', '级',
                 '面', '包', '不', '阶', '级', '但', '更', '健', '康'],
                ['加', '入', '法', '国', '老', '面', '佛', '卡', '夏'],
                ['南', '瓜', '核', '桃', '欧', '包', '无', '油', '无', '糖', '附', '法', '国', '老', '面'],
                ['听', '说', '法', '国', '超', '级', '流', '行', '一', '款', '名', '古', '屋', '面', '包'],
                ['唐', '果', '料', '理', '法', '国', '红', '酒', '炖', '牛', '肉', '简', '易', '版'],
                ['外', '酥', '内', '软', '法', '国', '下', '午', '茶', '甜', '点', '青', '苹', '果', '布', '里', '欧',
                 '修'],
                ['大', '家', '来', '找', '茬', '风', '靡', '法', '国', '苹', '果', '隐', '形', '蛋', '糕', '内', '带',
                 '蓝', '莓'], ['好', '吃', '不', '胖', '黄', '金', '法', '国', '球', '三', '明', '治'],
                ['完', '美', '复', '刻', '法', '国', '烘', '焙', '大', '师', '红', '茶', '玛', '德', '琳'],
                ['带', '着', '法', '国', '人', '独', '有', '浪', '漫', '气', '息', '甜', '品', '可', '可', '费', '南',
                 '雪'], ['教', '你', '做', '法', '国', '皇', '后', '最', '爱', '咕', '咕', '洛', '夫', '面', '包'],
                ['新', '春', '报', '喜', '狗', '年', '大', '吉', '法', '国', '斗', '牛', '犬', '馒', '头'],
                ['最', '正', '宗', '法', '国', '可', '丽', '饼'],
                ['极', '具', '法', '国', '风', '味', '柠', '檬', '玛', '德', '琳', '蛋', '糕'],
                ['樱', '桃', '法', '国', '吐', '司', '早', '餐'],
                ['油', '封', '料', '理', '法', '国', '人', '吃', '鸡', '胗', '料', '理', '法'],
                ['法', '国', '乡', '村', '面', '包'],
                ['法', '国', '人', '最', '爱', '甜', '品', '焦', '糖', '布', '丁'], ['法', '国', '可', '丽', '饼'],
                ['法', '国', '吐', '司'], ['法', '国', '土', '司'], ['法', '国', '培', '根', '面', '包'],
                ['法', '国', '巧', '克', '力', '慕', '斯'], ['法', '国', '洋', '葱', '汤'],
                ['法', '国', '牛', '奶', '面', '包'], ['法', '国', '球', '面', '包'],
                ['法', '国', '甜', '品', '棉', '花', '糖', '圣', '诞', '玛', '德', '琳', '蛋', '糕'],
                ['法', '国', '百', '合', '洋', '蓟'], ['法', '国', '红', '丝', '绒', '玛', '德', '琳'],
                ['法', '国', '经', '典', '海', '鲜', '派', '咸', '味', '派'],
                ['法', '国', '美', '食', '法', '式', '洋', '葱', '汤'],
                ['法', '国', '老', '面', '烫', '种', '牛', '奶', '吐', '司'], ['法', '国', '老', '面', '制', '作'],
                ['法', '国', '舒', '芙', '蕾'], ['法', '国', '著', '名', '小', '茶', '点', '费', '南', '雪'],
                ['法', '国', '蓝', '带', '糕', '点', '制', '作', '糕', '点', '奶', '油', '馅'],
                ['法', '国', '蓝', '带', '糕', '点', '制', '作', '香', '蕉', '拿', '破', '仑', '酥'],
                ['法', '国', '蓝', '龙', '四', '吃'], ['法', '国', '银', '鳕', '鱼'],
                ['法', '国', '银', '鳕', '鱼', '煎', '蒸'],
                ['法', '国', '面', '包', '大', '师', '独', '家', '配', '方', '教', '你', '做', '正', '宗', '羊', '角',
                 '面', '包'], ['法', '国', '风', '情', '芝', '士', '焗', '扇', '贝'], ['法', '国', '黄', '油', '球'],
                ['法', '国', '黑', '麦', '面', '包'],
                ['法', '式', '咸', '可', '丽', '饼', '来', '自', '法', '国', '布', '列', '塔', '尼', '特', '色', '煎',
                 '饼', '果', '子', '荞', '麦', '可', '丽', '饼'],
                ['法', '式', '煎', '鸭', '胸', '配', '苹', '果', '薯', '条', '法', '国', '西', '南', '菜'],
                ['浓', '巧', '稥', '橘', '法', '国', '欧', '包'],
                ['火', '爆', '法', '国', '多', '年', '蒙', '布', '朗', '蛋', '糕'],
                ['热', '狗', '面', '包', '日', '式', '烫', '种', '法', '国', '老', '面', '种'],
                ['玛', '德', '琳', '蛋', '糕', '香', '浓', '奶', '油', '夹', '心', '法', '国', '下', '午', '茶', '点',
                 '心'],
                ['用', '法', '国', '师', '傅', '手', '法', '来', '做', '德', '式', '面', '包', '黑', '麦', '核', '桃',
                 '无', '花', '果'], ['石', '榴', '贝', '果', '法', '国', '老', '面'],
                ['经', '典', '法', '国', '阶', '级', '面', '包', '布', '里', '欧', '修'],
                ['营', '养', '美', '味', '香', '煎', '法', '国', '银', '鳕', '鱼'],
                ['蒜', '香', '奶', '酪', '吐', '司', '法', '国', '老', '面'],
                ['蓝', '莓', '夹', '心', '法', '国', '吐', '司'],
                ['蓝', '莓', '法', '国', '吐', '司', '花', '样', '做', '法'],
                ['记', '忆', '玛', '德', '琳', '昙', '花', '一', '现', '法', '国', '美', '味'],
                ['谷', '粒', '多', '法', '国'],
                ['超', '级', '简', '单', '快', '手', '早', '餐', '法', '国', '球', '夹', '心', '三', '明', '治'],
                ['软', '式', '法', '国', '面', '包', '低', '糖'],
                ['风', '靡', '法', '国', '糖', '渍', '苹', '果', '蛋', '糕'],
                ['香', '橙', '法', '国', '吐', '司', '早', '餐'], ['香', '烤', '法', '国', '吐', '司'],
                ['香', '煎', '法', '国', '鹅', '肝'],
                ['香', '草', '水', '果', '森', '林', '千', '层', '饼', '法', '国', '甜', '点', '大', '师', '作', '品'],
                ['香', '草', '番', '茄', '芝', '士', '冷', '盘', '误', '入', '法', '国', '小', '镇', '遇', '到', '美',
                 '食'], ['黑', '爵', '乳', '酪', '巧', '克', '力', '法', '国'], ['黑', '芝', '麻', '法', '国', '包'],
                ['黑', '芝', '麻', '法', '国', '球', '免', '揉', '面', '版'], ['意', '大', '利', '米', '饭'],
                ['餐', '铃', '铛', '料', '理', '秀', '墨', '西', '哥', '风', '味', '双', '料', '牛', '肉', '芝', '士',
                 '焗', '意', '大', '利', '面'], ['中', '式', '意', '大', '利', '通', '心', '粉'],
                ['亲', '测', '好', '吃', '减', '肥', '餐', '奶', '油', '虾', '仁', '火', '腿', '意', '大', '利', '面'],
                ['亲', '测', '好', '吃', '减', '肥', '餐', '薯', '泥', '培', '根', '意', '大', '利', '面'],
                ['健', '身', '餐'], ['健', '身', '餐', '减', '肥', '餐'], ['儿', '童', '餐'],
                ['儿', '童', '餐', '之', '牛', '油', '果', '意', '大', '利', '面'], ['娃', '娃', '餐'],
                ['宝', '宝', '餐'], ['家', '常', '意', '大', '利', '比', '萨'], ['意', '大', '利', '佛', '卡', '夏'],
                ['意', '大', '利', '冰', '淇', '淋'], ['意', '大', '利', '奶', '冻'],
                ['意', '大', '利', '奶', '酪', '菌', '菇', '饭'], ['意', '大', '利', '披', '萨'],
                ['意', '大', '利', '炒', '面'], ['意', '大', '利', '烩', '饭'], ['意', '大', '利', '甜', '椒', '樽'],
                ['意', '大', '利', '番', '茄', '汤'], ['意', '大', '利', '肉', '丸', '面'],
                ['意', '大', '利', '肉', '圆'],
                ['意', '大', '利', '肉', '酱', '面', '儿', '童', '简', '餐', '系', '列'],
                ['意', '大', '利', '通', '心', '粉'], ['意', '大', '利', '通', '心', '面'], ['意', '大', '利', '面'],
                ['意', '大', '利', '面', '儿', '童', '餐'], ['懒', '人', '餐'], ['月', '子', '餐'], ['水', '果', '餐'],
                ['海', '鲜', '餐'], ['炒', '意', '大', '利'], ['爱', '心', '餐'], ['生', '日', '餐'],
                ['留', '学', '生', '每', '一', '餐', '奶', '油', '意', '大', '利', '面'],
                ['自', '制', '意', '大', '利', '肉', '酱', '意', '大', '利', '面'],
                ['高', '考', '爱', '心', '餐', '金', '榜', '题', '名', '餐', '营', '养', '餐', '科', '学', '煎', '蛋',
                 '番', '茄'], ['日', '本', '料', '理', '日', '式', '便', '当', '里', '小', '动', '物'],
                ['中', '华', '端', '午', '料', '理'], ['基', '础', '料', '理', '油', '葱', '酥'],
                ['德', '风', '料', '理'], ['懒', '人', '料', '理', '卤', '味'], ['料', '理', '锅', '披', '萨'],
                ['日', '本', '丸', '子'],
                ['日', '本', '人', '气', '料', '理', '天', '津', '饭', '低', '脂', '低', '卡', '鲜', '美', '无', '比'],
                ['日', '本', '厚', '蛋', '烧'], ['日', '本', '咖', '喱'],
                ['日', '本', '家', '庭', '料', '理', '筑', '前', '煮'],
                ['日', '本', '家', '庭', '料', '理', '之', '炖', '豆', '渣', '卯', '花'], ['日', '本', '寿', '司'],
                ['日', '本', '御', '节', '料', '理', '筑', '前', '煮'], ['日', '本', '抹', '茶', '道'],
                ['日', '本', '料', '理', '关', '东', '煮'],
                ['日', '本', '料', '理', '厚', '蛋', '烧', '厚', '焼', '玉', '子'],
                ['日', '本', '料', '理', '味', '增', '汤', '味', '噌', '汁'],
                ['日', '本', '料', '理', '大', '阪', '烧', '好', '焼'],
                ['日', '本', '料', '理', '稲', '荷', '寿', '司'], ['日', '本', '料', '理', '豚', '汁'],
                ['日', '本', '料', '理', '金', '平'], ['日', '本', '料', '理', '大', '福', '草', '莓'],
                ['日', '本', '梅', '酒'], ['日', '本', '樱', '花', '酒'], ['日', '本', '炸', '虾'],
                ['日', '本', '炸', '豆', '腐'], ['日', '本', '粘', '面'], ['日', '本', '蕨', '饼'],
                ['照', '烧', '龙', '利', '鱼', '日', '本', '料', '理', '蜜', '桃', '爱', '营', '养', '师', '私', '厨',
                 '健', '康', '鱼', '料', '理'],
                ['酸', '酸', '哒', '可', '开', '胃', '算', '日', '本', '料', '理', '拿', '波', '里', '意', '面'],
                ['风', '靡', '日', '本', '玉', '子', '烧'], ['黑', '暗', '料', '理'],
                ['素', '韩', '国', '炸', '酱', '面'], ['韩', '国', '料', '理', '辣', '炒', '年', '糕'],
                ['韩', '式', '风', '情', '辣', '炒', '年', '糕', '分', '钟', '正', '宗', '韩', '国', '味'],
                ['一', '款', '从', '韩', '国', '红', '到', '全', '世', '界', '蒜', '香', '奶', '酪', '包'],
                ['不', '再', '为', '剩', '饭', '发', '愁', '韩', '国', '泡', '菜', '炒', '饭'],
                ['丰', '富', '维', '生', '素', '橘', '子', '柠', '檬', '果', '酱', '韩', '国', '妈', '妈', '巧', '心',
                 '之', '作'], ['刷', '脂', '韩', '国', '泡', '菜', '汤', '辣', '酱', '汤'],
                ['口', '感', '非', '常', '惊', '艳', '韩', '国', '料', '理', '韩', '式', '西', '葫', '芦', '煎', '饼'],
                ['四', '分', '钟', '必', '备', '快', '手', '餐', '韩', '国', '金', '氏', '辣', '炒', '年', '糕'],
                ['工', '作', '日', '晚', '餐', '韩', '国', '烤', '牛', '肉'],
                ['感', '觉', '难', '但', '很', '简', '单', '小', '白', '料', '理', '韩', '国', '春', '川', '鸡'],
                ['既', '好', '做', '又', '颜', '值', '高', '韩', '国', '部', '队', '火', '锅'],
                ['暖', '心', '暖', '身', '韩', '国', '泡', '菜', '辣', '炒', '年', '糕', '蜜', '桃', '爱', '营', '养',
                 '师', '私', '厨', '益', '生', '菌', '肠', '道', '健', '康'],
                ['正', '宗', '韩', '国', '炸', '酱', '面'],
                ['火', '爆', '韩', '国', '街', '头', '韩', '式', '烤', '鸡', '腿'],
                ['煎', '西', '葫', '芦', '韩', '国', '思', '密', '达'],
                ['用', '电', '饼', '铛', '吃', '韩', '国', '烤', '盘'],
                ['百', '吃', '不', '厌', '韩', '国', '芝', '士', '拉', '面', '部', '队', '火', '锅', '来', '啦'],
                ['紫', '菜', '包', '饭', '跟', '韩', '国', '主', '妇', '学'],
                ['红', '茶', '吐', '司', '法', '国', '老', '面'], ['自', '制', '韩', '国', '拌', '饭'],
                ['色', '香', '味', '营', '养', '俱', '全', '韩', '国', '拌', '饭'],
                ['菜', '鸟', '级', '韩', '国', '泡', '菜'],
                ['超', '简', '单', '减', '脂', '韩', '式', '辣', '酱', '炒', '鸡', '蛋', '韩', '国', '下', '饭', '菜'],
                ['超', '级', '好', '吃', '自', '制', '韩', '国', '辣', '白', '菜'],
                ['跟', '白', '钟', '元', '学', '韩', '国', '泡', '菜', '汤'], ['速', '成', '韩', '国', '泡', '菜'],
                ['韩', '国', '人', '气', '美', '食', '丨', '红', '豆', '抹', '茶', '司', '康', '三', '分', '钟', '搞',
                 '定'], ['韩', '国', '人', '气', '芝', '士', '火', '鸡', '面'],
                ['韩', '国', '参', '鸡', '汤', '迷', '迭', '香'], ['韩', '国', '大', '酱', '汤'],
                ['韩', '国', '拌', '饭', '那', '些', '年', '我', '们', '一', '起', '追', '韩', '餐'],
                ['韩', '国', '料', '理', '煎', '五', '花', '肉', '就', '这', '么', '简', '单'],
                ['韩', '国', '泡', '菜', '白', '萝', '卜', '正', '宗', '版'], ['韩', '国', '泡', '菜'],
                ['韩', '国', '泡', '菜', '泡', '萝', '卜'],
                ['韩', '国', '泡', '菜', '五', '花', '肉', '蜜', '桃', '爱', '营', '养', '师', '私', '厨'],
                ['韩', '国', '泡', '菜', '大', '赛', '第', '一', '名', '辣', '白', '菜', '配', '方'],
                ['韩', '国', '泡', '菜', '汤', '素'], ['韩', '国', '泡', '菜', '炒', '饭'],
                ['韩', '国', '泡', '菜', '辣', '白', '菜'],
                ['韩', '国', '济', '州', '岛', '零', '食', '橘', '子', '巧', '克', '力'],
                ['韩', '国', '海', '带', '汤'], ['韩', '国', '火', '辣', '鸡', '爪'], ['韩', '国', '炸', '鸡'],
                ['韩', '国', '甜', '辣', '酱', '炸', '酱', '面'], ['韩', '国', '白', '雪', '蒸', '糕'],
                ['韩', '国', '百', '姓', '日', '常', '餐', '桌', '必', '不', '可', '少', '大', '酱', '汤'],
                ['韩', '国', '石', '榴', '蛋', '糕'], ['韩', '国', '石', '锅', '拌', '饭'],
                ['韩', '国', '素', '食', '紫', '菜', '包', '饭'],
                ['韩', '国', '网', '红', '厚', '蛋', '三', '明', '治'],
                ['韩', '国', '芝', '士', '铁', '板', '辣', '炒', '鸡'], ['韩', '国', '芝', '士', '饭'],
                ['韩', '国', '街', '头', '同', '款', '辣', '炒', '年', '糕'],
                ['韩', '国', '豆', '腐', '汤', '把', '人', '气', '美', '食', '搬', '回', '家'],
                ['韩', '国', '超', '火', '鸡', '蛋', '小', '面', '包', '蒸', '烤', '箱', '版'],
                ['韩', '国', '超', '火', '网', '红', '缤', '纷', '香', '蕉', '奶', '昔'],
                ['韩', '国', '辛', '拉', '面', '泡', '面', '升', '级', '版'],
                ['韩', '国', '辣', '白', '菜', '改', '良', '川', '味', '版'], ['韩', '国', '辣', '鸡', '爪'],
                ['韩', '国', '部', '队', '火', '锅'], ['韩', '国', '香', '辣', '猪', '蹄'],
                ['韩', '国', '鸡', '蛋', '培', '根', '沙', '拉', '早', '餐', '包', '三', '明', '治'],
                ['韩', '国', '鸡', '蛋', '糕'],
                ['那', '年', '花', '开', '月', '正', '圆', '最', '让', '少', '奶', '奶', '喜', '爱', '陕', '西', '小',
                 '吃', '甑', '糕'], ['小', '吃', '陕', '西', '西', '安', '油', '炸', '馍', '馍'],
                ['小', '吃', '陕', '西', '甑', '糕', '甘', '肃', '糕', '卷'],
                ['烙', '面', '皮', '夏', '天', '最', '凉', '快', '地', '饭', '它', '也', '好', '吃', '陕', '西', '有',
                 '名', '小', '吃', '味', '很', '独', '特'], ['特', '色', '小', '吃', '陕', '西', '凉', '皮'],
                ['特', '色', '小', '吃', '陕', '西', '凉', '皮'],
                ['电', '饭', '锅', '版', '陕', '西', '小', '吃', '甄', '糕'],
                ['看', '热', '剧', '那', '年', '花', '开', '学', '做', '陕', '西', '名', '小', '吃', '甑', '糕'],
                ['肉', '夹', '馍', '陕', '西', '特', '色', '小', '吃'],
                ['让', '活', '一', '道', '经', '典', '陕', '西', '特', '色', '小', '吃'],
                ['陕', '西', '关', '中', '小', '吃', '麻', '食'],
                ['陕', '西', '关', '中', '小', '吃', '酥', '脆', '喷', '香', '涮', '锅', '油', '饼'],
                ['陕', '西', '关', '中', '小', '吃', '麦', '饭'],
                ['陕', '西', '名', '小', '吃', '腊', '汁', '肉', '夹', '馍'], ['陕', '西', '哨', '子', '面'],
                ['陕', '西', '小', '吃', '金', '线', '油', '塔'], ['陕', '西', '小', '吃', '旋', '面'],
                ['陕', '西', '小', '吃', '孜', '然', '肉', '夹', '馍'],
                ['陕', '西', '小', '吃', '韭', '菜', '滋', '卷'], ['陕', '西', '小', '吃', '凉', '皮'],
                ['陕', '西', '小', '吃', '千', '层', '油', '馍'], ['陕', '西', '小', '吃', '棒', '棒', '馍'],
                ['陕', '西', '小', '吃', '甑', '糕'], ['陕', '西', '小', '吃', '甑', '甑', '糕'],
                ['陕', '西', '小', '吃', '石', '子', '馍'],
                ['陕', '西', '小', '吃', '蜂', '蜜', '红', '豆', '糯', '米', '凉', '糕'],
                ['陕', '西', '小', '吃', '胡', '辣', '汤', '素', '版'], ['陕', '西', '小', '吃', '甑', '糕'],
                ['陕', '西', '岐', '山', '臊', '子'], ['陕', '西', '油', '糕'], ['陕', '西', '烩', '麻', '食'],
                ['陕', '西', '特', '色', '小', '吃', '豆', '面', '糊'],
                ['陕', '西', '特', '色', '小', '吃', '棒', '棒', '馍'],
                ['陕', '西', '特', '色', '小', '吃', '麻', '什'],
                ['陕', '西', '特', '色', '小', '吃', '槐', '花', '麦', '饭'], ['陕', '西', '甑', '糕'],
                ['陕', '西', '白', '吉', '馍'], ['陕', '西', '肉', '夹', '馍'], ['陕', '西', '腊', '汁', '肉'],
                ['陕', '西', '臊', '子'], ['陕', '西', '臊', '子'], ['陕', '西', '锅', '盔'], ['陕', '西', '鱼', '鱼'],
                ['陕', '西', '麦', '饭'], ['陕', '西', '麻', '食']]
    search_data = request.GET.get('q', "")
    hh = models.mypicture.objects.filter(user=111111113)
    aa = []
    for x in search_data:
        if x != '吃' and x != '菜' and x != '我' and x != '一' and x != '下' and x != '不' and x != '好':
            aa.append(x)
    if search_data:
        e = 0
        pp = 0
        for i in all_docs:

            similarity = cosine_similarity(i, aa, all_docs)
            pp += 1
            if similarity > 0.2:
                e += 1
                print(similarity)
                try:
                    food_1 = models.mypicture.objects.filter(main_id=pp).values('user').first()
                    food_2 = models.mypicture.objects.filter(user=food_1['user']).values('id').first()
                    food_3 = models.mypicture.objects.filter(id=food_2['id'])
                    hh = food_3 | hh
                except:
                    pass
            if e > 17:
                break
    return render(request, 'TF-IDF算法.html', {'foods': hh})


def 浏览推荐(request):
    info = request.session.get('info')
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    username = info['username']
    aa = models.browse.objects.filter(user_name=username).values('main_id').order_by('-id')[0]
    cc = models.mypicture.objects.filter(id=aa['main_id']).values('class2')[0]
    foods = models.mypicture.objects.filter(class2=cc['class2']).order_by('?')[0:9]
    return render(request, '浏览行为推荐算法.html', {'foods': foods})

def 个人喜好(request):
    info = request.session.get('info')
    if not info:
        message = "请登录"
        return render(request, '主页面.html', {'message': message})
    username = info['username']
    hobby1 = info['hobby1']
    foods = models.mypicture.objects.filter(class1=hobby1).order_by('?')[0:9]
    return render(request, '浏览行为推荐算法.html', {'foods': foods})