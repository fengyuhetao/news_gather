# -*- coding:utf-8 -*-
import requests
from scrapy.selector import Selector
import pymysql

conn = pymysql.connect(host="localhost", user="root", passwd="", db="crawl", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取ip
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36"}

    ip_list = []
    for i in range(2025):
        print("http://www.xicidaili.com/nn/{0}".format(i))
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers = headers)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

    for ip in ip_list:
        print(ip)
        cursor.execute(
            "insert into proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, '{3}') ON DUPLICATE KEY UPDATE port=VALUES(port), speed=VALUES(speed), proxy_type=VALUES(proxy_type)".format(
                ip[0], ip[1], ip[3], ip[2]
            )
        )

        conn.commit()


class GetIp(object):
    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "https://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, proxies = proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code <= 200 and code < 300:
                print("efective ip")
                return True
            else:
                print('invalid ip and port')
                delete_ip(ip)
                return False

    def delete_ip(self, ip):
        cursor.execute("delete from proxy_ip where ip = '{0}'".format(ip))
        cursor.commit()

    def get_random_ip(self):
        # 从数据库中随机获取一个ip
        random_sql = "select ip, port from proxy_ip order by RAND() limit 1"
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            if self.judge_ip(ip, port):
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    get_ip = GetIp()
    get_ip.get_random_ip()
    # crawl_ips()