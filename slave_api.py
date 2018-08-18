import sys
import requests
import time
import random
import json

class SlaveApi():

    def __init__(self,cookie,csrf,very):
        self.cookie = cookie
        self.csrf = csrf
        self.very = very
        self.init()

    def init(self):
        self.post_headers = { \
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.77 Safari/537.36',
            'very': self.very,
            'csrf': self.csrf,
            'Server': 'Slavehack2',
            'Referer': 'https://www.slavehack2.com/',
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Host': 'www.slavehack2.com'
        }

    def update(self):
        post_data = 'action=update&data={"files":true,"remotelogs":true,"logs":true,"ftp":false}&data2={"files":{},"remotelogs":{"order":["id","desc"]},"logs":{"order":["id","desc"]},"ftp":{"remote":true}}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?update", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        #print('{}\n{}\n{}\n\n{}'.format(
        #   '-----------START-----------',
        #   p.method + ' ' + p.url,
        #   '\n'.join('{}: {}'.format(k, v) for k, v in p.headers.items()),
        #   p.body,
        #))
        s=requests.Session()
        return s.send(p).text

    def notifications(self):
        post_data = 'action=get&data={}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?notifications", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def finances(self):
        post_data = 'action=get&data={"accounts":true}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?finances", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def player(self):
        post_data = 'action=get&data={"data":["all"]}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?player", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def slaveslist(self):
        post_data = 'action=get&data={"get":true}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?slaveslist", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def session_ip(self):
        post_data = 'action=get&data={"ip":true}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?session", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def session_remote(self):
        post_data = 'action=get&data={"connected":true}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?session", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def alerts(self):
        post_data = 'action=get&data={}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?alerts", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def powerups(self):
        post_data = 'action=get&data={"check":"activated"}'
        
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?powerups", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def start_mission(self,mission_id):
        post_data = 'action=get&data={"make":"[\\"'+str(mission_id)+'\\"]"}'
              
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?missions", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def get_missions(self):
        post_data = 'action=get&data={}'
              
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?missions", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def end_mission(self,mission_id):
        post_data = 'action=get&data={"end":'+str(mission_id)+'}'
              
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?missions", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def terminal(self,post_data):
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?terminal", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text 

    def pulse(self,remote_ip):
        post_data = 'action=get&data={"command":"[\\"pulse\\",\\"'+str(remote_ip)+'\\"]"}'
        return self.terminal(post_data)

    def connect_remote(self,remote_ip):
        post_data = 'action=get&data={"command":"[\\"-c\\",\\"'+str(remote_ip)+'\\"]"}'
        res = self.terminal(post_data)
        return res

    def remove_file(self,file_name):
        post_data = 'action=get&data={"command":"[\\"rm\\",\\"'+file_name+'\\"]"}'
        res = self.terminal(post_data)
        return res
    
    def scan(self):
        post_data = 'action=get&data={"command":"[\\"scan\\"]"}'
        res = self.terminal(post_data)
        return res  

    def inventory(self):
        post_data = 'action=get&data={"player":"items"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?inventory", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def exit_connection(self):
        post_data = 'action=get&data={"command":"[\\"exit\\"]"}'
        res = self.terminal(post_data)
        return res

    def factions(self):
        post_data = 'action=get&data={"view":"player"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?factions", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def defense(self):
        post_data = 'action=get&data={"check":true}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?defense", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def get_logs(self):
        post_data = 'action=get&data={"order":["id","desc"],"makenew":"new"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?logs", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def remove_log(self,id):
        post_data = 'action=remove&data={"id":"'+str(id)+'"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?logs", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text 

    def remove_remote_log(self,id):
        post_data = 'action=remove&data={"id":"'+str(id)+'"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?remotelogs", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text 

    def get_chat(self):
        post_data = 'action=get&data={}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?chat", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def get_processes(self):
        post_data = 'action=get&data={}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?processes", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def end_process(self,pid):
        post_data = 'action=get&data={"finish":"'+str(pid)+'"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?processes", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def get_files(self):
        post_data = 'action=get&data={}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?files", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def get_activity(self):
        post_data = 'action=get&data={}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?activity", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def format_harddrive(self):
        post_data = 'action=get&data={"command":"[\\"format\\",\\"harddrive\\"]"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?terminal", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text

    def format_logs(self):
        post_data = 'action=get&data={"command":"[\\"format\\",\\"logs\\"]"}'
        r = requests.Request("POST", "https://www.slavehack2.com/theme/api/?terminal", \
            cookies={'Slavehack':self.cookie}, \
            headers=self.post_headers, \
            data=post_data \
        )
        p = r.prepare()
        s=requests.Session()
        return s.send(p).text