# -*- coding: utf-8 -*-
import sys
import json
import uuid
import oss2
import yaml
import base64
import requests
import time
import random
import uanalyse
from pyDes import des, CBC, PAD_PKCS5
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning
import notification

# debug模式
debug = True
if debug:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rand_lon = str(random.randint(0, 9))
rand_lat = str(random.randint(0, 9))


# 读取yml配置
def getYmlConfig(yaml_file='config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)


# 全局配置
config = getYmlConfig(yaml_file='config.yml')


# 获取当前utc时间，并格式化为北京时间
def getTimeStr():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")


# 输出调试信息，并及时刷新缓冲区
def log(content):
    print(getTimeStr() + ' ' + str(content))
    sys.stdout.flush()


# 获取今日校园api
def getCpdailyApis(user):
    apis = {}
    user = user['user']
    if 'cpdaily' in user['ua']:
        print('你UA输入的有问题，请看说明书！')
        exit(2)
    if 'Android' not in user['ua']:
        print('你UA输入的有问题，请看说明书！')
        exit(2)
    schools = requests.get(url='https://mobile.campushoy.com/v6/config/guest/tenant/list', verify=not debug).json()[
        'data']
    flag = True
    for one in schools:
        if one['name'] == user['school']:
            if one['joinType'] == 'NONE':
                log(user['school'] + ' 未加入今日校园')
                exit(-1)
            flag = False
            params = {
                'ids': one['id']
            }
            res = requests.get(url='https://mobile.campushoy.com/v6/config/guest/tenant/info', params=params,
                               verify=not debug)
            data = res.json()['data'][0]
            joinType = data['joinType']
            idsUrl = data['idsUrl']
            ampUrl = data['ampUrl']
            if 'campusphere' in ampUrl or 'cpdaily' in ampUrl:
                parse = urlparse(ampUrl)
                host = parse.netloc
                res = requests.get(parse.scheme + '://' + host)
                parse = urlparse(res.url)
                apis[
                    'login-url'] = idsUrl + '/login?service=' + parse.scheme + r"%3A%2F%2F" + host + r'%2Fportal%2Flogin'
                apis['host'] = host

            ampUrl2 = data['ampUrl2']
            if 'campusphere' in ampUrl2 or 'cpdaily' in ampUrl2:
                parse = urlparse(ampUrl2)
                host = parse.netloc
                res = requests.get(parse.scheme + '://' + host)
                parse = urlparse(res.url)
                apis[
                    'login-url'] = idsUrl + '/login?service=' + parse.scheme + r"%3A%2F%2F" + host + r'%2Fportal%2Flogin'
                apis['host'] = host
            break
    if flag:
        log(user['school'] + ' 未找到该院校信息，请检查是否是学校全称错误')
        exit(-1)
    log(apis)
    return apis


# 登陆并获取session
def getSession(user, apis):
    user = user['user']
    params = {
        # 'login_url': 'http://authserverxg.swu.edu.cn/authserver/login?service=https://swu.cpdaily.com/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay',
        'login_url': apis['login-url'],
        'needcaptcha_url': '',
        'captcha_url': '',
        'username': user['username'],
        'password': user['password']
    }

    cookies = {}
    # 借助上一个项目开放出来的登陆API，模拟登陆
    if 'enable' in user:
        if user['enable'] == 0:
            print('您设定了enable=0,安全模式将不会获取COOKIE，您想要使用的话请删除config.yml里面的noapi=1!')
            sendMessage('如果您看到这条消息，请您去github上重新设置您的config。', user, '报错提醒-今日校园自动签到')
            exit(9)
    if user['usecookies'] == 0:
        res = ''
        try:
            j=0
            for i in range(0,5):
                print("使用config中定义的api")
                res = requests.post(config['login']['api'], data=params)
                if 'success' not in res.json()['msg']:
                    print(f'第{j+1}次未获取到Cookies')
                    j=j+1
                else:
                    break
            if 'success' not in res.json()['msg']:
                print(f'{j}次尝试也没有cookies，可能学校服务器坏了，自己弄吧！')
                sendMessage(f'如果您看到这条消息，证明{j}次尝试也没有cookies，可能学校服务器坏了，自己弄吧！', user)
                exit(888)
            print(res.json())
        except Exception as e:
            res = requests.post(url='http://www.zimo.wiki:8080/wisedu-unified-login-api-v1.0/api/login', data=params)
            print("使用子墨的API")
            if 'success' not in res.json()['msg']:
                print('用子墨的API也没有获取到Cookies')
                sendMessage(f'如果您看到这条消息，证明子墨的api也没有获取到cookies，可能学校服务器坏了，自己弄吧！', user, '报错提醒-今日校园自动签到')


        # cookieStr可以使用手动抓包获取到的cookie，有效期暂时未知，请自己测试
        # cookieStr = str(res.json()['cookies'])
        cookieStr = str(res.json()['cookies'])
        print('已从API获取到Cookie')
        #exit(999)
    else:
        cookieStr = user['cookies']
        print('使用文件内Cookie')
    print(cookieStr)
    # log(cookieStr) 调试时再输出
    # if cookieStr == 'None':
    # log(res.json())
    # exit(-1)
    # log(cookieStr)

    # 解析cookie
    for line in cookieStr.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
    return session


# 获取最新未签到任务并全部签到
def getUnSignedTasksAndSign(session, apis, user):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': user['user']['ua']+'  cpdaily/8.2.17 wisedu/8.2.17',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    print(headers)
    # 第一次请求每日签到任务接口，主要是为了获取MOD_AUTH_CAS
    res = session.post(
        url='https://{host}/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay'.format(host=apis['host']),
        headers=headers, data=json.dumps({}))
    # 第二次请求每日签到任务接口，拿到具体的签到任务
    res = session.post(
        url='https://{host}/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay'.format(host=apis['host']),
        headers=headers, data=json.dumps({}))
    print(res.json())
    if len(res.json()['datas']['unSignedTasks']) < 1:
        log('当前没有未签到任务')
        sendMessage('当前没有未签到任务', user['user'])
        exit(-1)
    elif time.localtime().tm_hour in [18, 19, 20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 5, 6, 7]:
        print('未在签到时间，等会再来吧！')
        sendMessage('自定义限制：未在签到时间，等会再来吧！', user['user'])
        #exit(8)
        #TODO 删掉


    # log(res.json())
    for i in range(0, len(res.json()['datas']['unSignedTasks'])):
        # if '出校' in res.json()['datas']['unSignedTasks'][i]['taskName'] == False:
        # if '入校' in res.json()['datas']['unSignedTasks'][i]['taskName'] == False:
        latestTask = res.json()['datas']['unSignedTasks'][i]
        params = {
            'signInstanceWid': latestTask['signInstanceWid'],
            'signWid': latestTask['signWid']
        }
        task = getDetailTask(session, params, apis, user)
        print(task)
        if time.localtime().tm_hour in [18, 19, 20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 5, 6, 7]:
            print('未在签到时间，等会再来吧！')
        form = fillForm(task, session, user, apis)
        print(form)
        if time.localtime().tm_hour in [18, 19, 20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 5, 6, 7]:
            print('未在签到时间，等会再来吧！')
        submitForm(session, user, form, apis)


# 获取签到任务详情
def getDetailTask(session, params, apis, user):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': user['user']['ua']+'  cpdaily/8.2.17 wisedu/8.2.17',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    print(headers)
    res = session.post(
        url='https://{host}/wec-counselor-sign-apps/stu/sign/detailSignInstance'.format(host=apis['host']),
        headers=headers, data=json.dumps(params))
    data = res.json()['datas']
    return data


# 填充表单
def fillForm(task, session, user, apis):
    user = user['user']
    form = {}
    if task['isPhoto'] == 1:
        fileName = uploadPicture(session, user['photo'], apis)
        form['signPhotoUrl'] = getPictureUrl(session, fileName, apis)
    else:
        form['signPhotoUrl'] = ''
    if task['isNeedExtra'] == 1:
        extraFields = task['extraField']
        defaults = config['cpdaily']['defaults']
        extraFieldItemValues = []
        for i in range(0, len(extraFields)):
            default = defaults[i]['default']
            extraField = extraFields[i]
            if config['cpdaily']['check'] and default['title'] != extraField['title']:
                log('第%d个默认配置项错误，请检查' % (i + 1))
                sendMessage('提交错误' + '第%d个默认配置项错误，请检查' % (i + 1), user)
                exit(-1)
            extraFieldItems = extraField['extraFieldItems']
            for extraFieldItem in extraFieldItems:
                if extraFieldItem['content'] == default['value']:
                    extraFieldItemValue = {'extraFieldItemValue': default['value'],
                                           'extraFieldItemWid': extraFieldItem['wid']}
                    # 其他，额外文本
                    if extraFieldItem['isOtherItems'] == 1:
                        extraFieldItemValue = {'extraFieldItemValue': default['other'],
                                               'extraFieldItemWid': extraFieldItem['wid']}
                    extraFieldItemValues.append(extraFieldItemValue)
        # log(extraFieldItemValues)
        # 处理带附加选项的签到
        form['extraFieldItems'] = extraFieldItemValues
    # form['signInstanceWid'] = params['signInstanceWid']
    form['signInstanceWid'] = task['signInstanceWid']
    form['longitude'] = user['lon'] + rand_lon
    form['latitude'] = user['lat'] + rand_lat
    form['isMalposition'] = 1
    form['uaIsCpadaily'] = True
    ################这个参数一定不能穿帮！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    form['abnormalReason'] = user['abnormalReason']
    form['position'] = user['address']
    # TODO 这个参数的名称有待考究 需要抓包见分晓！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    return form


# 上传图片到阿里云oss
def uploadPicture(session, image, apis):
    url = 'https://{host}/wec-counselor-sign-apps/stu/sign/getStsAccess'.format(host=apis['host'])
    res = session.post(url=url, headers={'content-type': 'application/json'}, data=json.dumps({}), verify=not debug)
    datas = res.json().get('datas')
    fileName = datas.get('fileName')
    accessKeyId = datas.get('accessKeyId')
    accessSecret = datas.get('accessKeySecret')
    securityToken = datas.get('securityToken')
    endPoint = datas.get('endPoint')
    bucket = datas.get('bucket')
    bucket = oss2.Bucket(oss2.Auth(access_key_id=accessKeyId, access_key_secret=accessSecret), endPoint, bucket)
    with open(image, "rb") as f:
        data = f.read()
    bucket.put_object(key=fileName, headers={'x-oss-security-token': securityToken}, data=data)
    res = bucket.sign_url('PUT', fileName, 60)
    # log(res)
    return fileName


# 获取图片上传位置
def getPictureUrl(session, fileName, apis):
    url = 'https://{host}/wec-counselor-sign-apps/stu/sign/previewAttachment'.format(host=apis['host'])
    data = {
        'ossKey': fileName
    }
    res = session.post(url=url, headers={'content-type': 'application/json'}, data=json.dumps(data), verify=not debug)
    photoUrl = res.json().get('datas')
    return photoUrl


# DES加密
def DESEncrypt(s, key='b3L36XNL'):
    key = key
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(s)
    # print(encrypt_str)
    print(f'加密结束的内容为：{base64.b64encode(encrypt_str).decode()}')
    return base64.b64encode(encrypt_str).decode()


# 提交签到任务
def submitForm(session, user, form, apis):
    user = user['user']
    # Cpdaily-Extension
    extension = {
        "lon": user['lon'] + rand_lon,
        "model": uanalyse.ua2model(user['ua']),
        "appVersion": "8.2.17",
        "systemVersion": uanalyse.ua2androidver(user['ua']),
        "userId": user['username'],
        "systemName": "android",
        "lat": user['lat'] + rand_lat,
        "deviceId": str(uuid.uuid1())
    }

    headers = {
        'tenantId': 'henu',
        'User-Agent': user['ua']+' okhttp/3.12.4',
        'CpdailyStandAlone': '0',
        'extension': '1',
        'Cpdaily-Extension': DESEncrypt(json.dumps(extension)),
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip',
        # 'Host': 'swu.cpdaily.com',
        'Connection': 'Keep-Alive'
    }
    print(extension)
    print(headers)
    #print('程序还有一步就提交了，已暂停')
    #exit(888)
    # TODO 设置提交锁的位置
    res = session.post(url='https://{host}/wec-counselor-sign-apps/stu/sign/submitSign'.format(host=apis['host']),
                       headers=headers, data=json.dumps(form))
    message = res.json()['message']
    if message == 'SUCCESS':
        log('自动签到成功')
        sendMessage('自动签到成功', user)
    else:
        log('自动签到失败，原因是：' + message)
        sendMessage('自动签到失败' + message, user)
        # sendMessage('自动签到失败，原因是：' + message, user['email'])
        exit(-1)


# 发送邮件通知
def sendMessage(msg, user, title=getTimeStr() + '今日校园自动签到结果通知'):
    if msg.count("未开始") > 0:
        return ''
    print(user)
    try:
        if user['useserverchan'] != 0:
            log('正在发送微信通知')
            log(getTimeStr())
            #               sendMessageWeChat(msg + getTimeStr(), '今日校园自动签到结果通知')
            notification.send_serverchan(user['serverchankey'], title, msg)
    except Exception as e:
        log("send failed")


# 主函数
def main():
    for user in config['users']:
        print(user)

        apis = getCpdailyApis(user)
        session = getSession(user, apis)
        getUnSignedTasksAndSign(session, apis, user)


# 提供给腾讯云函数调用的启动函数
def main_handler(event, context):
    try:
        main()
    except Exception as e:
        raise e
    else:
        return 'success'


if __name__ == '__main__':
    # print(extension)
    print(main_handler({}, {}))
