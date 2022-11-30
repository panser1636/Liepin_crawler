# Liepin_crawler
## 主要功能
1、使用scrapy框架对猎聘（招聘）网站进行多页爬取，爬取的信息为python行业的工作岗位，其对应的工作地点、工作薪资和工作要求；

2、对爬取到的信息基于管道化存储到Mysql数据库，为了可以导出运行文件，运行文件中为Sqlite3数据库(也可保存到本地数据库中)；

3、对Mysql的数据进行处理和数据分析，分析得到每个城市的平均薪酬、每个岗位的平均薪酬以及每个城市的岗位数量图；

4、使用streamlit方法将数据内容和数据分析的结果在网页显示，前端用户可根据岗位名称、岗位地点、薪资字段进行筛选、查询相关数据。


## 使用手册
1、首先进入工程文件夹 ： `cd  bosspro2  # 工程文件夹的路径`

2、然后执行命令：  `scrapy crawl boss2`  即可运行爬虫文件 

![image](https://user-images.githubusercontent.com/81425936/204834916-9dcf9838-3e08-4dab-b63b-c8d24acd5521.png)

3、打开 show_data 文件夹

  直接在命令行执行 `streamlit run D:\pachong\show_data\showdata.py  # 该文件的路径`

左边区域为复选框，选择不同的选项会筛选出三个选项中至少符合其中一个的选项的内容；

将表格数据拉至底端，会出现一个数据展示的按钮,点击该按钮，即可浏览数据分析的图

  
