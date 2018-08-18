#!/usr/bin/python3
 
 
import sys
import requests
import time
import random
import json
import threading

from slave_api import SlaveApi
 
Cookie="80pa65mjbisg3a8ilj4ee97440" # set your cookie heres
UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.77 Safari/537.36"
very='cvvw45yvj' # Normally doesn't change
csrf='cdcd5f7a980bea956416c0e3e5e77ff8' # get your token in the html or request header
PAUSE = 0.8
ANTIBAN_PAUSE = 4
MIN_MISSION = 5
MAX_MISSION =10

def game_loop(sApi,player_data):
    while True:
            pass
            #lancer la mission
            mission_id = random.randint(MIN_MISSION,MAX_MISSION)
            mission = sApi.start_mission(mission_id).replace('\\','')
            print('-- Mission --')
            print(mission)
            print('-------------')
            mission_content = mission[mission.index('"content":"')+11:-2]
            mission_data = json.loads(mission_content)
            current_mission = mission_data[0]
            print('starting mission %s' %(current_mission['id']))
            #la victime n'est pas dans mes slaves ?
            already_slave = False
            for slave in player_data['npc_slaves']:
                if (slave['ip'] == current_mission['target']):
                    print("target (%s) is already a slave ... "%current_mission['target'])
                    already_slave = True
                    break
            if not already_slave:
                print("target (%s) is not a slave ... pulse it"%current_mission['target'])
                #faire un pulse
                pulse = sApi.pulse(current_mission['target']).replace('\\','')
                process_id = pulse[pulse.find('terminal_process_')+17:-13]
                print('pulse -> process id %s'%process_id)
                while True:
                    processes = sApi.get_processes().replace('\\','').replace('"[{"','[{"').replace('"}]"','"}]')
                    if 'content":"[]"' in processes:
                        time.sleep(1)
                        continue
                    processes_content = processes[processes.index('"content":')+10:-2]
                    print('-- processes concent (pulse)')
                    print(processes_content)
                    print('--------------------------')
                    processes_data_tab = json.loads(processes_content)
                    processes_data = None
                    for process in processes_data_tab:
                        if str(process_id) == str(process['pid']):
                            processes_data = process
                            break
                    if processes_data is None or str(process_id) != str(processes_data['pid']):
                        time.sleep(1)
                    else:
                        break
                #attendre
                print("waiting %s s for adding slave %s"%(processes_data['timeleft'],current_mission['target']))
                time.sleep(int(processes_data['timeleft'])+1)
                #accepter
                print('adding slave !')
                print(sApi.end_process(processes_data['pid']))
                time.sleep(1)
                print('updating slaveslist ...')
                slaveslist = sApi.slaveslist().replace('\\','')
                slaveslist_content = slaveslist[slaveslist.index('"content":"')+11:-2]
                slaveslist_data = json.loads(slaveslist_content)
                player_data['npc_slaves'] = slaveslist_data['npcs']
            
            #se connecter
            connect(sApi,current_mission['target'])
            #supprimer le fichier nécessaire
            print('send command to remove file %s'%current_mission['expect'])
            remove_file = sApi.remove_file(current_mission['expect']).replace('\\','')
            print(remove_file)
            r_process_id = remove_file[remove_file.find('terminal_process_')+17:-13]
            while True:
                processes = sApi.get_processes().replace('\\','').replace('"[{"','[{"').replace('"}]"','"}]')
                print(processes)
                if 'content":"[]"' in processes:
                    time.sleep(1)
                    continue
                print('-- processes (remove)')
                print(processes)
                print('--------------------------')                
                processes_content = processes[processes.index('"content":')+10:-2]
                print('-- process concent (remove)')
                print(processes_content)
                print('--------------------------')
                processes_data_tab = json.loads(processes_content)
                processes_data = None
                for process in processes_data_tab:
                    if str(r_process_id) == str(process['pid']):
                        processes_data = process
                        break
                if processes_data is None or str(r_process_id) != str(processes_data['pid']):
                    time.sleep(1)
                else:
                    break
            #attendre
            print("waiting %s s for removing file %s"%(processes_data['timeleft'],current_mission['expect']))
            time.sleep(int(processes_data['timeleft'])+1)
            #valider
            sApi.end_process(processes_data['pid'])
            time.sleep(1)
            #valider la mission
            sApi.end_mission(current_mission['id'])
            print('Ending mission %s'%(current_mission['id']))
            print('exit remote connection')
            print(sApi.exit_connection())
            print(sApi.notifications())
            print('pausing a bit ... not souspicious ... plz do not ban')
            time.sleep(ANTIBAN_PAUSE)

def update_loop(sApi,player_data):
    while True:
        update_data = sApi.update().replace("\\",'')
        threading.Thread(target=analyze_update,args=(sApi,update_data,player_data)).start()
        time.sleep(PAUSE)

def analyze_update(sApi,update_data,player_data):
    remote_logs = local_logs = None
    remote_logs,local_logs = get_logs(update_data)
    
    if remote_logs is not None:
        remote_data = parse_remote_content(remote_logs)
        if remote_data['id'] != '':
            if remote_data['ip'] == player_data['local_ip']:
                print('--- REMOVING REMOTE LOG ---')
                print(sApi.remove_remote_log(int(remote_data['id'])))
                print('---------------------------')

    if local_logs is not None:
        local_data = parse_local_content(local_logs)
        if local_data['id'] != '':
            print(sApi.remove_log(int(local_data['id'])))   

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
    remotelogs = update_data[update_data.index("remotelogs")+13: update_data.index('","logs":') ]
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
 
def main():
    mission,slaves = new_delete_mission(sApi)
    for slave in slaves:
        if slave['ip'] is not mission['target']:
            sApi.pulse(slave['ip'])
            # attendre que le password soit connu
            # envoyer la requête pour accepter
    connect(sApi,slave['ip'])
 

 
def new_delete_mission(api):
    mission_data_full = json.loads(api.start_mission(1))
    mission_data = json.loads(json.loads(mission_data_full['content'])[0])
    print(mission_data)

    api.notifications()
    api.finances()
    api.player()
    slaves = json.loads(api.slaveslist())
    slaves_npc = json.loads(json.loads(slaves['content'])['npc'])
    return mission_data,slaves_npc

def connect(api,ip):
    while True:
        print('connecting to %s ...'%ip)
        connect_remote = api.connect_remote(ip)
        print(connect_remote)
        if 'Love Succs' in connect_remote:
            print('detected "Love Succs", reconnecting to %s'%ip)
            time.sleep(1)
        else:
            break


    api.slaveslist()

    print('scanning ...')
    print(api.scan())

    api.inventory()

    api.notifications()
    print('connected to %s'%ip)


def end_mission(api,mission_id):
    res = json.loads(api.end_mission(mission_id))
    return res['status']

def launch_game(sApi):
    session_remote = sApi.session_remote().replace('\\','')
    remote_ip = session_remote[session_remote.index('":"["')+6:session_remote.index('"]"')]

    sApi.defense()
    sApi.get_logs()
    sApi.powerups()
    sApi.get_activity()

    player = sApi.player().replace('\\','')
    player_content = player[player.index('"content":"{')+11:-2]
    player_data = json.loads(player_content)

    sApi.get_missions()
    sApi.get_chat()
    sApi.get_processes()

    slaveslist = sApi.slaveslist().replace('\\','')
    slaveslist_content = slaveslist[slaveslist.index('"content":"{')+11:-2]
    slaveslist_data = json.loads(slaveslist_content)

    sApi.notifications()
    sApi.get_files()
    sApi.update()
    sApi.notifications()
    finances = sApi.finances().replace('\\','').replace('"[{"','[{"').replace('"}]"','"}]')
    finances_content = finances[finances.index('"content":"{')+11:-2]
    finances_data = json.loads(finances_content)
    return {
        'username': player_data['player_info']['username'],
        'local_ip': player_data['player_info']['ip'],
        'remote_ip': remote_ip,
        'dollars': finances_data['accounts']['total'],
        'btc': finances_data['accounts']['totalbtc'],
        'npc_slaves': slaveslist_data['npcs'],
        'player_slaves': slaveslist_data['players']
    }

if __name__=='__main__':
    sApi = SlaveApi(Cookie,csrf,very,UserAgent)
    player_data = launch_game(sApi)
    print('Welcome, %s. Your infos are:'%player_data['username'])
    try:
        game_thread=threading.Thread(target=game_loop,args=(sApi,player_data))
        game_thread.start()

        update_thread=threading.Thread(target=update_loop,args=(sApi,player_data))
        update_thread.start()
    except:
        print ("Error: unable to start thread")

    while 1:
        pass