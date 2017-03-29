# APIs' documentation for "platform.idolx46.top"  
idol文章提交平台的接口文档（其实也没啥好写的）  
  
平台说明：  
&nbsp;&nbsp;&nbsp;&nbsp;平台全站使用HTTPS  
&nbsp;&nbsp;&nbsp;&nbsp;因提交没有任何限制，内容有效性也无法判断，所以暂时不考虑入库  
&nbsp;&nbsp;&nbsp;&nbsp;提交的数据仅以json的格式存储在文件中（类似mongodb？）  
&nbsp;&nbsp;&nbsp;&nbsp;所有接口其实都是静态接口  
  
接口地址：  
&nbsp;&nbsp;&nbsp;&nbsp;https://platform.idolx46.top/data/...


##  1.得到所有文章的列表数据  
**因存的只是文件，每次产生列表要遍历目录并排序，该接口每小时更新一次，而且不分页**  
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/getall`
  
### 键值定义：  
| 字段        | 说明   |
| :--------   | :---------------  |
| update   | 接口更新时间   |
| id   | 文章ID   |
| delivery   | 文章投送时间（时戳）   | 
| type   | 文章类型（ blog / news / magazine ）   |
| title   | 文章题目   |
| source   | 文章来源（ 博客作者 / 新闻站点 / 杂志名称）   |
| provider   | 提供者 （ 字幕组名字 ）   |
| summary   | 文章摘要 （ 不超过80字 ）   |
| detail   | 文章详细   |
  
### 返回实例：  
```
{
	"update": "2017/03/29 14:00",	
	"content": [
	{
		"id": "476665",
		"delivery": "1490762460",
		"type": "news",
		"title": "不BB",
		"source": "我",
		"provider": "想想",
		"summary": "\n\n",
		"detail": "/data/476665"
	},
	{
		"id": "845105",
		"delivery": "1490722980",
		"type": "blog",
		"title": "中文",
		"source": "紫薯",
		"provider": "红薯",
		"summary": "马铃薯\n\n",
		"detail": "/data/845105"
	},
	......
	]
}
```

##  2.得到指定文章的详细数据  
**nginx定义后的url，其实是静态文件分发**   
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/:id:`  
&nbsp;&nbsp;&nbsp;&nbsp;就是上一接口中的detail字段  
&nbsp;&nbsp;&nbsp;&nbsp;就是`/data/`后跟id号  
  
### 字段定义：  

| 字段        | 说明   |
| :--------   | :---------------  |
| title   | 文章题目   |
| type   | 文章类型（ blog / news / magazine ）   |
| source   | 文章来源（ 博客作者 / 新闻站点 / 杂志名称）   |
| provider   | 提供者 （ 字幕组名字 ）   |
| delivery   | 文章投送时间（可读的时间）   | 
| detail   | 文章全文   |
  
### 返回实例：  
```
{
	"title": "不BB",
	"type": "news",
	"source": "我",
	"provider": "想想",
	"delivery": "2017/03/29 12:41",
	"article": "![IMAGE](14afd06ecff7abf69102ae0743cab118.jpg)\n![IMAGE](14afd06ecff7abf69102ae0743cab118.jpg)\n"
}
```
  
注：  
&nbsp;&nbsp;&nbsp;&nbsp;文章中的图片遵循markdown的语法，但是文章本身不一定是按markdown语法写的。换行的语法就有好多种，这个坑我不跳  
&nbsp;&nbsp;&nbsp;&nbsp;文章中的图片链接是相对路径，显示要做处理。因为这是静态文件，提交时生成的，所以路径问题清客户端自己处理，等以后入库了再由接口处理，具体操作看下一个接口  

##  3.得到指定文章中的图片  
**图片名称用的是图片的MD5校验值，所以长**  
  
### 请求方法：  
&nbsp;&nbsp;&nbsp;&nbsp;GET	`/data/:id:/:filename:`  
&nbsp;&nbsp;&nbsp;&nbsp;也就是说由上一接口得到的文章全文中的图片路径前都要加上文章id  

	![IMAGE](14afd06ecff7abf69102ae0743cab118.jpg)  
	=> 
	![IMAGE](https://platform.idolx46.top/data/476665/14afd06ecff7abf69102ae0743cab118.jpg) 
  
### 返回实例：  
&nbsp;&nbsp;&nbsp;&nbsp;就是图片啊