def send_serverchan(skey, title, content):
    from lightpush import lightpush
    lgp = lightpush()
    lgp.set_single_push(key=skey)
    try:
        lgp.single_push(title, content)
        print("success")
    except Exception as e:
        print("e")
#send_serverchan('','test','test')