# pymanga

A spider downloading manga from website in framework scrapy.

## How to use

### Download from comic page
```bat
scrapy crawl dmzj -a url=https://manhua.dmzj.com/mix/
```

### Download from volume page
```bat
scrapy crawl dmzj -a url=https://manhua.dmzj.com/mix/24308.shtml
```

### Download from news page
```bat
scrapy crawl dmzj -a url=https://news.dmzj.com/article/9718.html
```

### Directory setting

in file `{spider}\pymanga\settings.py`

```python
# Enable FilesPipeline
FILES_STORE = 'D:\\tmp'

# Download
DOWNLOAD_STORE = "D:\\manga"
```

**FILES_STORE** is the location stores downloaded files temporarily.

**DOWNLOAD_STORE** is the location stores downloaded `{DOWNLOAD_STORE}\comic\volume\picture`.

## 开发新的网站爬虫

例子：`http://www.wuqimh.com/32481/`

### 创建爬虫框架

在项目目录下（该目录下有个`scrapy.cfg`）输入命令`scrapy genspider wuqimh wuqimh.com`。

如果看到

```shell
Created spider 'wuqimh' using template 'basic' in module:
  pymanga.spiders.wuqimh
```

说明创建成功。新增文件`{当前目录}/spiders/wuqimh.py`。

### 修改爬虫python文件

从别的爬虫里抄过来就行的：

* __all_urls
* __init__
* start_requests
* parse

需要根据网站页面进行处理的（使用xpath）：

* parse_comic_page

## 用Xpath找到漫画标题

**在非项目目录下**使用`scrapy shell http://www.wuqimh.com/2809/`，进入命令行。

此后输入的所有语句都可以直接用在`parse_comic_page`里，或其他类似方法里。


### Chrome和ChroPath

1. 用Chrome打开`http://www.wuqimh.com/2809/`。
1. 按F12，右键点击漫画页面正文里的漫画名，选择“检查(N)”。
1. 在右边窗口（第一个标签页是Style，第二个标签页是Computed）选择ChroPath标签页，选择`Rel XPath`行，内容估计是`//div[@class='book-title']//h1`。左键点击最左边的按钮，从而拷贝内容到剪贴板。
1. 在scrapy shell命令行里输入`response.xpath("//div[@class='book-title']//h1")`。根据情况，输入`response.xpath("//div[@class='book-title']//h1/text()").extract_first()`可以得到更简洁的结果。

## 故障处理

### 创建爬虫时找不到execjs包

`pip install PyExecJS`


