from selenium import webdriver
from  selenium.webdriver.common.by  import  By

from time import sleep
import time
import json
import re

def get_sub_task(task):
    driver = webdriver.Chrome()
    # 发起url请求
    driver.get(task['url'])
    time.sleep(3)
    div = driver.find_elements(By.CLASS_NAME, "zzxq_right")
    div = div[1]
    a_link_list = div.find_elements(By.TAG_NAME,"a")
    task_list = []
    for locals in a_link_list:
        if locals.text != '全部':
            task_list.append({
                'url':locals.get_attribute("href"),
                'tag':locals.text
            })
    return task_list


def get_page_info(task):
    driver = webdriver.Chrome()
    # 发起url请求
    driver.get(task['url'])
    time.sleep(3)
    div = driver.find_element(By.CLASS_NAME, "zxlb")
    house_item = div.find_elements(By.TAG_NAME,"li")
    for house in house_item:
        status = house.find_element(By.CLASS_NAME,"material-card")
        name = house.find_element(By.TAG_NAME,"h3").text
        time_info = house.find_element(By.CLASS_NAME,"timeBox").get_attribute('data-times') 
        infos = house.find_element(By.CLASS_NAME,"man_bom").find_elements(By.TAG_NAME,"span")
        print('-----------------------------------------------')
        cheng_jiao_jia_ = 0
        if '已经成交' in status.text:
            cheng_jiao_jia_ = status.find_element(By.TAG_NAME,"span").text
        status_info = status.text.split('\n')[0]
        assert(len(infos) == 5)
        #
        mian_ji_ = infos[0].text
        chao_xiang_ = infos[1].text
        ju_shi_ = infos[2].text
        qi_pai_jia_ = infos[3].text
        shi_chang_jia_ = infos[4].text
        #
        shi_chang_jia_ = re.findall(r'\d+',str(shi_chang_jia_))[0]
        qi_pai_jia_ = re.findall(r'\d+',str(qi_pai_jia_))[0]
        cheng_jiao_jia_ = re.findall(r'\d+',str(cheng_jiao_jia_))[0]
        mian_ji_ = re.findall(r'\d+',str(mian_ji_))[0]
        #
        print('name',name)
        print('status',status_info)
        print('shi_chang_jia_',shi_chang_jia_)
        print('qi_pai_jia_',qi_pai_jia_)
        print('cheng_jiao_jia_', cheng_jiao_jia_)
        print('cheng_jiao_shi_jian_',time_info)
        print('mian_ji_',mian_ji_)
        print('chao_xiang_',chao_xiang_)
        print('ju_shi_',ju_shi_)


if __name__ == '__main__':
    url = 'https://www.yipaibj.com/fapai/yong_type/0/price/0/acreage/0/ci_type/0/room/0/xian_type/0/zhuangtai/0/bmrs/0/priceb/0/pricet/0/acrb/0/acrt/0/keyword/0/area/1/metro_station/0/metro/0'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    div = driver.find_element(By.CLASS_NAME, "zzxq_right")
    a_link_list = div.find_elements(By.TAG_NAME,"a")
    page_num = driver.find_element(By.CLASS_NAME,"pagination").find_elements(By.TAG_NAME,'li')[-2].text

    task_list = []
    for locals in a_link_list:
        if locals.text != '全部':
            task_list.append({
                'url':locals.get_attribute("href"),
                'tag':locals.text,
                'page_num':page_num
            })

    for task in task_list:
        print(task['url'])
        task['children'] = get_sub_task(task)
    
    with open('task.json' , 'w', encoding='utf-8') as f:
        f.write(json.dumps(task_list,ensure_ascii=False))

    # get_page_info({
    #     'url':'https://www.yipaibj.com/fapai-331-0-0-0-0-0-0-0-0-0-0-0-0-1-0-0/xian_type/0/zhuangtai/0/index_type/0/end/0/bmrs/0/priceb/0/pricet/0/acrt/0/acrb/0/pai_type/0/keyword/0.html?page=1',
    #     'tag1':"昌平",
    #     'tag2':"天通苑",
    # })
