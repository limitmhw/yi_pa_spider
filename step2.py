from selenium import webdriver
from  selenium.webdriver.common.by  import  By

from time import sleep
import time
import json
import re
import os
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_sub_task(task):
    driver = get_driver()
    # 发起url请求
    driver.get(task['url'])
    time.sleep(1)
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
    driver.close()
    return task_list


def get_page_info(task):
    driver = get_driver()
    # 发起url请求
    driver.get(task['url'])
    time.sleep(1)
    div = driver.find_element(By.CLASS_NAME, "zxlb")
    house_item = div.find_elements(By.TAG_NAME,"li")
    for house in house_item:
        status = house.find_element(By.CLASS_NAME,"material-card")
        name = house.find_element(By.TAG_NAME,"h3").text
        time_info = house.find_element(By.CLASS_NAME,"timeBox").get_attribute('data-times') 
        infos = house.find_element(By.CLASS_NAME,"man_bom").find_elements(By.TAG_NAME,"span")
        print('-----------------------------------------------')
        cheng_jiao_jia_ = '0'
        if '已经成交' in status.text:
            try:
                cheng_jiao_jia_ = status.find_element(By.TAG_NAME,"span").text
            except:
                print('error:',status.text)
                cheng_jiao_jia_ = status.text
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
        cheng_jiao_jia_list = re.findall(r'\d+',str(cheng_jiao_jia_))
        if len(cheng_jiao_jia_list) == 0:
            cheng_jiao_jia_ = '0'
        else:
            cheng_jiao_jia_ = cheng_jiao_jia_list[0]
        mian_ji_ = re.findall(r'\d+',str(mian_ji_))[0]
        #
        print('url',task['url'])
        print('tag1',task['tag1'])
        print('tag2',task['tag2'])
        print('name',name)
        print('status',status_info)
        print('shi_chang_jia_',shi_chang_jia_)
        print('qi_pai_jia_',qi_pai_jia_)
        print('cheng_jiao_jia_', cheng_jiao_jia_)
        print('cheng_jiao_shi_jian_',time_info)
        print('mian_ji_',mian_ji_)
        print('chao_xiang_',chao_xiang_)
        print('ju_shi_',ju_shi_)
        data = str(task['url']) + "," + str(task['tag1']) + "," + str(task['tag2']) + "," + str(name) + "," + str(status_info) + "," + str(shi_chang_jia_) + "," + str(qi_pai_jia_) + "," + str(cheng_jiao_jia_) + "," + str(time_info) + "," + str(mian_ji_) + "," + str(chao_xiang_) + "," + str(ju_shi_) + '\n'
        with open('house_data.csv','a',encoding='utf-8') as f:
            f.write(data)
    driver.close()


def get_loaction_info(task):
    driver = get_driver()
    driver.get(task['url'])
    print(task)
    time.sleep(1)
    page_num = 1
    try:
        page_num = driver.find_element(By.CLASS_NAME,"pagination").find_elements(By.TAG_NAME,'li')[-2].text
    except:
        pass
    task['page_num'] = page_num
    driver.close()
    return task

def update_history():
    history_set = set()
    tag_set = set()
    if os.path.exists('house_data.csv'):
        with open('house_data.csv','r',encoding='utf-8') as f :
            datalines =  f.readlines()
            last_data = datalines[-1]
            delete_url = last_data.split(',')[0]
            delete_tag = last_data.split(',')[1]
            delete_url_parent = delete_url.split('?')[0]
            new_datalines = []
            for line in datalines:
                if delete_url not in line:
                    new_datalines.append(line)

            for line in new_datalines:
                history_set.add(line.split(',')[0])
                parent_url = line.split(',')[0].split('?')[0]
                root_tag = line.split(',')[1]
                if root_tag != delete_tag:
                    tag_set.add(root_tag)
                if parent_url != delete_url_parent:
                    history_set.add(parent_url)
                else:
                    print(line)
            with open('house_data.csv','w',encoding='utf-8') as f:
                f.write(''.join(new_datalines))
    return history_set, tag_set

if __name__ == '__main__':
    json_dict = {}
    history_set, tag_set = update_history()
    with open('task.json','r',encoding='utf-8') as f :
        json_str = f.read()
        json_dict = json.loads(json_str)

    for k in json_dict:
        tag1 = k['tag']
        if tag1 in tag_set:
            continue
        for location in  k['children']:
            if location['url'] in history_set:
                continue
            task = {
                'url':location['url'],
                'tag1':tag1,
                'tag2':location['tag']
            }
            task = get_loaction_info(task)
            for page in range(1,int(task['page_num'])+1):
                task_tmp = {
                    'url':task['url'] + '?page=' + str(page),
                    'tag1':task['tag1'],
                    'tag2':task['tag2'],
                }
                if task_tmp['url'] not in history_set:
                    get_page_info(task_tmp)
                # print('page',page)
