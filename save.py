import sys

def empty_update(res):
    remotelogs = res[res.index("remotelogs")+13: res.index('","logs":') ]
    try:
        rl_content = remotelogs[ remotelogs.index('content":"[')+12:-3 ]
    except:
        rl_content = None

    locallogs = res[ res.index('","logs"')+12:-2 ]
    try:
        ll_content = locallogs[ locallogs.index('content":"[')+12: ]
    except:
        ll_content = None

    #print(f"{remotelogs} == {rl_content} == {locallogs} == {ll_content}")
    new_evt = False

    if rl_content:
        new_evt = True
        first=True
        while True:
            if len(rl_content) < 2:
                break
            if rl_content[1] != ',' and not first:
                break
            first = False if first else None
            blk = rl_content[ :rl_content.index("}")+1 ]
            print(blk)
            data = processBlk(blk)
            newLog('remote', data)
            rl_content = rl_content[len(blk):]

    if ll_content:
        new_evt = True
        first=True
        while True:
            if len(ll_content) < 2:
                break
            if ll_content[1] != ',' and not first:
                break
            first = False if first else None
            blk = ll_content[ :ll_content.index("}")+1 ]
            print(blk)
            data = processBlk(blk)
            newLog('local', data)
            ll_content = ll_content[len(blk):]

    return new_evt


def processBlk(blk):
    try:
        blk_id = blk[ blk.find('"id":')+5:blk.find(',"entry"') ]
    except:
        blk_id = None

    try:
        blk_type = blk[ blk.find('</i>&nbsp;<b>')+13:blk.find("<br>") ]
    except:
        blk_type = None

    try:
        if blk.find("this.innerHTML = '") != -1:
            blk_ip = blk[ blk.index("this.innerHTML = '")+18:blk.find("'; }") ]
        else:
            blk_ip = blk[ blk.index('plug" aria-hidden="true"></i>&nbsp;')+35: blk.index('</span>","level')]
    except:
        blk_ip = None

    try:
        blk_lvl = blk[ blk.index('level')+7:blk.index(',"logged"') ]
    except:
        blk_lvl = None

    try:
        blk_ts = blk[ blk.index('logged')+8:-1 ]
    except:
        blk_ts = None

    return { \
        'id': blk_id, \
        'type': blk_type, \
        'ip': blk_ip, \
        'lvl': blk_lvl, \
        'ts': blk_ts \
    }

def newLog(whr, data):
    if whr == 'remote':
        prechr = "r>> "
    else:
        prechr = "l<< "
    sys.stdout.write("\n{}----------------------------\n".format(prechr))
    sys.stdout.write("{}!New Log!\n".format(prechr))
    sys.stdout.write("{}Id: {}\n".format(prechr, data["id"]))
    sys.stdout.write("{}Type: {}\n".format(prechr, data["type"]))
    sys.stdout.write("{}Ip: {}\n".format(prechr, data["ip"]))
    sys.stdout.write("{}Lvl: {}\n".format(prechr, data["lvl"]))
    sys.stdout.write("{}Ts: {}\n".format(prechr, data["ts"]))
    sys.stdout.write("{}----------------------------\n\n".format(prechr))
    sys.stdout.flush()