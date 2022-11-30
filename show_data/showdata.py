import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import re
import streamlit as st
import operator

# streamlit run D:\学习\大二下课件与学习资料\python\爬虫大作业\bosspro2\bosspro2\showdata.py

import sqlite3

def create_table():
    conn = sqlite3.connect(r'D:\job_information.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE python_liepin (job_name CHAR(100), job_salary CHAR(50), job_address CHAR(100),job_demand TEXT);')
    cursor.close()
    conn.close()


# def show_database():
#     conn = sqlite3.connect(r'D:\job_information.db')
#     cursor = conn.cursor()
#     cursor.execute(
#         'SELECT job_name,job_salary FROM python_liepin;')
#     for row in cursor:
#         print("job_name = ", row[0])
#         print("job_salary = ", row[1], "\n")
#
#     cursor.close()
#     conn.close()
#
create_table()
# show_database()

st.title('查询岗位信息：')
@st.cache
def load_data():
    conn = sqlite3.connect(r'D:\job_information.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM python_liepin')
    data = cursor.fetchall()
    conn.commit()

    data_dataframe = []
    i = 0
    for i in range(len(data)):
        data_dataframe.append(list(data[i]))
    df = pd.DataFrame(data_dataframe, columns=['岗位名称', '薪资', '工作地点', '工作要求'])
    cursor.close()
    conn.close()


    return df
#pyinstaller -D D:\学习\大二下课件与学习资料\python\爬虫大作业\bosspro2\bosspro2\spiders\boss2.py
def show_data():
    conn = sqlite3.connect(r'D:\job_information.db')
    cursor = conn.cursor()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False   # 解决中文显示问题
    # 从数据库中提取数据
    data = dict()
    cursor.execute('SELECT job_salary FROM python_liepin')
    data['job_salary'] = list(cursor.fetchall())
    cursor.execute('SELECT job_name FROM python_liepin')
    data['job_name'] = list(cursor.fetchall())
    cursor.execute('SELECT job_address FROM python_liepin')
    data['job_address'] = list(cursor.fetchall())

    print(data['job_salary'])
    print(data['job_name'])
    print(data['job_address'])

    # 打印城市平均薪酬图&岗位平均薪酬
    address_salary = dict()  # 城市——薪酬
    job_2_salary = dict()  # 岗位——薪酬

    for i in range(len(data['job_salary'])):
        if re.match('\d+-\d+k.*',data['job_salary'][i][0]):
            salary_sin = int(data['job_salary'][i][0].split('-')[0])
            address_name = data['job_address'][i][0].split('-')[0]
            job_name_single = data['job_name'][i][0].split('（' or '，')[0]
            if address_name not in address_salary:
                address_salary[address_name] = []
            address_salary[address_name].append(salary_sin)
            if job_name_single not in job_2_salary:
                job_2_salary[job_name_single] = []
            job_2_salary[job_name_single].append(salary_sin)

    city_name = []  # 城市名字
    job_name_list = []  # 岗位名字
    city_salary = []  # 城市——平均薪酬
    job_salary = []  # 岗位——平均薪酬
    # 计算各城市平均薪酬
    for key in address_salary:
        address_salary[key] = sum(address_salary[key])/len(address_salary[key])
    address_salary = dict(sorted(address_salary.items(), key=operator.itemgetter(1), reverse=True))  # 排序
    for key in address_salary:
        city_name.append(key)
        city_salary.append(address_salary[key])
    # 计算各岗位平均薪酬
    for key in job_2_salary:
        job_2_salary[key] = sum(job_2_salary[key])/len(job_2_salary[key])
    job_2_salary = dict(sorted(job_2_salary.items(), key=operator.itemgetter(1), reverse=True))
    for key in job_2_salary:
        job_name_list.append(key)
        job_salary.append(job_2_salary[key])

    print(city_name)
    print(city_salary)
    print(job_name_list)
    print(job_salary)

    fig1 = plt.figure()
    bar1 = plt.bar(range(len(city_name)),city_salary, width= 0.8, align='center',color='green', alpha=0.6, tick_label=city_name)
    plt.xlabel("城市")
    plt.ylabel("月薪资/K")
    plt.title('城市平均薪酬/K')
    plt.xticks(rotation=345)
    plt.savefig(r'./城市平均薪酬(K).png')
    fig1.show()

    fig2 = plt.figure()
    bar2 = plt.plot(range(8),job_salary[:8], 'bo-', alpha=0.6)
    plt.xticks(range(8),job_name_list[:8])
    plt.xlabel("岗位")
    plt.ylabel("月薪资/K")
    plt.title('岗位平均薪酬/K')
    plt.xticks(rotation=270)
    plt.savefig(r'./岗位平均薪酬(K).png')
    fig2.show()

    # 打印城市岗位数量图
    city_name_2 = [] # 城市名称
    job_number_city = {} # 城市——岗位
    number = [] # 各个城市的岗位数量
    for i in range(len(data['job_address'])):
        address_name_2 = data['job_address'][i][0].split('-')[0]
        if address_name_2 not in job_number_city:
                job_number_city[address_name_2] = 0
        job_number_city[address_name_2] = job_number_city[address_name_2] + 1

    job_number_city = dict(sorted(job_number_city.items(), key=operator.itemgetter(1), reverse=True))

    for key in job_number_city:
        number.append(job_number_city[key])
        city_name_2.append(key)
    print(job_number_city)
    print(city_name_2)

    fig3 = plt.figure()
    bar3 = plt.bar(range(8), number[:8], color="orange", width=0.6, alpha=0.4, align='center',tick_label=city_name_2[:8])
    plt.xlabel("城市")
    plt.ylabel("岗位数量")
    plt.title('城市岗位数量图')
    plt.xticks(rotation=270)
    plt.savefig(r'./城市岗位数量.png')
    fig3.show()

    # 断开数据库链接
    conn.commit()
    cursor.close()
    conn.close()


show_data()
df = load_data()
# st.table(df)
# 左边选框
job_name_list = df["岗位名称"].unique()
job_name = st.sidebar.selectbox(
    "请选择你想了解的岗位名称",
    job_name_list
)
job_address_list = df["工作地点"].unique()
address_name = st.sidebar.selectbox(
    "请选择你想了解的工作地点",
    job_address_list
)
job_salary_list = df["薪资"].unique()
salary_name = st.sidebar.selectbox(
    "请选择你想了解的薪酬",
    job_salary_list
)

part_df = df[(df["岗位名称"] == job_name) | (df['工作地点'] == address_name) | (df['薪资'] == salary_name)]
st.table(part_df)

if st.button('岗位数据分析') :
    st.image(r'./城市平均薪酬(K).png')
    st.image(r'./岗位平均薪酬(K).png')
    st.image(r'./城市岗位数量.png')