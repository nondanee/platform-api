# APIs' documentation for "platform.idolx46.top"  
idol文章提交平台的接口文档  
  
平台说明：  
&nbsp;&nbsp;&nbsp;&nbsp;平台全站依然使用HTTPS  
&nbsp;&nbsp;&nbsp;&nbsp;另外开了4600端口给接口使用（仅JSON数据接口），使用HTTP  
&nbsp;&nbsp;&nbsp;&nbsp;提交的数据已经全部入库  
&nbsp;&nbsp;&nbsp;&nbsp;所有接口其实都是静态接口  
  
接口地址：  
&nbsp;&nbsp;&nbsp;&nbsp;https://platform.idolx46.top/data/...  
&nbsp;&nbsp;&nbsp;&nbsp;http://platform.idolx46.top:4600/data/...


##  1.得到文章的列表数据（时间倒序）  

  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list`&nbsp;&nbsp;&nbsp;&nbsp;所有文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=blog`&nbsp;&nbsp;&nbsp;&nbsp;博客文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=news`&nbsp;&nbsp;&nbsp;&nbsp;新闻文章  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/list?type=magazine`&nbsp;&nbsp;&nbsp;&nbsp;杂志文章  

### 请求参数：
| 参数     | 说明   |
| :------   | :------------  |
| type   | 分类（news / magazine / blog / 有效，不填则为所有分类）  |
| page   | 页码（从1开始）   |
| size   | 每页条数（默认每页10条）   |
  
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
| view   | 文章预览（等别人做适配）   |
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
		"view": "/preview/article/381269",
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
	"view": "/preview/article/573142",
	"withpic": [
		"https://platform.idolx46.top/photo/573142/9cfb20df84e4b13eeda338d072b34b33.jpg",
		"https://platform.idolx46.top/photo/573142/ed85db1753a4ccd13652a14b92222b75.jpg",
		"https://platform.idolx46.top/photo/573142/6f5ab3d3bc856dda16ea70c1d0fa1e21.jpg"
	]
  }
  ......
]
```
### 出错：  
&nbsp;&nbsp;&nbsp;&nbsp;分类不存在		400 no that type 
&nbsp;&nbsp;&nbsp;&nbsp;该页是空		200 empty page


##  2.得到指定文章的详细数据    
  
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
| article   | 文章全文   |
  
### 返回实例：  
```
{
  "id": "573142",
  "delivery": 1491564360,
  "type": "blog",
  "title": "就很可爱",
  "subtitle": "Ray",
  "provider": "日不懂语翻不会译的团长",
  "article": "阿靓「今天的Ray拍摄感觉如何」<br><br>阿头「很棒、我很少有机会跟麻衣羊两个人一起拍摄、这次就在旁边、感觉自己就像成了模特儿一样」<br><br>阿靓「真棒、那玲香呢」<br><br>阿香「Ray的氛围很可爱、一进到现场、感觉自己就像成了女生一样」<br><br>3人「冷静点、你本来就是女生」<br><br>阿朱「我的话、这次和平常的妆容也不一样很兴奋、而且平常很少能在现场看见模特形态下的麻衣羊、刚才看见她摆姿势的样子、简直流弊到不行」<br><br>2人「很可爱呢」<br><br>阿靓「（摆手）」<br><br>阿朱「就很可爱」<br><br><img src=\"https://platform.idolx46.top/photo/573142/9cfb20df84e4b13eeda338d072b34b33.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/ed85db1753a4ccd13652a14b92222b75.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/6f5ab3d3bc856dda16ea70c1d0fa1e21.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/dfcc3a65895e3e4d2b8a077002c66998.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/c09c1daf9d8393db7a08443feafae21c.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/058d044c41c2d352e3d6e4d9fd699e16.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/b6d4d0f9b9a111dbcdba1379cf5a50c1.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/543d28f4aac877b184af5639d3c37b6d.jpg\"><br><br><img src=\"https://platform.idolx46.top/photo/573142/cfb8fa53ec3527266917e143259d5615.jpg\"><br><br>"
}
```
  
注：  
&nbsp;&nbsp;&nbsp;&nbsp;全文都已转换成html格式，图片链接是绝对链接，无需处理  