import re


def list2str_withblank(raw_list):
    string = " ".join(i for i in raw_list)
    return string


def ua2androidver(ua):
    info_list = re.findall(r"[(](.*?)[)]", ua)
    for i in range(0, len(info_list)):
        tmp_info = info_list[i].split(';')
        # print(tmp_info)
        for j in range(0, len(tmp_info)):
            if 'Android' in tmp_info[j]:
                android_list = tmp_info[j].split(' ')
                for k in range(0, len(android_list)):
                    if 'Android' in android_list[k]:
                        android_ver = android_list[k + 1]
                        return android_ver


def ua2model(ua):
    tmp_blank = []
    info_list = re.findall(r"[(](.*?)[)]", ua)
    for i in range(0, len(info_list)):
        tmp_info = info_list[i].split(';')
        for j in range(0, len(tmp_info)):
            if 'Build' in tmp_info[j]:
                build_list = tmp_info[j].split(' ')
                for k in range(0, len(build_list)):
                    if build_list[k] == '':
                        tmp_blank.append(k)
                if tmp_blank:
                    for tmp in range(0, len(tmp_blank)):
                        del build_list[tmp_blank[tmp]]
                for k in range(0, len(build_list)):
                    if 'Build' in build_list[k]:
                        build_dest = k
                        return list2str_withblank(build_list[:build_dest])


def ua2sysver(ua):
    tmp_blank = []
    info_list = re.findall(r"[(](.*?)[)]", ua)
    for i in range(0, len(info_list)):
        tmp_info = info_list[i].split(';')
        for j in range(0, len(tmp_info)):
            if 'Build' in tmp_info[j]:
                build_list = tmp_info[j].split(' ')
                for k in range(0, len(build_list)):
                    if build_list[k] == '':
                        tmp_blank.append(k)
                if tmp_blank:
                    for tmp in range(0, len(tmp_blank)):
                        del build_list[tmp_blank[tmp]]
                for k in range(0, len(build_list)):
                    if 'Build' in build_list[k]:
                        build_dest = k
                        buildno_list = list2str_withblank(build_list[build_dest:]).split('/')
                        for m in (0, len(buildno_list)):
                            if 'Build' in buildno_list[m]:
                                return list2str_withblank(buildno_list[m + 1:])


def ua_check(ua, compare):
    if compare in ua:
        return True
    else:
        return False

# 以下代码可用作测试函数可用性
"""raw_ua = 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Redmi K20 Pro Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.7.12'
print(type(raw_ua))
print(ua2androidver(raw_ua))
print(ua2model(raw_ua))
print(ua2sysver(raw_ua))
"""