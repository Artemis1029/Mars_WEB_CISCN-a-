#Mars-Web-CISCN	

基于模板二次开发，

```
docker up -d		启动
```

漏洞所在www/sshop/views/Shop.py第79行

```python
            success = yaml.load(price)

            return self.render('pay.html', danger=success)
```

这里直接利用了缺陷函数yaml.load()解析了数据，然后返回数据，因为yaml解析时候使用的load方法存在反序列化命令执行的漏洞问题，这里可以由此构造payload，用于读取服务器文件