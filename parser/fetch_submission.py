import csv
import json
import os
import requests
import sys
import yaml

# Read configuration file
CONFIG_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "env.yml")
with open(CONFIG_FILE) as cfg_file:
    CONFIG = yaml.full_load(cfg_file)

URIEL_BASE = "{0}://{1}".format(CONFIG["scheme"], CONFIG["uriel_url"])
JOPHIEL_BASE = "{0}://{1}".format(CONFIG["scheme"], CONFIG["jophiel_url"])

HEADERS = {'Content-type': 'application/json', 'Accept': '*/*'}
URIEL_URL = {
    "subm"    : "/api/v2/contests/submissions/programming/?contestJid={contestJid}&page={page}",
    "setting" : "/api/v2/contests/{contestJid}"
}


def get_auth_token(username, passwd):
    global HEADERS
    login_url = JOPHIEL_BASE + "/api/v2/session/login"
    req_body = { "usernameOrEmail" : username, "password" : passwd }

    api_resp = requests.post(login_url, json.dumps(req_body), headers=HEADERS).json()
    HEADERS["Authorization"] = "Bearer " + api_resp["token"]

def get_contest_setting(contestJid):
    if HEADERS.get("Authorization", None) == None:
        get_auth_token("superadmin", CONFIG["superadmin_password"])
    URL = URIEL_BASE + URIEL_URL['setting'].format(contestJid = contestJid)
    api_resp = requests.get(URL, headers = HEADERS).json()
    return api_resp

def get_submission(contestJid, page):
    if HEADERS.get("Authorization", None) == None:
        get_auth_token("superadmin", CONFIG["superadmin_password"])
    URL = URIEL_BASE + URIEL_URL['subm'].format(contestJid = contestJid, page = page)
    api_resp = requests.get(URL, headers = HEADERS).json()
    return api_resp["data"]["page"]

def get_problem_list(contestJid):
    if HEADERS.get("Authorization", None) == None:
        get_auth_token("superadmin", CONFIG["superadmin_password"])
    URL = URIEL_BASE + URIEL_URL['subm'].format(contestJid = contestJid, page = 1)
    api_resp = requests.get(URL, headers = HEADERS).json()
    ret = dict()
    for k in api_resp["problemAliasesMap"]:
        ret[k] = ord(api_resp["problemAliasesMap"][k]) - ord('A') + 1
    return ret

def get_participants_list(contestJid):
    if HEADERS.get("Authorization", None) == None:
        get_auth_token("superadmin", CONFIG["superadmin_password"])
    URL = URIEL_BASE + URIEL_URL['subm'].format(contestJid = contestJid, page = 1)
    api_resp = requests.get(URL, headers = HEADERS).json()
    return api_resp["config"]["userJids"]

def parsing_submission(submissions, prob_index, setting, participants):
    ret = dict()
    contest_start = setting["beginTime"]
    for submisi in submissions:
        verdict = "WA"
        if submisi["latestGrading"]["verdict"]["code"] == "AC": verdict = "AC"

        ret[submisi["id"]] = {
            "user_id": submisi["userJid"],
            "problem_index": prob_index[submisi["problemJid"]],
            "verdict": verdict,
            "submitted_seconds": (submisi["time"] - contest_start) // 1000
        }

    return ret

def parsing_users(participants, filename):
    ret = dict()
    with open(filename) as json_file:
        users = json.load(json_file)
    for jid in participants:
        if users.get(jid, None) == None:
            users[jid] = {
                "name": "Hilang",
                "institutionName": "Hilang"
            }
        ret[jid] = {
            "name": users[jid]["name"],
            "college": users[jid]["institutionName"],
            "is_exclude": False
        }    
    return ret

# Generating contest.json
CONTEST_JID = "JIDCONTVJoTiMNdvrrRFz6geue2"
CONTEST_SETTING = get_contest_setting(CONTEST_JID)
PROB_LIST = get_problem_list(CONTEST_JID)
PARTICIPANT_LIST = get_participants_list(CONTEST_JID) + ["JIDUSERmZGQKb4pC7W1RP81cJwy"]

all_submission = list()
print("== Fetch Submission Report ==")
for i in range(1, 1000):
    print(f"Page {i}", flush=True)
    res = get_submission(CONTEST_JID, i)
    if len(res) == 0:
        break
    else:
        all_submission += res

contest_json = {
    "problem_count": len(PROB_LIST),
    "solutions": parsing_submission(all_submission[::-1], PROB_LIST, CONTEST_SETTING, PARTICIPANT_LIST),
    "users": parsing_users(PARTICIPANT_LIST, "peserta.json")
}

with open("contest.json", "w+") as contest_file:
    json.dump(contest_json, contest_file)