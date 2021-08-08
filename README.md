# FUCK_HENUDC

#### 20210808 更新新功能，让您每天的坐标都小范围变化。

#### 20210723 已适配最新版本

### 使用方法：

#### 0.（懒人）点右上角的FORK，fork到你的仓库里

注意：这个方法会导致你配置的yml别人也能下到，不怕别人知道你学号的上

#### 0.（安全）打开你自己的GitHub首页，新建项目并克隆我的源码。小白请按照：https://github.com/yurhett/Fuck_HENUDC/tree/main/doc

#### 1.收集信息

- #### 验证你的河大账号和密码：[点击链接](https://ids.henu.edu.cn/)并用你的学号登录，记住你登陆成功的学号和密码。

- #### 确认你的地址：[点击链接](https://lbs.qq.com/tool/getpoint/index.html)并选择你经常签到的地址。如：34.810703,114.369221（请不要填写这个坐标，经测试，相对偏移较大） 河南省开封市顺河回族区琢玉路，然后[点击链接](http://api.map.baidu.com/lbsapi/getpoint/index.html)选择刚才的点位，获得坐标，如：114.376956,34.820271。

- #### 记录你的qmsg key：[点击链接](https://qmsg.zendee.cn/)微信登录后复制您的SCKEY代码

- #### 安卓手机额外步骤，为了使用您自己的UA不被发现，您可以在安卓手机上用今日校园APP扫描以下二维码：

  ![image](./doc/qrcode.png)

  #### 复制生成的文字，注意，粘贴时请不要粘贴文字尾部的：cpdaily/8.2.17 wisedu/8.2.17
  
  #### 特殊步骤：您可以到 [https://lbsyun.baidu.com/apiconsole/key#/home](https://lbsyun.baidu.com/apiconsole/key#/home) 创建浏览器端应用，然后复制您的ak

#### 2.编辑config.yml

```yaml
#调试是改为true将可以在控制台定位报错信息
debug: false
#百度地图ak
baidumap:
users:

  - user:
      #别名，多用户的时候用于区分用户
      nickname: '我的名字'
      #类型请勿更改
      type: 1
      #qmsg KEY 请到：https://qmsg.zendee.cn/me.html 了解更多信息
      qmsg: '这里填写你的qmsgkey'
      #收信人QQ
      qq: '这里填写你的收信QQ'
      #学校全称，仅支持河南大学
      schoolName: '河南大学'
      #学号或者工号
      username: '这里填写你的学号'
      #密码
      password: '这里填写你的密码'
      #您的UA，可以通过二维码获取（仅限安卓用户），这是区别您和他人的重要一步，但实际上服务器并不会拿UA作为判断依据，所以懒人可以直接用我的
      ua: 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Plus Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36'
      #地址信息
      #附上经纬度查询地址（请自行选择自己的学校地址，address，lon，lat都要填查询到的）：http://api.map.baidu.com/lbsapi/getpoint/index.html
      address: '河南省开封市顺河回族区塔云路'
      #lon 经度，一定要精确到小数点后5位
      lon: 114.37695
      #lat 纬度，一定要精确到小数点后5位
      lat: 34.82027
      #填写表单时判断是否与您预设的一一对应，不对应就会报错，建议开启
      checkTitle: 1
      #在校内填0，在校外填1
      isMalposition: 1
      #反馈信息，不要填
      abnormalReason:
      #表单信息，目前的信息和河南大学签到的内容一致
      forms:
        - form:
            title: 1. 暑假期间，本人身体健康状况是否良好 (必填)
            value: 是
        - form:
            title: 2. 暑假期间，与本人共同居住者身体健康状况是否良好 (必填)
            value: 是
        - form:
            title: 3. 暑假期间，是否有中高风险地区旅居史 (必填)
            value: 否
        - form:
            title: 4. 暑假期间，是否接触过确诊病例或无症状感染者 (必填)
            value: 否
        - form:
            title: 5. 本人是否承诺以上所填信息真实有效，自愿承担因隐瞒不报产生的一切后果 (必填)
            value: 是


#将以上的 - user再复制一遍可以定义多个用户
```

#### 3.鸣谢：

#### 感谢[@thriving123](https://gitee.com/thriving123) 提供的过程和源代码，本项目就是在他的[fuckTodayStudy](https://gitee.com/thriving123/fuckTodayStudy)基础上简单修改而来，有空帮他点个star吧~

##### 旧版本：感谢[@ZimoLoveShuang](https://github.com/ZimoLoveShuang) 提供80%的过程和源代码，本项目就是在他的[auto-sign](https://github.com/ZimoLoveShuang/auto-sign)基础上简单修改而来，有空帮他点个star吧~