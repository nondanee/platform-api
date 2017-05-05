# 乃木物APP后台接口文档  
    
接口说明：  
&nbsp;&nbsp;&nbsp;&nbsp;平台全站使用HTTPS  
&nbsp;&nbsp;&nbsp;&nbsp;另开外4600端口给数据接口使用，使用HTTP  
  
接口地址：  
&nbsp;&nbsp;&nbsp;&nbsp;https://platform.idolx46.top/data/...  
&nbsp;&nbsp;&nbsp;&nbsp;http://platform.idolx46.top:4600/data/...


##  1.文章列表接口（时间倒序）  

  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list`&nbsp;&nbsp;&nbsp;&nbsp;所有文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=blog`&nbsp;&nbsp;&nbsp;&nbsp;博客文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=news`&nbsp;&nbsp;&nbsp;&nbsp;新闻文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=magazine`&nbsp;&nbsp;&nbsp;&nbsp;杂志文章  

### 请求参数：
| 参数     | 说明   |
| :------   | :------------  |
| type   | 分类（news / magazine / blog 有效，没有该参数默认所有分类）  |
| page   | 页码（从1开始）   |
| size   | 每页条数（没有该参数默认每页10条）   |
  
### 键值定义：  
| 字段        | 说明   |
| :--------   | :-----------------  |
| id   | 文章ID   |
| delivery   | 文章投送时间（时戳）   | 
| type   | 文章类型（ blog / news / magazine ）   |
| title   | 文章标题   |
| subtitle   | 文章副标题（ 成员名 / 新闻站点 / 杂志名 ）   |
| provider   | 提供者 （ 字幕组名字 ）   |
| summary   | 文章摘要 （ 不超过80字 ）   |
| detail   | 文章详细   |
| view   | 文章预览（移动端页面）   |
| withpic   | 文章附图（没有配图为null，3张以下显示1张，3张及以上显示3张）   |
  
### 返回实例：  
```
[
	{
		"id": "381269",
		"delivery": 1491565920,
		"type": "magazine",
		"title": "面对新人类",
		"subtitle": "21世纪出生的新加入的伙伴们",
		"provider": "尚基（PosiPeace字幕组）×花舞（泪痣小八字幕组）",
		"summary": "小実和花奈琳搭档，初次与三期生的中学生成员们进行对谈。一开始二人就在21世纪出生的新人面前毫不掩饰自己的震惊。对着这两个天真烂漫的人才，天生就喜欢偶像的二人也变...",
		"detail": "/data/381269",
		"view": "/mbview/article/381269",
		"withpic": null
	},
	{
		"id": "573142",
		"delivery": 1491564360,
		"type": "blog",
		"title": "就很可爱",
		"subtitle": "Ray",
		"provider": "日不懂语翻不会译的团长",
		"summary": "阿靓「今天的Ray拍摄感觉如何」 阿头「很棒、我很少有机会跟麻衣羊两个人一起拍摄、这次就在旁边、感觉自己就像成了模特儿一样」 阿靓「真棒、那玲香呢」 阿香「Ra...",
		"detail": "/data/573142",
		"view": "/mbview/article/573142",
		"withpic": [
			{"image": "https://platform.idolx46.top/photo/573142/9cfb20df84e4b13eeda338d072b34b33.jpg"},
			{"image": "https://platform.idolx46.top/photo/573142/ed85db1753a4ccd13652a14b92222b75.jpg"},
			{"image": "https://platform.idolx46.top/photo/573142/6f5ab3d3bc856dda16ea70c1d0fa1e21.jpg"}
		]
	},
	......
]
```
### 出错：  
&nbsp;&nbsp;&nbsp;&nbsp;分类不存在		400 no that type  
&nbsp;&nbsp;&nbsp;&nbsp;该页是空		404 empty page  


##  2.详细数据接口    
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/:id:`  

### 字段定义：  

| 字段        | 说明   |
| :--------   | :---------------  |
| id   | 文章ID   |
| delivery   | 文章投送时间（时戳）   | 
| type   | 文章类型（ blog / news / magazine ）   |
| title   | 文章题目   |
| subtitle   | 文章副标题（ 成员名 / 新闻站点 / 杂志名 ）   |
| provider   | 提供者 （ 字幕组名字 ）   |
| article   | 文章全文（html格式）   |
  
### 返回实例：  
```
{
	"id": "646480",
	"delivery": 1491577500,
	"type": "news",
	"title": "「Love music」",
	"subtitle": "miwaスタッフtwitter",
	"provider": "日不懂语翻不会译的团长",
	"article": "miwaスタッフ【公式】@miwastaff	<br><br>今晚23時在富士台的「Love music」中、将会和播放乃木坂46的各位合唱「結-ゆい-」！<br><br><img src=\"https://platform.idolx46.top/photo/646480/587454e923f04c96ed61cf5bfba280d5.jpg\"><br>"
}
```


##  3.官博数据接口（时间倒序）  

  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/blogs`&nbsp;&nbsp;&nbsp;&nbsp;  

### 成员名称字典：   
| 成员名     | 请求参数    |
| :--------   | :--------------  |
| 秋元真夏                       | akimoto-manatsu        |
| 生田絵梨花                     | ikuta-erika            |
| 生駒里奈                       | ikoma-rina             |
| 伊藤かりん                     | itou-karin             |
| 伊藤純奈                       | itou-junna             |
| 伊藤万理華                     | itou-marika            |
| 伊藤理々杏                     | itou-riria             |
| 井上小百合                     | inoue-sayuri           |
| 岩本蓮加                       | iwamoto-renka          |
| 梅澤美波                       | umezawa-minami         |
| 衛藤美彩                       | etou-misa              |
| 大園桃子                       | oozono-momoko          |
| 川後陽菜                       | kawago-hina            |
| 川村真洋                       | kawamura-mahiro        |
| 北野日奈子                     | kitano-hinako          |
| 久保史緒里                     | kubo-shiori            |
| 齋藤飛鳥                       | saitou-asuka           |
| 斎藤ちはる                     | saitou-chiharu         |
| 斉藤優里                       | saitou-yuuri           |
| 阪口珠美                       | sakaguchi-tamami       |
| 相楽伊織                       | sagara-iori            |
| 桜井玲香                       | sakurai-reika          |
| 佐々木琴子                     | sasaki-kotoko          |
| 佐藤楓                         | satou-kaede            |
| 白石麻衣                       | shiraishi-mai          |
| 新内眞衣                       | shinuchi-mai           |
| 鈴木絢音                       | suzuki-ayane           |
| 高山一実                       | takayama-kazumi        |
| 寺田蘭世                       | terada-ranze           |
| 中田花奈                       | nakada-kana            |
| 中村麗乃                       | nakamura-reno          |
| 中元日芽香                     | nakamoto-himeka        |
| 西野七瀬                       | nishino-nanase         |
| 能條愛未                       | noujou-ami             |
| 樋口日奈                       | higuchi-hina           |
| 星野みなみ                     | hoshino-minami         |
| 堀未央奈                       | hori-miona             |
| 松村沙友理                     | matsumura-sayuri       |
| 向井葉月                       | mukai-hazuki           |
| 山崎怜奈                       | yamazaki-rena          |
| 山下美月                       | yamashita-mizuki       |
| 吉田綾乃クリスティー           | yoshida-ayano-christie |
| 与田祐希                       | yoda-yuuki             |
| 若月佑美                       | wakatsuki-yumi         |
| 和田まあや                     | wada-maaya             |
| 渡辺みり愛                     | watanabe-miria         |
| 研究生                         | kenkyuusei             |
| スタッフブログ                 | unei-sutaffu           |

### 请求参数：
| 参数     | 说明   |
| :------   | :------------  |
| member   | 对照成员名称字典，该列表可从接口获得(没有该参数默认成员) |
| page   | 页码（从1开始）   |
| size   | 每页条数（没有该参数默认每页10条）   |
  
### 键值定义：  
| 字段        | 说明   |
| :--------   | :-----------------  |
| post   | 发布时间（时戳）   | 
| author   | 成员名   |
| title   | 博客标题   |
| summary   | 博客摘要 （ 官博移动版数据 ）   |
| url   | 官博链接   |
  
### 返回实例：  
```
[
	{
		"post": 1492429680,
		"author": "伊藤純奈",
		"title": "犬夜叉、おわり。",
		"summary": " \n \n \n \n \nこんばんは！\n伊藤純奈です\n \n \n\n \n\n \n \nオフショット〜〜\n \n ...",
		"url": "http://blog.nogizaka46.com/junna.itou/smph/2017/04/038155.php"
	},
	{
		"post": 1492417200,
		"author": "若月佑美",
		"title": "あれ？若また稽古してるの？",
		"summary": "というメンバーからの言葉に\nちょっと笑ってしまった。光栄な事です。\n \n\n \n舞台 犬夜叉 千穐...",
		"url": "http://blog.nogizaka46.com/yumi.wakatsuki/smph/2017/04/038148.php"
	},
	{
		"post": 1492410240,
		"author": "中元日芽香",
		"title": "ひめたん-0o0-その698",
		"summary": " \n\n \n日曜の夜は、らじらー！サンデー\n \nゲストは寺田蘭世ちゃんでした( ˆωˆ )\n聞いて...",
		"url": "http://blog.nogizaka46.com/himeka.nakamoto/smph/2017/04/038131.php"
	},
	{
		"post": 1492408500,
		"author": "白石麻衣",
		"title": "ポカポカ。",
		"summary": "こんにちは&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;お久しぶりです...",
		"url": "http://blog.nogizaka46.com/mai.shiraishi/smph/2017/04/038130.php"
	},
	......
	{
		"post": 1492344720,
		"author": "川村真洋",
		"title": "はろ♡",
		"summary": "&nbsp;こんにちは♡ろってぃーです．&nbsp;&nbsp;&nbsp;今日は暖かかったです...",
		"url": "http://blog.nogizaka46.com/mahiro.kawamura/smph/2017/04/038125.php"
	}
]
```
### 出错：  
&nbsp;&nbsp;&nbsp;&nbsp;成员不存在		400 no such member  
&nbsp;&nbsp;&nbsp;&nbsp;该页是空		404 empty page    




##  4.成员列表接口   
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/memberlist`&nbsp;&nbsp;&nbsp;&nbsp;(简版，含"研究生"、"スタッフブログ"项)  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/members`&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&nbsp;&nbsp;&nbsp;`/data/intro?member=all`&nbsp;&nbsp;&nbsp;&nbsp;(详细，不含"研究生"、"スタッフブログ"项)  

### 字段定义：  

| 字段        | 说明   |
| :--------   | :---------------  |
| name   | 姓名   |
| kana   | 姓名-平假名   | 
| rome   | 姓名-罗马音(接口3,接口5的member参数请求值)   |
| birthdate   | 出生日期   |
| bloodtype   | 血型   |
| constellation   | 星座   |
| height   | 身高   |
| status   | 选拔情况   |
| portrait   | 公式照   |
| link   | 官网连接   |
  
### 返回实例(简版)：  
```
[
	{
		"name": "秋元真夏",
		"rome": "akimoto-manatsu",
		"portrait": "http://img.nogizaka46.com/www/smph/member/img/akimotomanatsu_prof.jpg"
	},
	...
	{
		"name": "スタッフブログ",
		"rome": "unei-sutaffu",
		"portrait": "https://platform.idolx46.top/resource/sutaffu_prof.jpg"
	}
]
```

### 返回实例(详细)：
```
[
	{
		"name": "秋元真夏",
		"kana": "あきもと まなつ",
		"rome": "akimoto-manatsu",
		"birthdate": "1993年8月20日",
		"bloodtype": "B型",
		"constellation": "しし座",
		"height": "156cm",
		"status": "1期生 選抜メンバー 十二福神",
		"portrait": "http://img.nogizaka46.com/www/smph/member/img/akimotomanatsu_prof.jpg",
		"link": "http://www.nogizaka46.com/smph/member/detail/akimotomanatsu.php"
	},
	...
	{
		"name": "和田まあや",
		"kana": "わだ まあや",
		"rome": "wada-maaya",
		"birthdate": "1998年4月23日",
		"bloodtype": "O型",
		"constellation": "おうし座",
		"height": "157cm",
		"status": "1期生 アンダー",
		"portrait": "http://img.nogizaka46.com/www/smph/member/img/wadamaaya_prof.jpg",
		"link": "http://www.nogizaka46.com/smph/member/detail/wadamaaya.php"
	}
]
```

##  5.成员介绍接口  

### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/intro`  

### 请求参数：
| 参数     | 说明   |
| :------   | :------------  |
| member   | 对照成员名称字典，该列表可从接口获得 |

### 字段定义：  

| 字段        | 说明   |
| :--------   | :---------------  |
| name   | 姓名   |
| kana   | 姓名-平假名   | 
| rome   | 姓名-罗马音   |
| birthdate   | 出生日期   |
| bloodtype   | 血型   |
| constellation   | 星座   |
| height   | 身高   |
| status   | 选拔情况   |
| portrait   | 公式照   |
| link   | 官网连接   |
  
### 返回实例：  
```  
{
	"name": "秋元真夏",
	"kana": "あきもと まなつ",
	"rome": "akimoto-manatsu",
	"birthdate": "1993年8月20日",
	"bloodtype": "B型",
	"constellation": "しし座",
	"height": "156cm",
	"status": "1期生 選抜メンバー 十二福神",
	"portrait": "http://img.nogizaka46.com/www/smph/member/img/akimotomanatsu_prof.jpg",
	"link": "http://www.nogizaka46.com/smph/member/detail/akimotomanatsu.php"
}
```  

### 出错：  
&nbsp;&nbsp;&nbsp;&nbsp;成员不存在		400 no such member  
&nbsp;&nbsp;&nbsp;&nbsp;缺少参数		400 required parameter miss   
   
##  6.APP更新接口    
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/check/version/android`  

### 字段定义：  

| 字段        | 说明   |
| :--------   | :---------------  |
| versionCode   | 版本编码  |
| versionName   | 版本号   | 
| msg   | 更新描述   |
| download   | 下载地址   |
  
### 返回实例：  
```
{
	"versionCode": 2,
	"versionName": "1.0",
	"msg": "fixed some bugs",
	"download": "https://platform.idolx46.top/resource/app-debug.apk"
}
```