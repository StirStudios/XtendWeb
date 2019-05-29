#!/usr/bin/env python


import sys
import json
import subprocess
import os
import platform
import psutil
import signal
import shutil
import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def nginxreload():
    with open(os.devnull, 'w') as FNULL:
        subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def sighupnginx():
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
hook_output = mydict["output"]
hook_output_dict = hook_output[0]
status = hook_output_dict["result"]
if status == 1:
    hookargs = mydict["args"]
    hookargs_domain = hookargs["domain"]
    conf_sub_domain = hookargs_domain.replace("_", ".", 1)
    if conf_sub_domain.startswith("*"):
        conf_sub_domain = "_wildcard_."+conf_sub_domain.replace('*.', '')
    silentremove(installation_path+"/domain-data/"+conf_sub_domain)
    silentremove(nginx_dir+conf_sub_domain+".conf")
    silentremove(nginx_dir+conf_sub_domain+".include")
    if os.path.isfile(cluster_config_file):
        with open(cluster_config_file, 'r') as cluster_data_yaml:
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        for server in cluster_data_yaml_parsed.keys():
            silentremove("/etc/nginx/"+server+"/"+conf_sub_domain+".conf")
            silentremove("/etc/nginx/"+server+"/"+conf_sub_domain+".include")
    if os.path.exists('/var/resin/hosts/'+conf_sub_domain):
        shutil.rmtree('/var/resin/hosts/'+conf_sub_domain)
    sighupnginx()
    print(("1 nDeploy:cPaneltrigger:RemoveSubdom:"+conf_sub_domain))
else:
    print(("0 nDeploy:cPaneltrigger:SkipHook"))
