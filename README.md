# picture_spider
Python3.7.3
Scrapy1.6.0

爬取 https://www.zhainanfu.com/tuku 下的图片，分别保存在各自的文件夹。

自己定制Scrapy的图片管道，重写了file_path方法来实现图片保存在不同文件夹。

还有一个问题还没解决，Scrapy的ImagesPipeline默认无法保存gif，
因此下载下来的gif全是静态的，需要重写ImagesPipeline中的下载方法。
