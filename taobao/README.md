# 使用Selenium爬取淘宝商品
```
通过用Selenium来模拟游览器 来抓取淘宝的商品信息并用pyquery解析得到商品的图片、名称、价格、购买人数、店铺名称和店铺所在地信息
```
### 步骤

1. 安装Selenium、firefox 及驱动
2. 打开淘宝页面，搜索商品，比如iPad，可以看到很多商品列表
    * 淘宝获取数据是通过调用ajax请求（审查元素-网络）
    * 接口https://s.taobao.com/api?xxx
    * 也可以通过构造ajax请求来抓取数据（发现参数的规律）

3. 页面分析 每一条商品都包括品的基本信息，包括商品图片、名称、价格、购买人数、店铺名称和店铺所在地，我们要做的就是将这些信息都抓取下来。
    * 搜索界面的简化url 为https://s.taobao.com/search?q=xx（爬取的商品） q为关键字只要改变这个参数，即可获取不同商品的列表
    * 通过分页信息抓取每一页的展现的商品（通过跳转的方式）
5. 获取商品列表
    * 如果是第一页加载搜索url请求第一页
    * 等待商品信息加载出来（在网页里面查看）及当前页码
    * 如果不是第一页 跳转到下一页
6. 通过pyquery解析商品列表

- [ ] 保存到数据库

### 用法
```
usage: tb.py [-h] product [product ...]

Selenium Crawl Taobao Product Example: python tb.py xxx;

positional arguments:
  product     Enter a product

optional arguments:
  -h, --help  show this help message and exit

```
