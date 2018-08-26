#!/usr/bin/python3
 
 
import time
import random
import json
import threading
import configparser
from slave_api import SlaveApi
from math import fabs
 
config = configparser.ConfigParser()
config.read('configuration.ini')

Cookie=str(config['DEFAULT']['Cookie'])
UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.77 Safari/537.36'
very=str(config['DEFAULT']['very'])
csrf=str(config['DEFAULT']['csrf'])

PAUSE_UPDATE = float(config['DEFAULT']['PAUSE_UPDATE'])
ANTIBAN_PAUSE = float(config['DEFAULT']['ANTIBAN_PAUSE'])
FORMAT_TIMER = int(config['DEFAULT']['FORMAT_TIMER'])
PAUSE_RANSOM = int(config['DEFAULT']['PAUSE_RANSOM'])
BTC_FEES_PERCENT = float(config['DEFAULT']['BTC_FEES_PERCENT'])

def start_delete_mission(sApi,mission_id):
    mission = sApi.start_mission(mission_id).replace('\\','')
    mission_content = mission[mission.index('"content":"')+11:-2]
    mission_data = json.loads(mission_content)
    current_mission = mission_data[0]

    print('Starting mission %s:' % current_mission['id'])
    print('\tSubject\t: %s' % current_mission['subject'])
    print('\tTarget\t: %s' % current_mission['target'])
    print('\tFile\t: %s' % current_mission['expect'])
    print('\tPayout\t: %s$' % current_mission['payout'])
    print('-------------------------\n')
    return current_mission

def target_is_slave(npc_slaves,target_ip):
    for slave in npc_slaves:
        if (slave['ip'] == target_ip):
            print("Target (%s) is already a slave." % target_ip)
            return True
    return False

def end_process(pid,process_name):
    sApi.end_process(pid)
    print("Process %s (%s) has been terminated"%(process_name,pid))

def get_process_data(sApi,process_id):
    while True:
        processes = sApi.get_processes().replace('\\','').replace('"[{"','[{"').replace('"}]"','"}]')
        if 'content":"[]"' in processes:
            time.sleep(1)
            continue
        processes_content = processes[processes.index('"content":')+10:-2]
        processes_data_tab = json.loads(processes_content)
        processes_data = None
        [{"pid":1933933,"processnum":134,"processname":"Deleting","type":"CPU","object":"29dc2e22d.zip (20.8)","targetip":"150.120.26.74","timestart":"2018-08-18 10:47:27","timetotal":"8.9","timeleft":7.9,"percent":"11.24","done":0}]
        for process in processes_data_tab:
            if str(process_id) == str(process['pid']):
                print("Found a process id matching (%s):"%process_id)
                print("\tName\t\t: %s"%process['processname'])
                print("\tType\t\t: %s"%process['type'])
                print("\tObject\t\t: %s"%process['object'])
                print("\tTarget\t\t: %s"%process['targetip'])
                print("\tTime Left\t: %s"%process['timeleft'])
                print('-------------------------')
                processes_data = process
                return processes_data
        if processes_data is None or str(process_id) != str(processes_data['pid']):
            time.sleep(1)
        else:
            return processes_data

def launch_and_validate_pulse(sApi,current_mission):
    pulse = sApi.pulse(current_mission['target']).replace('\\','')
    process_id = pulse[pulse.find('terminal_process_')+17:-13]
    print('Launched a pulse. Process id = %s'%process_id)
    processes_data = get_process_data(sApi,process_id)
    time_left = float(processes_data['timeleft'])
    process_name = processes_data['processname']
    #attendre
    print("Waiting %ds (%s). Target: %s"%(time_left,process_name,processes_data['targetip']))
    time.sleep(fabs(time_left+1.0))
    #accepter
    end_process(processes_data['pid'],process_name)
    time.sleep(1)

def clear_remote_logs(sApi,local_ip):
    logs = sApi.get_terminal_logs().replace('\\\\\\"',"'").replace('\\\\\\/','').replace('\\','')\
                                .replace('"{','{').replace('}"','}')
    logs_data = json.loads(logs)
    for log in logs_data['content']['logs']:
        if local_ip in log['entry']:
            print('Found a log with our IP (%s) in remote logs. Removing it.'%local_ip)
            sApi.remove_remote_log(log['id'])

def launch_and_validate_remove(sApi,current_mission,player_data):
    remove_file = sApi.remove_file(current_mission['expect']).replace('\\','')
    process_id = remove_file[remove_file.find('terminal_process_')+17:-13]
    print('Sent command to remove file %s'%current_mission['expect'])
    processes_data = get_process_data(sApi,process_id)
    time_left = float(processes_data['timeleft'])
    process_name = processes_data['processname']
    #attendre
    print("Waiting %ds (%s). Target: %s"%(time_left,process_name,processes_data['targetip']))
    time.sleep(fabs(time_left+1.0))
    #accepter
    end_process(processes_data['pid'],process_name)
    clear_remote_logs(sApi,player_data)
    time.sleep(1)

def update_slavelists(sApi):
    print('Updating slaveslist')
    slaveslist = sApi.slaveslist().replace('\\','')
    slaveslist_content = slaveslist[slaveslist.index('"content":"')+11:-2]
    return json.loads(slaveslist_content)

def validate_mission(mission_id):
    print('Ending mission %s'%mission_id)
    status = sApi.end_mission(mission_id)
    print("\tStatus: %s"%status)
    print('-------------------------')

def get_remote_logs(update_data):
    remotelogs = update_data[update_data.index("remotelogs")+13: update_data.index('","logs":')]
    try:
        content = remotelogs[remotelogs.index('content":"[')+12:-3 ]
    except:
        content = None
    return content

def get_local_logs(update_data):
    locallogs = update_data[update_data.index('","logs":')+12:-2 ]
    try:
        content = locallogs[locallogs.index('content":"[')+12:-3]
    except:
        content = None
    return content    

def analyze_update(sApi,update_data,player_data,harddrive_data):
    #remote_logs = local_logs = None
    #remote_logs,local_logs = get_logs(update_data)
    if not '"remotelogs":"{"status":"error"' in update_data:
        #remove remote logs
        remote_logs = get_remote_logs(update_data)
        remote_data = parse_remote_content(remote_logs)
        if remote_data['id'] != '':
            if remote_data['ip'] == player_data['local_ip']:
                print('--- REMOVING REMOTE LOG ---')
                remote_log_res = sApi.remove_remote_log(remote_data['id'])
                if  remote_log_res != '{"status":"success","content":"[]"}':
                    print("\tRemote logs are not empty, checking all logs IP")
                    remote_logs_parsed = remote_log_res.replace('\\\\\\"',"'").replace('\\\\\\/','').replace('\\','')\
                                                    .replace('"[{','[{').replace('}]"}','}]}')
                    remote_log_json = json.loads(remote_logs_parsed)
                    for log in remote_log_json['content']:
                        if player_data['local_ip'] in log['entry']:
                            print('\tFound player ip (%s) in a log. Removing it.'% player_data['local_ip'])
                            sApi.remove_remote_log(log['id'])
                else:
                    print(remote_data)
                print('-------------------------')
    if not ',"logs":"{"status":"error"' in update_data:
        #remove local logs
        local_logs = get_local_logs(update_data)
        local_data = parse_local_content(local_logs)
        if local_data['id'] != '':
            print('--- REMOVING LOCAL LOG ---')
            local_log_res = sApi.remove_log(local_data['id'])
            if  local_log_res != '{"status":"success","content":"[]"}':
                print("\tLocal logs are not empty, formating")
                sApi.format_logs()
            else:
                print(local_data)
            print('-------------------------')
            if ((local_data['type'] == 'Authentication') and (local_data['level'] == '3')):
                print('SUSPICIOUS LOG DETECTED !')
                print(local_data)
                harddrive_data['format_harddrive'] = True
                print('Suspicious log has been detected. Harddrive will be formatted every %ds.'%FORMAT_TIMER)
                print('-------------------------')
    harddrive_data['compteur'] += 1
    if harddrive_data['compteur'] > FORMAT_TIMER and harddrive_data['format_harddrive']:
        print('Suspicious log had been detected. Formating.')
        sApi.format_harddrive()
        harddrive_data['compteur'] = 0

def process_log_content(blk):
    try:
        blk_id = blk[blk.find('"id":')+5:blk.find(',"entry"') ]
    except:
        blk_id = None

    try:
        blk_type = blk[ blk.find('</i>&nbsp;<b>')+13:blk.find("</b>") ]
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
        blk_lvl = blk[ blk.index('level')+7:blk.index(',"logged"')]
    except:
        blk_lvl = None

    try:
        if blk.endswith('}]"'):
            blk_ts = blk[blk.index('logged')+8:-3]
        else:
             blk_ts = blk[blk.index('logged')+8:-1]
    except:
        blk_ts = None

    return { \
    'id': blk_id, \
    'type': blk_type, \
    'ip': blk_ip, \
    'level': blk_lvl, \
    'timestamp': blk_ts \
    }

def parse_remote_content(remote_logs):
    data = process_log_content(remote_logs)
    return data

def parse_local_content(local_logs):
    data = process_log_content(local_logs)
    return data

def get_logs(update_data):
    remotelogs = update_data[update_data.index("remotelogs")+13: update_data.index('","logs":')]
    try:
        rl_content = remotelogs[remotelogs.index('content":"[')+12:-3 ]
    except:
        rl_content = None

    locallogs = update_data[update_data.index('","logs":')+12:-2 ]
    try:
        ll_content = locallogs[locallogs.index('content":"[')+12:-3]
    except:
        ll_content = None
    return rl_content,ll_content

def connect(api,ip,local_ip):
    while True:
        print('Connecting to %s ...'%ip)
        connect_remote = api.connect_remote(ip)
        if 'Love Succs' in connect_remote:
            print('\tDetected "Love Succs", reconnecting to %s'%ip)
            time.sleep(1)
        else:
            connect_data = connect_remote[connect_remote.find('Accessing '):connect_remote.find('<script>')]
            print('\t'+connect_data)
            clear_remote_logs(api,local_ip)
            break

    print('Scanning %s'%ip)
    scan = api.scan().replace('\\','')
    scan_result = scan[scan.find('"{"action":"')+12:scan.find('<script>')]
    print('\t%s'%scan_result)


def end_mission(api,mission_id):
    res = json.loads(api.end_mission(mission_id))
    return res['status']

def launch_game(sApi):
    session_remote = sApi.session_remote().replace('\\','')
    remote_ip = session_remote[session_remote.index('":"["')+6:session_remote.index('"]"')]

    player = sApi.player().replace('\\','')
    player_content = player[player.index('"content":"{')+11:-2]
    player_data = json.loads(player_content)

    slaveslist = sApi.slaveslist().replace('\\','')
    slaveslist_content = slaveslist[slaveslist.index('"content":"{')+11:-2]
    slaveslist_data = json.loads(slaveslist_content)

    finances = sApi.finances().replace('\\','').replace('"[{"','[{"').replace('"}]"','"}]')
    finances_content = finances[finances.index('"content":"{')+11:-2]
    finances_data = json.loads(finances_content)
    return {
        'username': player_data['player_info']['username'],
        'local_ip': player_data['player_info']['ip'],
        'level': int(player_data['player_info']['level']),
        'remote_ip': remote_ip,
        'dollars': finances_data['accounts']['total'],
        'btc': finances_data['accounts']['totalbtc'],
        'npc_slaves': slaveslist_data['npcs'],
        'player_slaves': slaveslist_data['players']
    }

def process_notifications(sApi,player_data):
    notifications = json.loads(sApi.notifications())
    for notification in notifications['content']:
        if notification['title'] == 'Mission Completed':
            print(notification['message'])
        elif notification['title'] == 'You Just Leveled Up!':
            new_level = int(notification['message'].split(' ')[2])
            player_data['level'] = new_level
            print('Level up ! you are now level %s'%new_level)

def game_loop(sApi,player_data):
    while True:
            # chose a random mission_id to not be too previsible
            min = 1
            max = 1
            if player_data['level']<=10:
                min = 3
                max = 5
            else:
                min = 8
                max = 10
            mission_id = random.randint(min,max)
            #lancer la mission
            current_mission = start_delete_mission(sApi,mission_id)

            #la victime n'est pas dans mes slaves ?
            if not target_is_slave(player_data['npc_slaves'],current_mission['target']):
                print("Target (%s) is not in slaves list."%current_mission['target'])
                #faire un pulse, attendre et le valider
                launch_and_validate_pulse(sApi,current_mission)
                # update la liste des slaves
                player_data['npc_slaves'] = update_slavelists(sApi)['npcs']
            
            #se connecter sur la cible
            connect(sApi,current_mission['target'],player_data['local_ip'])

            # faire un rm, attendre et valider
            launch_and_validate_remove(sApi,current_mission,player_data['local_ip'])

            #valider la mission (terminée après le rm)
            validate_mission(current_mission['id'])

            # on quitte la connexion actuelle (remise à l'état initial)
            print('Exit remote connection (%s)'%current_mission['target'])
            sApi.exit_connection()
            # demande de notifs (client like)
            process_notifications(sApi,player_data)
            # pause de sécurité (pas obligée)
            print('Pause mission thread for %ds. Reason: antiban'%ANTIBAN_PAUSE)
            time.sleep(fabs(ANTIBAN_PAUSE))

def update_loop(sApi,player_data):
    harddrive_data = {
        'format_harddrive': False,
        'compteur': 0
    }
    while True:
        update_data = sApi.update().replace("\\",'')
        threading.Thread(target=analyze_update,args=(sApi,update_data,player_data,harddrive_data)).start()
        time.sleep(fabs(PAUSE_UPDATE))

def ransom_active(sApi):
    test = sApi.terminal_test().replace('\\','')
    return 'Access to your Terminal is being held for ransom' in test

def pay_ransomware(sApi):
    test = sApi.terminal_test().replace('\\','')
    amount_and_id = test[test.find('"text-warning">')+15:test.find('</span><br><br><b')]
    amount_and_id_split = amount_and_id.split(' ')
    amount= amount_and_id_split[1]
    id= amount_and_id_split[2]
    return sApi.terminal_pay_ransomware(amount,id)

def get_finances(sApi):
    finances_res = sApi.finances().replace('\\\\\\"','"').replace('"[{"','[{"').replace('"}]\\"','"}]')\
                                    .replace('"{\\"','{\\"').replace('\\','').replace('}}"}','}}}')
    print(finances_res)
    return json.loads(finances_res)['content']

def convert_cash_to_btc(sApi):
    finances = get_finances(sApi)
    btc_conversion = float(finances['accounts']['conversion'].replace(',',''))
    total_dollars = float(finances['accounts']['total'].replace(',',''))
    amount = float((total_dollars * (1-BTC_FEES_PERCENT))/btc_conversion)
    return sApi.buy_bitcoin(finances['accounts']['list'][0]['aid'],amount)

def ransom_loop(sApi):
    while  True:
        if ransom_active(sApi):
            print('A ransomware has been detected on local computer. Getting rid of it.')
            print('WE QUIT FOR THE MOMENT !')
            sys.exit()
            #print(convert_cash_to_btc(sApi))
            #time.sleep(1)
            #print(pay_ransomware(sApi))
        else:
            print('No ransomware were found on local computer.')
        time.sleep(fabs(PAUSE_RANSOM))

if __name__=='__main__':
    sApi = SlaveApi(Cookie,csrf,very)
    player_data = launch_game(sApi)
    print('Welcome, %s. Congratulation on your level %s !\nThe bot will launch shortly.'%(player_data['username'],player_data['level']))
    print('-------------------\n')
    try:
        game_thread=threading.Thread(target=game_loop,args=(sApi,player_data))
        game_thread.start()

        update_thread=threading.Thread(target=update_loop,args=(sApi,player_data))
        update_thread.start()

        ransom_thread = threading.Thread(target=ransom_loop,args=(sApi,))
        ransom_thread.start()
    except:
        print ("Error: unable to start thread")
    while True:
        try:
            pass
        except KeyboardInterrupt:
            print('Bye, %s'%player_data['username'])