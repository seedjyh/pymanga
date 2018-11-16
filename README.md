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
