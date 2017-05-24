import asyncio
import aiohttp
import aiomysql
import re
import os
import collections
import random
import time
import datetime
import json
import collections
import hashlib
import base64
from aiohttp import web
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging


PATH='/home/ubuntu/platform/photo/'
port=8800

@asyncio.coroutine
def create_pool():
    global pool
    pool = yield from aiomysql.create_pool(host='localhost', port=3306,
                                           user='root', password='???',
                                           db='???', loop=loop,
                                           charset='utf8')

@asyncio.coroutine
def photo_bed(request):

    if request.content_type!="multipart/form-data":
        # print(request.content_type)
        return web.HTTPBadRequest(reason="error content type")

    try:
        reader = yield from request.multipart()
    except BaseException as e:
        # print(e)
        return web.HTTPBadRequest()

    get = yield from reader.next()
    # print(get.__dict__)

    session = yield from get_session(request)
    if 'room' not in session:

        global pool
        with (yield from pool) as conn:
            cur = yield from conn.cursor()

            while True:
                room = str(random.randint(000000,999999)).zfill(6)
                try:
                    yield from cur.execute('INSERT INTO article VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(room,datetime.datetime.now().strftime("%Y/%m/%d %H:%M"),"","","","","","",0,0))
                except BaseException as e:
                    if re.search(r"key 'PRIMARY'",e.args[1])!=None:
                        continue
                else:
                    break
            
            yield from conn.commit()
            yield from cur.close()
            conn.close()

        if os.path.exists(PATH+room)==0:
            os.mkdir(PATH+room)
        session["room"] = room

    else:
        room = session['room']

        if os.path.exists(PATH+room)==0:
            os.mkdir(PATH+room)

    filepath=''
    size = 0
    suffix = ''
    hashcal = hashlib.md5()   
    
    while True:
        try:
            chunk = yield from get.read_chunk()  # 8192 bytes by default
        except AttributeError:
            return web.HTTPBadRequest()

        if not chunk:
            break

        if size == 0 : 

            if len(chunk)<4:
                return web.HTTPBadRequest(reason="unsupported file type")
 
            # top8=chunk[0:4].hex().upper()
            top8=''.join('{:02x}'.format(x) for x in chunk[0:4]).upper()

            if top8[0:6] == 'FFD8FF':
                suffix = ".jpg"
            elif top8[0:8] == '89504E47':
                suffix = ".png"
            elif top8[0:8] == '47494638':
                suffix = ".gif"
            else:
                return web.HTTPUnsupportedMediaType(reason="unsupported file type")

            randnum = str(int(time.time()))
            filepath = PATH + room + '/' +randnum
            while(os.path.exists(filepath)):
                randnum = str(int(time.time()))
                filepath = PATH + room + '/' +randnum
            f = open(filepath,'wb')

        size = size + len(chunk)      
        f.write(chunk)
        hashcal.update(chunk)

        if size/1048576 > 3: # size limit 3MB
            f.close()
            os.remove(filepath)
            return web.HTTPRequestEntityTooLarge(reason="file size overflow")

    f.close()
    hashval = hashcal.hexdigest()
    newfilepath = PATH + room + '/' + hashval + suffix
    if os.path.exists(newfilepath)!=0:
        os.remove(filepath)
        return web.HTTPNotAcceptable(reason="file already exists")
    else:
        os.rename(filepath, newfilepath)
        return web.Response(text=hashval+suffix)

@asyncio.coroutine
def delete_photo(request):
    if request.content_type!="application/x-www-form-urlencoded":
        return web.HTTPBadRequest(reason="error content type")

    session = yield from get_session(request)
    if 'room' in session:
        room = session['room']
    else:
        return web.HTTPUnauthorized()

    data = yield from request.post()

    if len(data)==1 and 'filename' in data:
        filename = data['filename']
    else:
        return web.HTTPBadRequest()

    if re.search(r'^[\d|a-z]+\.(jpg|png|gif)$',filename)==None:
        return web.HTTPBadRequest()

    if os.path.exists(PATH + room + "/" + filename)==0 or filename=='':
        return web.HTTPInternalServerError(reason="file not found")
    else:
        os.remove(PATH + room + "/" + filename)

    return web.Response(text="Done")

@asyncio.coroutine
def article(request):

    if request.content_type!="application/x-www-form-urlencoded":
        return web.HTTPBadRequest(reason="error content type")

    data = yield from request.post()


    if 'title' in data:
        title = data['title'] 
    else:
        return web.HTTPBadRequest()
    
    if 'subtitle' in data:
        subtitle = data['subtitle']
    else:
        return web.HTTPBadRequest()
    
    if 'provider' in data:
        provider = data['provider']
    else:
        return web.HTTPBadRequest()

    if 'type' in data:
        category = data['type'].lower()
        if category not in {"blog":"","news":"","magazine":""}:
            return web.HTTPBadRequest()
    else:
        return web.HTTPBadRequest()

    if 'article' in data:
        article = data['article']
    else:
        return web.HTTPBadRequest()

    delivery = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    brief = re.sub(r'http://',"", article)
    brief = re.sub(r'https://',"", brief)
    brief = re.sub(r'\!\[[^\]]*\]\([^\)]+?\)',"",brief)
    brief = re.sub(r'\s+'," ",brief)
    brief = re.sub(r'^\s+',"",brief)
    brief = brief[0:80]
    brief = re.sub(r'\s$',"",brief)
    if len(brief) == 80:
        brief = brief+"..."

    imagelist = re.findall(r'([\d|a-f]{32}\.(jpg|png|gif))',article)

    article = re.sub(r'\r\n','\n',article)
    article = re.sub(r'\n','<br>',article)
    article = re.sub(r'\!\[[^\]]*\]\(([^\)]+?)\)','<img src="\g<1>">',article)

    global pool

    session = yield from get_session(request)
    if 'room' in session:
        room = session['room']

        used = []
        if len(imagelist)>0:
            for line in imagelist:
                used.append(line[0])

        existing = os.listdir(PATH + room)

        if len(existing)>len(used):
            noused = list(set(existing).difference(set(used)))
            for line in noused:
                os.remove(PATH + room + '/' + line)

        with (yield from pool) as conn:
            cur = yield from conn.cursor()
            yield from cur.execute('UPDATE article SET delivery = %s, type = %s, title = %s, subtitle = %s, provider = %s, summary = %s, full = %s, valid = %s WHERE id = %s;',(delivery,category,title,subtitle,provider,brief,article,1,room))
            yield from conn.commit()
            yield from cur.close()
            conn.close()

    else:

        with (yield from pool) as conn:
            cur = yield from conn.cursor()

            while True:
                room = str(random.randint(000000,999999)).zfill(6)
                try:
                    yield from cur.execute('INSERT INTO article VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(room,delivery,category,title,subtitle,provider,brief,article,1,0))
                except BaseException as e:
                    if e.find("key 'PRIMARY'")!=-1:
                        continue
                else:
                    break
            
            yield from conn.commit()
            yield from cur.close()
            conn.close()

        session['room'] = room


    # session.clear()
    return web.Response(text=room)

@asyncio.coroutine
def preview(request):

    room = request.match_info["room"]
    removeblock = ""
    session = yield from get_session(request)
    if 'room' in session:
        if session['room'] == room:
            removeblock='<div id="delete"  onclick="unsatisfied()"></div>'

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT delivery, title, subtitle, provider, full FROM article WHERE id = "%s" and valid = 1;'%(room))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound()

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    delivery = out[0][0].strftime("%Y/%m/%d %H:%M")
    title = out[0][1]
    subtitle = out[0][2]
    provider = out[0][3]
    full = out[0][4]

    html='''<meta charset="utf-8">
<!DOCTYPE html>
<html>
<head>
	<title>%s</title>
	<link rel="stylesheet" type="text/css" href="/preview.css"/>
	<script src="https://cdn.bootcss.com/zepto/1.0rc1/zepto.min.js"></script>
	<script type="text/javascript">
		function unsatisfied(){
			if(confirm("不太满意删了重发?"))
			{
				var id = window.location.href.slice(-6)
				$.ajax({
					url:"/delete/article/" + id,
					type:"post",
					data: false, 
					async: true,
					processData:false,
					contentType:false,
					success:function(data){	
						window.location.href="/"
					},
					error:function(e){
						if(e.status==403)
							alert("好像已经失去删除权限了。。。")
						else if(e.status==404)
							alert("怕是已经删除了呢。。")
						else
							alert("我也不知道发生了什么")
					}
				});
			}
		}
	</script>
</head>
<body>
<div id="whole">
%s
<div id="title">%s</div>
<div id="subtitle">%s</div>
<div id="provider">%s</div>
<div id="delivery">Archive: %s</div>
<div id="article">%s</div>
</div>
</body>
</html>
'''

    full=re.sub(r'([\d|a-f]{32}\.(jpg|png|gif))','/photo/'+room+'/\g<1>',full)

    html=html%(title+" | Platform · idol",removeblock,title,subtitle,provider,delivery,full)
    #session.clear()
    return web.Response(text=html,content_type='text/html',charset='utf-8')

@asyncio.coroutine
def delete_article(request):

    room = request.match_info["room"]

    session = yield from get_session(request)
    if 'room' not in session:
        return web.HTTPForbidden()
    elif room != session['room']:
        return web.HTTPForbidden()

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        result = yield from cur.execute("DELETE FROM article where id = %s;",(room))
        if result == 0:
            return web.HTTPNotFound()
        yield from conn.commit()
        yield from cur.close()
        conn.close()

    session.clear()
    return web.HTTPNoContent()


@asyncio.coroutine
def mbview(request):

    room = request.match_info["room"]

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT delivery, title, subtitle, provider, full FROM article WHERE id = "%s" and valid = 1;'%room)
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound()

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    delivery = out[0][0].strftime("%m/%d %H:%M")
    title = out[0][1]
    subtitle = out[0][2]
    provider = out[0][3]
    full = out[0][4]

    html='''<meta charset="utf-8">
<!DOCTYPE html>
<html>
<head>
	<title>乃木物</title>
	<link rel="stylesheet" type="text/css" href="/mbview.css"/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
</head>
<body>
<div id="block">
	<div id="title">%s</div>
	<div id="subtitle">%s</div>
</div>
<div id="post">
	<div id="provider"><a>%s</a></div>
	<div id="delivery"><a>%s</a></div>
</div>
<div id="article">%s</div>
</div>
</body>
</html>
'''

    full=re.sub(r'([\d|a-f]{32}\.(jpg|png|gif))','/photo/'+room+'/\g<1>',full)

    html=html%(title,subtitle,provider,delivery,full)

    return web.Response(text=html,content_type='text/html',charset='utf-8')




@asyncio.coroutine
def clean(request):
    session = yield from get_session(request)
    session.clear()
    return web.HTTPNoContent()

@asyncio.coroutine
def oneentry(request):
    room = request.match_info["room"]

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT id, delivery, type, title, subtitle, provider, full FROM article WHERE id = "%s" and valid = 1;'%room)
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound()

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    oneentry=collections.OrderedDict()
    oneentry['id']=out[0][0]
    oneentry['delivery']=int(time.mktime(out[0][1].timetuple()))
    oneentry['type']=out[0][2]
    oneentry['title']=out[0][3]
    oneentry['subtitle']=out[0][4]
    oneentry['provider']=out[0][5]

    article=re.sub(r'([\d|a-f]{32}\.(jpg|png|gif))','https://platform.idolx46.top/photo/'+room+'/\g<1>',out[0][6])

    oneentry['article']=article

    return web.Response(text=json.dumps(oneentry,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def entrylist(request):

    query_parameter=request.rel_url.query
    addition = ""
    limit = 10
    offset = 0

    if "type" in query_parameter:
        if query_parameter["type"] in {"blog":"","magazine":"","news":""}:
            addition = 'and type = "' + query_parameter["type"] + '"'
        else:
            return web.HTTPBadRequest(reason="no that type")

    if "size" in query_parameter:
        if re.search(r'^\d+$',query_parameter["size"]):
            limit = int(query_parameter["size"])
            if limit > 100:
                return web.HTTPBadRequest(reason="page size over limit")

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"]):
            if int(query_parameter["page"])==0:
                return web.HTTPBadRequest(reason="page start from 1")
            offset = (int(query_parameter["page"])-1)*limit

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT id, delivery, type, title, subtitle, provider, summary, full FROM article WHERE valid = 1 %s ORDER BY delivery DESC LIMIT %s OFFSET %s;'%(addition,str(limit),str(offset)))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(reason="empty page")

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    entrylist = []

    for line in out:
        oneentry=collections.OrderedDict()
        oneentry['id']=line[0]
        oneentry['delivery']=int(time.mktime(line[1].timetuple()))
        oneentry['type']=line[2]
        oneentry['title']=line[3]
        oneentry['subtitle']=line[4]
        oneentry['provider']=line[5]
        oneentry['summary']=line[6]
        oneentry['detail']="/data/" + line[0]
        oneentry['view']="/mbview/article/" + line[0]

        article=re.sub(r'([\d|a-f]{32}\.(jpg|png|gif))','https://platform.idolx46.top/photo/'+line[0]+'/\g<1>',line[7])
        imagelist_raw=re.findall(r'<img src="([^"]+)">',article)

        imagelist = list(set(imagelist_raw))
        imagelist.sort(key=imagelist_raw.index)

        if len(imagelist)>=3:
            outerlist=[]
            for n in range(0,3):
                innerdict={}
                innerdict['image']=imagelist[n]
                outerlist.append(innerdict)

            oneentry['withpic']=outerlist 
        elif len(imagelist)>=1:
            outerlist=[]
            innerdict={}
            innerdict["image"]=imagelist[0]
            outerlist.append(innerdict)

            oneentry['withpic']=outerlist
        else:
            oneentry['withpic']=None

        entrylist.append(oneentry)

    return web.Response(text=json.dumps(entrylist,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def version(request):
    os = request.match_info["os"]
    if os!="android":# and os!="ios":
        return web.HTTPBadRequest()
    
    #version = request.match_info["version"]
    #newest = "1.0"
    #version_check = version.split(".")
    #newest_check = newest.split(".")

    updateinfo = collections.OrderedDict()
    updateinfo["versionCode"] = 1
    updateinfo["versionName"] = "1.0"
    updateinfo["msg"] = "release 1.0"
    updateinfo["download"] = "https://platform.idolx46.top/resource/nogimono.apk"
    
    return web.Response(text=json.dumps(updateinfo,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def blogs(request):
    
    query_parameter=request.rel_url.query

    addition = ""
    limit = 10
    offset = 0

    if "member" in query_parameter:
        # if query_parameter["member"] in {"wakatsuki-yumi":"","saitou-chiharu":"","ikuta-erika":"","sakurai-reika":"","itou-marika":"","etou-misa":"","takayama-kazumi":"","saitou-yuuri":"","shiraishi-mai":"","nishino-nanase":"","matsumura-sayuri":"","kawago-hina":"","nakada-kana":"","hoshino-minami":"","saitou-asuka":"","higuchi-hina":"","nakamoto-himeka":"","kawamura-mahiro":"","wada-maaya":"","noujou-ami":"","ikoma-rina":"","inoue-sayuri":"","unei-sutaffu":"","akimoto-manatsu":"","kenkyuusei":"","hori-miona":"","kitano-hinako":"","shinuchi-mai":"","itou-karin":"","sagara-iori":"","itou-junna":"","watanabe-miria":"","suzuki-ayane":"","sasaki-kotoko":"","yamazaki-rena":"","terada-ranze":"","sankisei":""}:
        if query_parameter["member"] in {"akimoto-manatsu":"","ikuta-erika":"","ikoma-rina":"","itou-karin":"","itou-junna":"","itou-marika":"","itou-riria":"","inoue-sayuri":"","iwamoto-renka":"","umezawa-minami":"","unei-sutaffu":"","etou-misa":"","oozono-momoko":"","kawago-hina":"","kawamura-mahiro":"","kitano-hinako":"","kubo-shiori":"","kenkyuusei":"","saitou-asuka":"","saitou-chiharu":"","saitou-yuuri":"","sakaguchi-tamami":"","sagara-iori":"","sakurai-reika":"","sasaki-kotoko":"","satou-kaede":"","shiraishi-mai":"","shinuchi-mai":"","suzuki-ayane":"","takayama-kazumi":"","terada-ranze":"","nakada-kana":"","nakamura-reno":"","nakamoto-himeka":"","nishino-nanase":"","noujou-ami":"","higuchi-hina":"","hoshino-minami":"","hori-miona":"","matsumura-sayuri":"","mukai-hazuki":"","yamazaki-rena":"","yamashita-mizuki":"","yoshida-ayano-christie":"","yoda-yuuki":"","wakatsuki-yumi":"","wada-maaya":"","watanabe-miria":""}:
            addition = 'where rome = "' + query_parameter["member"] + '"'
        else:
            return web.HTTPBadRequest(reason="no such member")

    if "size" in query_parameter:
        if re.search(r'^\d+$',query_parameter["size"]):
            limit = int(query_parameter["size"])
            if limit > 100:
                return web.HTTPBadRequest(reason="page size over limit")

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"]):
            if int(query_parameter["page"])==0:
                return web.HTTPBadRequest(reason="page start from 1")
            offset = (int(query_parameter["page"])-1)*limit

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute("SELECT post, kana, author, title, summary, url FROM official_blogs %s ORDER BY post DESC, kana DESC LIMIT %s OFFSET %s"%(addition,str(limit),str(offset)))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(reason="empty page")

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()


    bloglist = []

    for line in out:
        oneblog=collections.OrderedDict()      
        oneblog['post']=int(time.mktime(line[0].timetuple()))
        oneblog['author']=line[2]
        oneblog['title']=line[3]
        oneblog['summary']=line[4]
        oneblog['url']=line[5]
        bloglist.append(oneblog)

    return web.Response(text=json.dumps(bloglist,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def memberdetail(request):

    query_parameter=request.rel_url.query

    if "member" in query_parameter:
        if query_parameter["member"] in {"akimoto-manatsu":"","ikuta-erika":"","ikoma-rina":"","itou-karin":"","itou-junna":"","itou-marika":"","itou-riria":"","inoue-sayuri":"","iwamoto-renka":"","umezawa-minami":"","etou-misa":"","oozono-momoko":"","kawago-hina":"","kawamura-mahiro":"","kitano-hinako":"","kubo-shiori":"","saitou-asuka":"","saitou-chiharu":"","saitou-yuuri":"","sakaguchi-tamami":"","sagara-iori":"","sakurai-reika":"","sasaki-kotoko":"","satou-kaede":"","shiraishi-mai":"","shinuchi-mai":"","suzuki-ayane":"","takayama-kazumi":"","terada-ranze":"","nakada-kana":"","nakamura-reno":"","nakamoto-himeka":"","nishino-nanase":"","noujou-ami":"","higuchi-hina":"","hoshino-minami":"","hori-miona":"","matsumura-sayuri":"","mukai-hazuki":"","yamazaki-rena":"","yamashita-mizuki":"","yoshida-ayano-christie":"","yoda-yuuki":"","wakatsuki-yumi":"","wada-maaya":"","watanabe-miria":""}:
            sql_member_detail = "SELECT name, kana, rome, birthdate, bloodtype, constellation, height, status, portrait, link FROM members where rome = '%s';"%query_parameter["member"]
        elif query_parameter["member"]=="all":
            sql_member_detail = "SELECT name, kana, rome, birthdate, bloodtype, constellation, height, status, portrait, link FROM members order by kana;"
        else:
            return web.HTTPNotFound()
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute(sql_member_detail)
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(reason="no such member")

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    introlist = []

    for line in out:
        intro=collections.OrderedDict()
        intro['name'] = line[0]
        intro['kana'] = line[1]
        intro['rome'] = line[2]
        intro['birthdate'] = line[3]
        intro['bloodtype'] = line[4]
        intro['constellation'] = line[5]
        intro['height'] = line[6]
        intro['status'] = line[7]
        intro['portrait'] = line[8]
        intro['link'] = line[9]
        introlist.append(intro)

    if len(introlist)==1:
        return web.Response(text=json.dumps(introlist[0],ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')
    else:
        return web.Response(text=json.dumps(introlist,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    app.router.add_route('POST', '/session/clean', clean)
    app.router.add_route('POST', '/submit/photo', photo_bed)
    app.router.add_route('POST', '/submit/article', article)
    app.router.add_route('POST', '/delete/photo', delete_photo)
    app.router.add_route('GET', '/preview/article/{room:\d{6}}', preview)
    app.router.add_route('POST', '/delete/article/{room:\d{6}}', delete_article)
    app.router.add_route('GET', '/mbview/article/{room:\d{6}}', mbview)
    app.router.add_route('GET', '/data/list', entrylist)
    app.router.add_route('GET', '/data/{room:\d{6}}', oneentry)
    app.router.add_route('GET', '/data/blogs', blogs)
    app.router.add_route('GET', '/data/intro', memberdetail)
    app.router.add_route('GET', '/check/version/{os:\w+}', version)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', port)
    print('Server started at port %s...'%port)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool())
loop.run_until_complete(init(loop))
loop.run_forever()
