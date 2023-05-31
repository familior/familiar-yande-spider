# YandeSpider

## 下载

本程序使用IDM进行下载，所以要先配置好IDM的目录才行

idman [/q | /h | /n | /a] [/d URL] [/p 下载目录] [/f 自定义文件名]
/d URL 		- 下载一个文件，等等。
/s		 	- 开始任务调度里的队列
/p 下载目录  	- 定义要保存的文件放在哪个本地路径
/f 自定义文件名   - 定义要保存的文件到本地的文件名
/q 			- IDM 将在成功下载之后退出。这个参数只为第一个副本工作
/h 			- IDM 将在成功下载之后挂起您的连接
/n 			- 当不要 IDM 询问任何问题时启用安静模式
/a 			- 添加下载任务时候，不要开始下载

~~~
# 添加队列
IDMan.exe /a /d https://files.yande.re/image/eab73ae33da105f13ed6f3e8e1dc2df3/yande.re%201092685%20ass%20garter_belt%20hololive%20hololive_english%20mori_calliope%20naked%20stockings%20tagme%20thighhighs.png
# 开始队列
IDMan.exe /s
~~~

## Post的地址规律

### 收藏处获取的地址有以下组合

image-jpg（当该图片只有jpg格式时候）

~~~
https://files.yande.re/image/ef69029be3cd237fe1cd72831195a062/yande.re%20498401%20anmi%20cleavage%20leotard%20no_bra%20pantsu%20pantyhose%20skirt_lift.jpg
~~~

jpeg-jpg（当该图片还有png格式可以选择的时候）

~~~
https://files.yande.re/jpeg/44e1ac393f56cf4392680e567f010b2d/yande.re%20515970%20anmi.jpg
~~~

sample-jpg（当该图片还有png格式可以选择的时候）

~~~
https://files.yande.re/sample/73355b927cd86dfc28dbd9b689ff504f/yande.re%20494284%20sample%20anmi%20bra%20cleavage%20dakimakura%20fate_grand_order%20garter%20megane_shoujo%20pantsu%20saber_extra.jpg
~~~

有上面的规律就好办了，

爬取到的如果是image-jpg组合就直接添加进列表中，

如果是jpeg-jpg组合就将jpeg修改成image，jpg修改成png，

如果是sample-jpg组合就将sample修改成image，jpg修改成png，把链接中的%20sample%20修改成%20



### 二级页面内获取的链接有以下组合
image-png（最优文件）

image-jpg（jpg次优文件）

sample-jpg（压缩垃圾文件，这种必须替换）

已经没必要从二级页面中获取真正的下载链接了，从收藏处就能分析出真正的下载链接



### 地址栏处出现过的有以下四种组合，就是总结上面的情况

image-png（最优文件）

image-jpg（jpg次优文件）

jpeg-jpg（jpg次优文件，但还能更好，需要替换）

sample-jpg（压缩垃圾文件，这种必须替换）
