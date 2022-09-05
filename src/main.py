# -*- coding: utf8 -*-
import json, requests
import os, sys, logging

from typing import List
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from typing import List, Dict
from yaml import load, dump, Loader, Dumper

cur_dir = os.path.abspath(__file__).rsplit("/", 2)[0]
log_path = os.path.join(cur_dir, "run.log")
logger = logging.getLogger(__file__)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)
logger.setLevel(logging.DEBUG)


class User:
    def __init__(self):
        self.tag = None
        self.name = None
        self.request_method = None
        self.url = None
        self.head = None

    def get_config_from_dict(self, users_config: Dict):
        usr_count_config = users_config["count"]
        self.tag = usr_count_config["tag"]
        self.name = usr_count_config["name"]
        self.request_method = usr_count_config["request_method"]
        self.url = usr_count_config["url"]
        self.bark_token = usr_count_config["bark_token"]
        self.head = usr_count_config["head"]


class configReader:
    def __init__(self):
        self.conf = None
        self.read_config_from_file()

    def read_config_from_file(self):
        logging.debug("正在读取配置文件......")
        try:
            with open("config.yaml", "r") as f:
                self.conf = load(f, Loader=Loader)
                temp = load(f, Loader=Loader)
                logging.info("成功读取配置文件")
        except FileNotFoundError:
            logging.warning("配置文件不存在")
        return temp


class dounaiSign:
    def __init__(self, conf: dict):
        self.conf = conf
        self.msg = None
        self.main_loop()

    def main_loop(self):
        logging.debug("开始执行脚本")
        sched = BlockingScheduler()
        for user in self.conf["users"]:
            usr = User()
            usr.get_config_from_dict(users_config=user)

            sched.add_job(
                self.main_handler, "cron", [usr], hour=1, minute=0, id=usr.name
            )
        sched.start()

    def main_handler(self, usr: User):

        logging.debug("用户：%s, 开始执行" % usr.name)
        r = requests.request("POST", url=usr.url, headers=usr.head, verify=False)
        self.msg = json.loads(r.text)
        logging.info("用户：%s 执行结果：%s" % (usr.name, self.msg["msg"]))
        bark_url = "https://api.day.app/{}/{}/{}?group=签到".format(
            usr.bark_token, usr.tag, self.msg["msg"]
        )
        r = requests.get(url=bark_url, headers=usr.head)
        if r.status_code == 200:
            logging.info("用户: %s 签到成功" % usr.name)
        else:
            logging.waring("无法通知用户")


if __name__ == "__main__":
    config = configReader()
    dounaiSign(config.conf)
    exit()
