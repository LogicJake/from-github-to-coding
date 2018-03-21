import json
import subprocess
import os
import requests

from requests.auth import HTTPBasicAuth

cookie="sid=41a9cb2b-7acc-4033-a81d-6b5570ec8bbf; _ga=GA1.2.104327396.1521622508; _gid=GA1.2.252039607.1521622508; code=access-token%3Dfalse%2Ccoding-cli%3Dfalse%2Ccoding-owas%3Dfalse%2Ci18n%3Dfalse%2Clint%3Dfalse%2Cpages-ssl%3Dfalse%2Crelease%3Dfalse%2Csquash-optimize%3Dfalse%2Ctask-comment%3Dfalse%2Cv2%3Dfalse%2Cvip%3Dtrue%2Czip-download%3Dfalse%2C"
github_name="LogicJake"
coding_name="kexijia"
token = "************"

def coding_get_projects():
    url = "https://coding.net/api/projects?page=1&pageSize=1000&type=created"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Cookie":cookie
    }
    response = json.loads(requests.get(url,headers=headers).text)['data']['list']
    return response

def coding_creat_project(project_name,description):
    url = "https://coding.net/api/project"
    data = {
        'teamGK': 'value1',
        'joinTeam': 'false',
        'name':project_name,
        'description':description,
        'type':1,       #0私用，1公有
        'vcsType':'git',
        'gitEnabled':'true',
        'gitReadmeEnabled':'false',
        'gitLicense':'no',
        'gitIgnore':'no',
        'members':''

    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Cookie": cookie
    }
    requests.post(url,data=data,headers=headers)

def github_get_repos():
    url = "https://api.github.com/users/{}/repos".format(github_name)
    response = json.loads(requests.get(url,auth=HTTPBasicAuth(github_name, token)).text)
    return response

def check_repo_exist(repo_name):
    repos = coding_get_projects()
    for repo in repos:
        if repo['name'] == repo_name:
            return True
    return False

def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path,i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)

def coding_get_last_commit(repo_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Cookie": cookie
    }
    url = "https://coding.net/api/user/{}/project/{}/git".format(coding_name,repo_name)
    response = json.loads(requests.get(url,headers=headers).text)['data']['depot'].get('lastCommitSha',"empty")
    return response

def github_get_last_commit(repo_name):
    url = "https://api.github.com/repos/{}/{}/commits".format(github_name,repo_name)
    response = json.loads(requests.get(url,auth=HTTPBasicAuth(github_name,token)).text)
    if isinstance(response,list):
        return response[0]['sha']
    else:
        print(response['message'])
        return "empty"

def synchronization(name,description):
    cd_command = "cd " + name + " & "
    clone_command = "git clone " + clone_url
    subprocess.Popen(clone_command, shell=True, stdout=subprocess.PIPE).wait()   # clone代码

    subprocess.Popen(cd_command + "git remote rm origin", shell=True, stdout=subprocess.PIPE).wait(timeout=10)

    # 修改远程仓库地址
    add_origin_command = cd_command + "git remote add origin https://git.coding.net/{}/{}.git".format(
        coding_name, name)
    subprocess.Popen(add_origin_command, shell=True, stdout=subprocess.PIPE).wait(timeout=10)

    res = check_repo_exist(name)
    if res:  # 如果存在直接推
        subprocess.Popen(cd_command + "git push origin master", shell=True, stdout=subprocess.PIPE).wait()
    else:
        coding_creat_project(name, description)
        subprocess.Popen(cd_command + "git push origin master", shell=True, stdout=subprocess.PIPE).wait()

if __name__ == '__main__':
    github_repos = github_get_repos()
    try:
        for repo in github_repos:
            name = repo['name']
            description = repo['description']
            clone_url = repo['clone_url']
            if(check_repo_exist(name)):
                github_last_commit = github_get_last_commit(name)
                coding_last_commit = coding_get_last_commit(name)
                if github_last_commit == "empty" or github_last_commit == coding_last_commit:
                    print(name+" don't need synchronization")
                    continue
                else:
                    synchronization(name, description)
            else:
                synchronization(name, description)
    except Exception as e:
        print(e)