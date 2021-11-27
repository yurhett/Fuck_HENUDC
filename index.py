import random
import time

import yaml
from todayLoginService import TodayLoginService
from actions.autoSign import AutoSign
from actions.collection import Collection
from actions.workLog import workLog
from actions.sleepCheck import sleepCheck
from actions.sendMsg import qmsgpush

def randomPosition(ak, lon, lat):
    import requests
    url = "https://api.map.baidu.com/reverse_geocoding/v3/"
    params = {
        "location": str(lat)+','+str(lon),
        "output": "json",
        "ak": ak,
        "coordtype": "bd09ll"
    }
    try:
        res = requests.get(url, params=params)
        temp = res.json()
        return temp['result']['formatted_address']
    except:
        return None


def getYmlConfig(yaml_file='config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)


def main():
    adminmsg = ''
    config = getYmlConfig()
    for user in config['users']:
        lgp = qmsgpush()
        lgp.set_single_push(key=user['user']['qmsg'],qq=user['user']['qq'])
        user['user']['baidumap'] = config['baidumap']
        if config['debug']:
            # 公用变量嵌入在此处
            msg = working(user)
        else:
            try:
                msg = working(user)
            except Exception as e:
                msg = str(e)
        adminmsg = adminmsg + '\n' + f'[INFO]{user["user"]["nickname"]} 的今日校园自动签到' + msg
        lgp.single_push(f'[INFO]{user["user"]["nickname"]}您好，学号为 {user["user"]["username"]} 的今日校园自动签到', msg)
        print(msg)
        time.sleep(random.randint(3,5))
    lgp = qmsgpush()
    lgp.set_single_push(key=config['users'][0]['user']['qmsg'], qq='1216518776')
    lgp.single_push(f'您好管理员，这是您的管理通知：\n', adminmsg)


def working(user):
    rand_lon = str(random.randint(0, 999)).zfill(3)
    rand_lat = str(random.randint(0, 999)).zfill(3)
    format(float(user['user']['lon']), '.2f')
    tmp_lon = str(format(float(user['user']['lon']), '.3f')) + rand_lon
    tmp_lat = str(format(float(user['user']['lat']), '.3f')) + rand_lat
    tmp_pos = randomPosition(user['user']['baidumap'],tmp_lon,tmp_lat)
    if tmp_pos is not None:
        user['user']['lon'] = tmp_lon
        user['user']['lat'] = tmp_lat
        user['user']['address'] = tmp_pos
    else:
        rand_lon = str(random.randint(0, 9))
        rand_lat = str(random.randint(0, 9))
        user['user']['lon'] = str(user['user']['lon']) + rand_lon
        user['user']['lat'] = str(user['user']['lat']) + rand_lat

    today = TodayLoginService(user['user'])
    today.login()
    # 登陆成功，通过type判断当前属于 信息收集、签到、查寝
    # 信息收集
    if user['user']['type'] == 0:
        # 以下代码是信息收集的代码
        collection = Collection(today, user['user'])
        collection.queryForm()
        collection.fillForm()
        msg = collection.submitForm()
        return msg
    elif user['user']['type'] == 1:
        # 以下代码是签到的代码
        sign = AutoSign(today, user['user'])
        sign.getUnSignTask()
        sign.getDetailTask()
        sign.fillForm()
        msg = sign.submitForm()
        return msg
    elif user['user']['type'] == 2:
        # 以下代码是查寝的代码
        check = sleepCheck(today, user['user'])
        check.getUnSignedTasks()
        check.getDetailTask()
        check.fillForm()
        msg = check.submitForm()
        return msg
    elif user['user']['type'] == 3:
        # 以下代码是工作日志的代码
        work = workLog(today, user['user'])
        work.checkHasLog()
        work.getFormsByWids()
        work.fillForms()
        msg = work.submitForms()
        return msg
# 阿里云的入口函数
def handler(event, context):
    main()


# 腾讯云的入口函数
def main_handler(event, context):
    main()
    return 'ok'


if __name__ == '__main__':
    main()
