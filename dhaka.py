import selenium.webdriver
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--stuid', required=True)
parser.add_argument('--password', required=True)
parser.add_argument('--addr', default='中国江苏省南京市栖霞区仙林大道')
config = parser.parse_args()

# Using selenium because I'm lazy
c = selenium.webdriver.Chrome()
c.get('http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do')
c.find_element_by_id('username').send_keys(config.stuid)
c.find_element_by_id('password').send_keys(config.password)
c.find_element_by_class_name('auth_login_btn').click()
cookies = {x['name']: x['value'] for x in c.get_cookies()}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
}

response = requests.get('http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do', headers=headers, cookies=cookies, verify=False)
wid = response.json()['data'][0]['WID']
print(response.json()['data'][0])

params = {
    'WID': wid,
    'CURR_LOCATION': config.addr,
    'IS_TWZC': 1,
    'IS_HAS_JKQK': 1,
    'JRSKMYS': 1,
    'JZRJRSKMYS': 1
}

response = requests.get(r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do', params=params, headers=headers, cookies=cookies, verify=False)
print(response.text)

c.quit()