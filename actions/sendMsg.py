import warnings
import requests


class qmsgpush(object):
    single_push_url = "https://qmsg.zendee.cn/send"
    single_push_key = ''
    single_push_qq = ''
    group_push_url = "https://qmsg.zendee.cn/group"
    group_push_key = ''
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    def set_single_push(self, key, qq, url=None):
        self.single_push_key = key
        if qq:
            self.single_push_qq = qq
        if url:
            self.single_push_url = url

    def set_group_push(self, key, url=None):
        self.group_push_key = key
        if url:
            self.group_push_url = url

    def _get_msg(self, title=None, content=None):
        if title is None:
            raise TypeError("Requires a string format title to push.")
        elif content is None:
            warnings.warn("Did not input content.", Warning)

        msg = {'qq': self.single_push_qq,
            'msg': title + '\n' + content}

        return msg

    def single_push(self, title=None, content=None):
        msg = self._get_msg(title,content)
        r = requests.post('%s/%s' % (self.single_push_url, self.single_push_key), data=msg, headers= self.header)
        return r

    def group_push(self, title=None, content=None):
        msg = self._get_msg(title,content)
        r = requests.post("%s/%s"%(self.group_push_url,self.group_push_key), data=msg, headers= self.header)
        return r

    def push(self, title=None, content=None, mode='single'):
        if mode == 'single':
            return self.single_push(title,content)
        elif mode == 'group':
            return self.group_push(title,content)
        else:
            raise ValueError("Please choose mode from single or group.")

