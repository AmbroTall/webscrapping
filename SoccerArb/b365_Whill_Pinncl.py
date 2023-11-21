# Bet365, William Hill, Pinnacle
#   16        15,          18,   
import time
import lxml
from bs4 import BeautifulSoup
import re
import urllib.parse
import time
import pandas as pd
from thefuzz import process
import gevent
from gevent import monkey
monkey.patch_all()
import network_utils as nu
from match import Match
from db import *

headers = {
    'authority': 'www.oddsportal.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'op_lang=en; op_cookie-test=ok; op_user_time_zone=2; op_user_full_time_zone=37; _hjSessionUser_3147261=eyJpZCI6IjFmNjE4YjZiLWI0YmYtNTRiNi04MzlkLWJiOGFkYjAyZWE2NyIsImNyZWF0ZWQiOjE2ODYyMzc4Mjg4MjcsImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2023-06-08T15:31:53.969Z; eupubconsent-v2=CPtCerAPtCerAAcABBENDICsAP_AAAAAAChQJGtf_X__b2_j-_7_f_t0eY1P9_7_v-0zjhfdl-8N2f_X_L8X52M7vF36pqoKuR4ku3LBIQVlHOHcDUmw6okVryPsbk2cr7NKJ7PEmnMbO2dYGH9_n13T-ZKY7___f__z_v-v________7-3f3__p___-2_e_V_99zfn9_____9vP___9v-_9_3gAAAAAAAAAAAAD4AAABwkAIAGgC8xUAEBeYyACAvMdAEABoAGYAZQC8yEAIAMwAyiUAMAMwAygF5lIAgANAAzADKAXmAAA.f_gAAAAAAAAA; _gid=GA1.2.737963796.1686506349; op_user_login_id=440624; op_user_login_hash=38a85111bfccef6528177b48928e3927; op_user_logout=0; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ik4yRitjTUY3Z29lZ1liTitBbUlqUGc9PSIsInZhbHVlIjoiTy96cGNLUHRBN1NTN29VNk5Va0JKN3dwT0pEVnhjQnRHblFrbmNONElqNER2ZnlBUUU5Nlc2cDZqMXdZd2R2eVlVMFlmZ1hhTmZHNW82Y0tHTTYyQnNwZ05EZlN5STY2N1R2dTBGMGNXZGo5QjIwYm1ONG5Ec1F5WkdaMzdlRGtWRjhKZ2ZXKzBlc3MwODVBQXkyRU9RPT0iLCJtYWMiOiJkMGU1NTdjMGJlMzkzZjZkYTBiODkzOGZjNTJlOWU1NGJjNGE3ODE0ZjhmYjYwZTJjNDc5MDJlZGI4NGRhYjkzIiwidGFnIjoiIn0%3D; _sg_b_n=1686680672556; _hjSession_3147261=eyJpZCI6IjdjNGNmYTI4LTljOTgtNDdjMC1hYTNiLTQyYzc5OGUzZGRiNSIsImNyZWF0ZWQiOjE2ODY3Njg1MTk3NjksImluU2FtcGxlIjpmYWxzZX0=; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+14+2023+22%3A37%3A54+GMT%2B0200+(Central+European+Summer+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=d86e3621-94a1-4805-80cb-9b8cab1f3816&interactionCount=3&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1&AwaitingReconsent=false&geolocation=SI%3B060; _ga=GA1.1.90401562.1686237953; _sg_b_p=%2Ffootball%2Fargentina%2Fliga-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Festudiantes-l-p-san-lorenzo-I5STvWSu%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fcentral-cordoba-santiago-del-estero-gimnasia-l-p-xzqXLHM0%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Ftigre-velez-sarsfield-OpK1ycMm%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Funion-de-santa-fe-lanus-dKPcyr4c%2F; _sg_b_v=38%3B121458%3B1686774994; XSRF-TOKEN=eyJpdiI6IllYU1ZVcFZMdC9RVi9Sb0wwNFArQmc9PSIsInZhbHVlIjoiVm5TeG5MZFc3UlVyZDBNdm03MUxTa2crZlhIbklIQTYzbnZRcXk4WW9VelBITzZSZzFlbXowV2JQNDlNc1BwTVBtejNpQllCVGs3bG5DdFhhRnJUQTBOcmhiNzJicG0wNS9OTlVQRldXcmtJZjd4bVpmcU5HOE9GaWVXVVoxTW0iLCJtYWMiOiJmNjZmMGQxNGE0YmMzOTliZDA1NTM5MjQ3Y2M0NDVhYjNlOGE3MjJlMGIxYzFiZTdhYWIxN2JmNWQwMTE1NjU0IiwidGFnIjoiIn0%3D; oddsportalcom_session=eyJpdiI6ImVIM3NEZFV2c1FJZmRpNTdDWEUrWmc9PSIsInZhbHVlIjoiYTZKTlBrdUwyUXdoZnNodTdZTmhyTndVS0Z6eExObmpzTFJTTHVMRWlzRFZhRSs5YktwRDdRR01YZWpBSW93bVA3bXZZeDZqMlJLT1lpSXp5REZMU1lONE4rbENQOE0yd0dmR0NRUUd0L0tCczVhajQ5M0EwMUhycVNyaVVackQiLCJtYWMiOiI1ZjU3NWVmODA5Yjg1NWU5YzdmOWU3YTYwMWFhNDA2NWFhNzYxZTQ5MzkzZTNiN2M4ODU4YjYxMTA1NTA0YTE1IiwidGFnIjoiIn0%3D; _ga_5YY4JY41P1=GS1.1.1686774991.32.1.1686775165.60.0.0; op_lang=en; op_user_cookie=5496935221; op_user_hash=d5d33f67497f4d434b04dddbdf5588e1; op_user_time=1686237826',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.oddsportal.com/football/brazil/serie-a/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IllYU1ZVcFZMdC9RVi9Sb0wwNFArQmc9PSIsInZhbHVlIjoiVm5TeG5MZFc3UlVyZDBNdm03MUxTa2crZlhIbklIQTYzbnZRcXk4WW9VelBITzZSZzFlbXowV2JQNDlNc1BwTVBtejNpQllCVGs3bG5DdFhhRnJUQTBOcmhiNzJicG0wNS9OTlVQRldXcmtJZjd4bVpmcU5HOE9GaWVXVVoxTW0iLCJtYWMiOiJmNjZmMGQxNGE0YmMzOTliZDA1NTM5MjQ3Y2M0NDVhYjNlOGE3MjJlMGIxYzFiZTdhYWIxN2JmNWQwMTE1NjU0IiwidGFnIjoiIn0='
}
base_headers = {
    'authority': 'www.oddsportal.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'op_lang=en; op_cookie-test=ok; op_user_time_zone=2; op_user_full_time_zone=37; _hjSessionUser_3147261=eyJpZCI6IjFmNjE4YjZiLWI0YmYtNTRiNi04MzlkLWJiOGFkYjAyZWE2NyIsImNyZWF0ZWQiOjE2ODYyMzc4Mjg4MjcsImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2023-06-08T15:31:53.969Z; eupubconsent-v2=CPtCerAPtCerAAcABBENDICsAP_AAAAAAChQJGtf_X__b2_j-_7_f_t0eY1P9_7_v-0zjhfdl-8N2f_X_L8X52M7vF36pqoKuR4ku3LBIQVlHOHcDUmw6okVryPsbk2cr7NKJ7PEmnMbO2dYGH9_n13T-ZKY7___f__z_v-v________7-3f3__p___-2_e_V_99zfn9_____9vP___9v-_9_3gAAAAAAAAAAAAD4AAABwkAIAGgC8xUAEBeYyACAvMdAEABoAGYAZQC8yEAIAMwAyiUAMAMwAygF5lIAgANAAzADKAXmAAA.f_gAAAAAAAAA; _gid=GA1.2.737963796.1686506349; op_user_login_id=440624; op_user_login_hash=38a85111bfccef6528177b48928e3927; op_user_logout=0; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ik4yRitjTUY3Z29lZ1liTitBbUlqUGc9PSIsInZhbHVlIjoiTy96cGNLUHRBN1NTN29VNk5Va0JKN3dwT0pEVnhjQnRHblFrbmNONElqNER2ZnlBUUU5Nlc2cDZqMXdZd2R2eVlVMFlmZ1hhTmZHNW82Y0tHTTYyQnNwZ05EZlN5STY2N1R2dTBGMGNXZGo5QjIwYm1ONG5Ec1F5WkdaMzdlRGtWRjhKZ2ZXKzBlc3MwODVBQXkyRU9RPT0iLCJtYWMiOiJkMGU1NTdjMGJlMzkzZjZkYTBiODkzOGZjNTJlOWU1NGJjNGE3ODE0ZjhmYjYwZTJjNDc5MDJlZGI4NGRhYjkzIiwidGFnIjoiIn0%3D; _sg_b_n=1686680672556; op_user_cookie=5525659674; op_user_hash=041db7d8204ae7af3727c0d1307dc875; op_user_time=1686768519; _hjSession_3147261=eyJpZCI6IjdjNGNmYTI4LTljOTgtNDdjMC1hYTNiLTQyYzc5OGUzZGRiNSIsImNyZWF0ZWQiOjE2ODY3Njg1MTk3NjksImluU2FtcGxlIjpmYWxzZX0=; XSRF-TOKEN=eyJpdiI6InpkbVdnVjBiYmlOVXYzWUg1V0cxSnc9PSIsInZhbHVlIjoieHp3cWVHbXFqdFM5RGlCVXNya1FBc3R5Q1kzclhGMG02WWxtREgxYmdBY0RRTEVwVmNFelc3OGc3VGI3Wi84ZVdRaDFlS1Vmay9zV25qb210d05zT1YxUmtTYUIwUTJBMlhySWd0Rnp2MUNPWUdlT01PSkZETkRGOVNiUTRNUW8iLCJtYWMiOiI3NTg3YTg3M2U0OGUzNWM5MTQ4NjI4M2YwNGU3YjI0ODIxMjkxMzI0NzllZmY5ZmE4ZWJhZGI0OTRmOWY1ZTUzIiwidGFnIjoiIn0%3D; oddsportalcom_session=eyJpdiI6InE5b0pBREtSaGNJeW9UaGlUUitwaFE9PSIsInZhbHVlIjoiYmhQbVd1UDVtTldIRGRnMnkxMjJHWG9udmJoaTlBcG5QNG9hd05RZDI1cTRDQjNrWUhvOHNERzVCTnZpNE1zVjR6U3RQMjZIWXZWaUpLRUQ5bytiV1pEMWtXdFVVRzBYTHhxWEJkUjJlRCtSNWk4SS9wVU94dUtpcEx5RnJYUFciLCJtYWMiOiIyNzZmMWM3MDAxNzc0ODllOGYxZWY0OWZhYmJkMDYzOGYzMTY5ZjJlNDEyYzdmNzAxNWVlOWU3NDM0NzIzNzBkIiwidGFnIjoiIn0%3D; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+14+2023+22%3A37%3A54+GMT%2B0200+(Central+European+Summer+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=d86e3621-94a1-4805-80cb-9b8cab1f3816&interactionCount=3&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1&AwaitingReconsent=false&geolocation=SI%3B060; _ga_5YY4JY41P1=GS1.1.1686774991.32.1.1686775074.57.0.0; _ga=GA1.1.90401562.1686237953; _sg_b_p=%2Ffootball%2Fargentina%2Fliga-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Festudiantes-l-p-san-lorenzo-I5STvWSu%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fcentral-cordoba-santiago-del-estero-gimnasia-l-p-xzqXLHM0%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Ftigre-velez-sarsfield-OpK1ycMm%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Funion-de-santa-fe-lanus-dKPcyr4c%2F; _sg_b_v=38%3B121458%3B1686774994; XSRF-TOKEN=eyJpdiI6IjlpRjJ4K0RYUjlTeGFJYW5VdkU2bmc9PSIsInZhbHVlIjoiSlRrWHNqMGc5ekl1RlNZdFBmRUFiSUlTTnRFWG13UEc5ejlqQVJDZmF4aEFQdHRlVnp2V1JHeVh3M0NKZ1NIdVlmRzEwZkswaEdjQ3VJbU1rWTJ6MStLZUhKb3hQK2xaV2poR0JIVm9kZlRtUlprTWloZTBVNk5zWGdJVXRhK2MiLCJtYWMiOiJkMjBkMTM2YzI1MDczOGYwNGVhMTc4ZjVlOTNmOTY3MzFkZjgzNTk3MzQyODk4M2ZmNTIwNTk3N2EyY2Q4NDhlIiwidGFnIjoiIn0%3D; oddsportalcom_session=eyJpdiI6IlVxQ0tTWjFoRUFyT3RNTmxTa0NJbUE9PSIsInZhbHVlIjoicGdLN3BkY2FwZkp4S1pCenczWC93K2FqUnNoNU5ZblNCNHpaVndEZFVCR2xkcm5qclBELy9DRFcwdVQ3VXNqVGtWeHkwejR4cVh1L1Z0Y05xR3pCNDB2KzdQUEhmamQzWTk1VEppMzI1djBTRklSd1o3dVM1TXhrQ3VDM0F0TTUiLCJtYWMiOiI4Y2VkZDc1MzlhOWYxZmZkM2MwNTU5MzA2YzkwMjI4NjIyOTgyMzM4ZWYyMTdjZWY4OWI1OWYwNTE3NDFkZDZlIiwidGFnIjoiIn0%3D; op_lang=en',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.oddsportal.com/football/argentina/liga-profesional/union-de-santa-fe-lanus-dKPcyr4c/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
bookmaker_mapping = {
    15: 'WilliamHill',
    16: 'Bet365',
    18: 'Pinnacle',
    15: 'WilliamHill'
}

def ALP():
   url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/8dtSizGC/X0/1/?_=1686316105"
   base_url = "https://www.oddsportal.com/football/argentina/liga-profesional/"
   country = "argentina"
   league = "liga-profesional"
   return oddsportalGetData(url, base_url, country, league, "ALP")
def BSA():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/MVWjN1qg/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686775165"
    base_url = "https://www.oddsportal.com/football/brazil/serie-a/"
    country = "brazil"
    league = "serie-a"
    return oddsportalGetData(url, base_url, country, league, "BSA")
def BSB():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/GhWfMLba/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686849387"
    base_url = "https://www.oddsportal.com/football/brazil/serie-b/"
    country = "brazil"
    league = "serie-b"
    return oddsportalGetData(url, base_url, country, league, "BSB")
def CPA():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/IReM2SoJ/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686855765"
    base_url = "https://www.oddsportal.com/football/colombia/primera-a/"
    country = "colombia"
    league = "primera-a"
    return oddsportalGetData(url, base_url, country, league, "CPA")
def ELP():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/vFoYw2WS/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686856002"
    base_url = "https://www.oddsportal.com/football/ecuador/liga-pro/"
    country = "ecuador"
    league = "liga-pro"
    return oddsportalGetData(url, base_url, country, league, "ELP")
def PL1():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/IZNOo7tp/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686856569"
    base_url = "https://www.oddsportal.com/football/peru/liga-1/"
    country = "peru"
    league = "liga-1"
    return oddsportalGetData(url, base_url, country, league, "PL1")
def USM():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/AZ3pnDvF/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1686856782"
    base_url = "https://www.oddsportal.com/football/usa/mls/"
    country = "usa"
    league = "mls"
    return oddsportalGetData(url, base_url, country, league, "USM")

def EPL():
    url = "https://www.oddsportal.com/ajax-sport-country-tournament_/1/jDTEm9zs/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691185049"
    base_url = "https://www.oddsportal.com/football/england/premier-league/"
    country = "england"
    league = "premier-league"
    return oddsportalGetData(url, base_url, country, league, "EPL")
def EFL():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/rZ2Ayuh9/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691352163'
    base_url = "https://www.oddsportal.com/football/england/championship/"
    country = "england"
    league = "championship"
    return oddsportalGetData(url, base_url, country, league, "EFL")
def EL1():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/YViCkbM8/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691414170'
    base_url = "https://www.oddsportal.com/football/england/league-one/"
    country = "england"
    league = "league-one"
    return oddsportalGetData(url, base_url, country, league, "EL1")
def EL2():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/ShiGlIyF/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691453416'
    base_url = "https://www.oddsportal.com/football/england/league-two/"
    country = "england"
    league = "league-two"
    return oddsportalGetData(url, base_url, country, league, "EL2")
def SP():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/SbnnvNtB/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691622499'
    base_url = "https://www.oddsportal.com/football/scotland/premiership/"
    country = "scotland"
    league = "premiership"
    return oddsportalGetData(url, base_url, country, league, "SP")
def SC():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/bkBjM1dU/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691773420'
    base_url = "https://www.oddsportal.com/football/scotland/championship/"
    country = "scotland"
    league = "championship"
    return oddsportalGetData(url, base_url, country, league, "SC")
def IFD():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/IJX5kfYO/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691662305'
    base_url = "https://www.oddsportal.com/football/ireland/division-1/"
    country = "ireland"
    league = "division-1"
    return oddsportalGetData(url, base_url, country, league, "IFD")
def IPD():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/GMJa5ZXB/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691769046'
    base_url = "https://www.oddsportal.com/football/ireland/premier-division/"
    country = "ireland"
    league = "premier-division"
    return oddsportalGetData(url, base_url, country, league, "IPD")
def SPD():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/bJrC4h3n/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691853055'
    base_url = "https://www.oddsportal.com/football/spain/laliga/"
    country = "spain"
    league = "laliga"
    return oddsportalGetData(url, base_url, country, league, "SPD")
def SSD():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/KYWK2WXb/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691873501'
    base_url = "https://www.oddsportal.com/football/spain/laliga2/"
    country = "spain"
    league = "laliga2"
    return oddsportalGetData(url, base_url, country, league, "SSD")
def FL1():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/4bh0n8Xm/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1691929453'
    base_url = "https://www.oddsportal.com/football/france/ligue-1/"
    country = "france"
    league = "ligue-1"
    return oddsportalGetData(url, base_url, country, league, "FL1")
def FL2():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament_/1/n7FCoSnf/X489013294X67133448X67584X0X134217728X0X0X0X0X0X0X0X10485760X134217729X512X1048578X0X0X1024X26656X131072X2304/1/?_=1692011392'
    base_url = "https://www.oddsportal.com/football/france/ligue-2/"
    country = "france"
    league = "ligue-2"
    return oddsportalGetData(url, base_url, country, league, "FL2")

def get_json(data_rs, i):
    data = []
    if data_rs[i]:
        try:
          data = data_rs[i].json()
        except ValueError:
           print('Decoding JSON has failed')
        if(data and 'd' in data and 'oddsdata' in data['d']):
            return data['d']['oddsdata']['back']
    return []

def oddsportalExtractData(status_rs, u1x2_rs, fh_rs, ggng_rs, dnb_rs, oddeven_rs, xhashes, tag):
  bookmakers = []
  for i in range(0, len(u1x2_rs)):
    status = None
    if(status_rs[i]):
       try:
        status = status_rs[i].json()
       except ValueError:
        print('Decoding status JSON has failed')
    if(not status or 'd' not in status or status['d']['isFinished'] or status['d']['isStarted']):
       continue
    matches_data = get_json(u1x2_rs, i)
    fh_data = get_json(fh_rs, i)
    ggng_data = get_json(ggng_rs, i)
    dnb_data = get_json(dnb_rs, i)
    oe_data = get_json(oddeven_rs, i)

    encodeId = list(xhashes.keys())[i]
    data = xhashes[encodeId]

    if(matches_data and 'E-1-2-0-0-0' in matches_data and 'odds' in matches_data['E-1-2-0-0-0']):
      for bookie, odds in matches_data['E-1-2-0-0-0']['odds'].items():
        if(bookie in matches_data['E-1-2-0-0-0']['act'] and (not matches_data['E-1-2-0-0-0']['act'][bookie])):
          continue
        if(int(bookie) not in bookmaker_mapping):
          continue
        name1 = data['match_name'].split(" - ")[0]
        name2 = data['match_name'].split(" - ")[1]
        name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
        ggng_odds = []
        fh_odds = []
        dnb_odds = []
        oddeven_odds = []
        if ggng_data and bookie in ggng_data['E-13-2-0-0-0']['odds']:
          ggng_odds = ggng_data['E-13-2-0-0-0']['odds'][bookie]
        if fh_data and bookie in fh_data['E-1-3-0-0-0']['odds']:
          fh_odds = fh_data['E-1-3-0-0-0']['odds'][bookie]
        if dnb_data and bookie in dnb_data['E-6-2-0-0-0']['odds']:
          dnb_odds = dnb_data['E-6-2-0-0-0']['odds'][bookie]
        if oe_data and bookie in oe_data['E-10-2-5-0-0']['odds']:
          oddeven_odds = oe_data['E-10-2-5-0-0']['odds'][bookie]

        bookmaker_name = bookie
        if(int(bookie) in bookmaker_mapping):
          bookmaker_name = bookmaker_mapping[int(bookie)]

        bookmaker_dict = next((b for b in bookmakers if b["Name"] == bookmaker_name), None)
        if bookmaker_dict is None:
          bookmaker_dict = {"Name": bookmaker_name, "Matches": []}
          bookmakers.append(bookmaker_dict)
        match = createMatch(odds, fh_odds, ggng_odds, dnb_odds, oddeven_odds, name)
        bookmaker_dict["Matches"].append(match)
  return bookmakers

def oddsportalGetData(url, base_url, country, league, tag):
  headers = {
    'authority': 'www.oddsportal.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'op_lang=en; op_cookie-test=ok; op_user_time_zone=2; op_user_full_time_zone=37; _hjSessionUser_3147261=eyJpZCI6IjFmNjE4YjZiLWI0YmYtNTRiNi04MzlkLWJiOGFkYjAyZWE2NyIsImNyZWF0ZWQiOjE2ODYyMzc4Mjg4MjcsImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2023-06-08T15:31:53.969Z; op_user_login_id=440624; op_user_login_hash=38a85111bfccef6528177b48928e3927; op_user_logout=0; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ik4yRitjTUY3Z29lZ1liTitBbUlqUGc9PSIsInZhbHVlIjoiTy96cGNLUHRBN1NTN29VNk5Va0JKN3dwT0pEVnhjQnRHblFrbmNONElqNER2ZnlBUUU5Nlc2cDZqMXdZd2R2eVlVMFlmZ1hhTmZHNW82Y0tHTTYyQnNwZ05EZlN5STY2N1R2dTBGMGNXZGo5QjIwYm1ONG5Ec1F5WkdaMzdlRGtWRjhKZ2ZXKzBlc3MwODVBQXkyRU9RPT0iLCJtYWMiOiJkMGU1NTdjMGJlMzkzZjZkYTBiODkzOGZjNTJlOWU1NGJjNGE3ODE0ZjhmYjYwZTJjNDc5MDJlZGI4NGRhYjkzIiwidGFnIjoiIn0%3D; _gid=GA1.2.122700242.1688309128; eupubconsent-v2=CPtCerAPtCerAAcABBENDMCsAP_AAAAAAChQJGtf_X__b2_j-_7-f_t0eY1P9_7_v-0zjhfdl-8N2f_X_L8X52M7vF16pqoKuR4ku3LBIQVlHOHcDUmw6okVryPsbk2cr7NKJ7PEmnMbO2dYGH97n13T-ZKY7___f__z_v-v________7-3f3__p___-2_e_V_89zfn9_____9vP___9v-_9_3gAAAAAAAAAAAAD4AAABQkAIAGgC8x0AQAGgAZgBlALzIQAgAzADKJQAwAzADKAXmUgCAA0ADMAMoBeYAAA.f_gAAAAAAAAA; _sg_b_n=1688309675838; op_user_time=1688327712; op_user_cookie=5590549574; op_user_hash=283e2e21d6cb261a6befe95ebac3d2a0; _hjIncludedInSessionSample_3147261=0; _hjSession_3147261=eyJpZCI6IjFhYmU4MGM0LWRiODQtNDY2YS1hZjMwLTJjMWY2YzhlOWQ0YyIsImNyZWF0ZWQiOjE2ODgzMjc3MTE4NDksImluU2FtcGxlIjpmYWxzZX0=; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jul+02+2023+21%3A56%3A39+GMT%2B0200+(Central+European+Summer+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=d86e3621-94a1-4805-80cb-9b8cab1f3816&interactionCount=3&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1&AwaitingReconsent=false&geolocation=SI%3B060; _ga_5YY4JY41P1=GS1.1.1688327708.54.1.1688327799.56.0.0; _ga=GA1.1.90401562.1686237953; _sg_b_p=%2Ffootball%2Fargentina%2Fliga-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fcolon-santa-fe-racing-club-GbsZyUCb%2F; _sg_b_v=62%3B187169%3B1688327713; XSRF-TOKEN=eyJpdiI6Imt2YzdDaERHZTdvTmFBWi8yb0QweGc9PSIsInZhbHVlIjoia0VXb3FaTWdDQzNjcGZLSVoxY1c3Rkw4WE5jSExNTndTRWRZTzNYL2F4Mnh1QzdNa05CbmJPMVlTc1ZlSEliTVl2ODN5T2VVcjVXazZzc0VZK0ovOWV5VlFWVDJIK3FmeDUrcVVRK2J6UnQwMUNleTc0QklZTVFuVVUzVkFJY0UiLCJtYWMiOiJkZWVkN2ExODNjYWI0NzNkMDEwNmQ0Y2RhNjFiOTNhYzA2NDA0NzcxYzlkZjM2NTk3MGZjZGQ2YTdmYjUyNjdhIiwidGFnIjoiIn0%3D; oddsportalcom_session=eyJpdiI6ImRtR1Y0c1phU1dvZTNXSGhMdi9TUHc9PSIsInZhbHVlIjoiTHFoZXRlSEFwQUoxVExRaTZ6SEprR2tzL25jVmIrSU9JcmIzQWNQYmZaNXF0MWlyVjhJRXZ1cVRxYm9PZmdxc1oxb0V1cFA4T3FVcnFEVUI1Wlg2MW1MTjdDYmkvUGszQldkU2JDbmdCR2NNTmdzU09yWmk0Y3ZDVjg3bmh5ZUciLCJtYWMiOiJjY2MxMjlkYjUxZWJkZTJiMTc4MDM1ZGJkZDc4MWZjMGI3YzY4NzlmNWNmYjVjYThkYjMwM2VmOWExMzZkMWRlIiwidGFnIjoiIn0%3D; op_lang=en',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.oddsportal.com/football/argentina/liga-profesional/colon-santa-fe-racing-club-GbsZyUCb/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6Imt2YzdDaERHZTdvTmFBWi8yb0QweGc9PSIsInZhbHVlIjoia0VXb3FaTWdDQzNjcGZLSVoxY1c3Rkw4WE5jSExNTndTRWRZTzNYL2F4Mnh1QzdNa05CbmJPMVlTc1ZlSEliTVl2ODN5T2VVcjVXazZzc0VZK0ovOWV5VlFWVDJIK3FmeDUrcVVRK2J6UnQwMUNleTc0QklZTVFuVVUzVkFJY0UiLCJtYWMiOiJkZWVkN2ExODNjYWI0NzNkMDEwNmQ0Y2RhNjFiOTNhYzA2NDA0NzcxYzlkZjM2NTk3MGZjZGQ2YTdmYjUyNjdhIiwidGFnIjoiIn0='
  }
  headers1 = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'authority': 'www.oddsportal.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
      'cache-control': 'no-cache',
      'cookie': 'op_lang=en; op_cookie-test=ok; op_user_time=1686237826; op_user_cookie=5496935221; op_user_hash=d5d33f67497f4d434b04dddbdf5588e1; op_user_time_zone=2; op_user_full_time_zone=37; _hjSessionUser_3147261=eyJpZCI6IjFmNjE4YjZiLWI0YmYtNTRiNi04MzlkLWJiOGFkYjAyZWE2NyIsImNyZWF0ZWQiOjE2ODYyMzc4Mjg4MjcsImV4aXN0aW5nIjp0cnVlfQ==; _sg_b_n=1686237878835; OptanonAlertBoxClosed=2023-06-08T15:31:53.969Z; _gid=GA1.2.1376262122.1686238314; eupubconsent-v2=CPtCerAPtCerAAcABBENDICsAP_AAAAAAChQJGtf_X__b2_j-_7_f_t0eY1P9_7_v-0zjhfdl-8N2f_X_L8X52M7vF36pqoKuR4ku3LBIQVlHOHcDUmw6okVryPsbk2cr7NKJ7PEmnMbO2dYGH9_n13T-ZKY7___f__z_v-v________7-3f3__p___-2_e_V_99zfn9_____9vP___9v-_9_3gAAAAAAAAAAAAD4AAABwkAIAGgC8xUAEBeYyACAvMdAEABoAGYAZQC8yEAIAMwAyiUAMAMwAygF5lIAgANAAzADKAXmAAA.f_gAAAAAAAAA; _hjSession_3147261=eyJpZCI6IjAwNmNlZDBiLThmNmYtNDQyNC1hMWFjLTcxZmQwMTlhMmI4MCIsImNyZWF0ZWQiOjE2ODYzMzY1MzQ3MDIsImluU2FtcGxlIjpmYWxzZX0=; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jun+09+2023+21%3A03%3A22+GMT%2B0200+(Central+European+Summer+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=d86e3621-94a1-4805-80cb-9b8cab1f3816&interactionCount=3&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CSTACK42%3A1&AwaitingReconsent=false&geolocation=SI%3B060; _ga_5YY4JY41P1=GS1.1.1686336535.7.1.1686337402.54.0.0; _ga=GA1.2.90401562.1686237953; _gat_UA-821699-19=1; XSRF-TOKEN=eyJpdiI6IlJNMmNQakZ4YXFBY2Y5NHFvUVlwbGc9PSIsInZhbHVlIjoiRkhSNWdyLzc0YXkzSWJMTnp4UW9ZN3J0NDJFekZnYW5DdGNoRUJhbWljS3dNbVpYa0lHajJ1Qm43ZzBpait0bDI3OFljNm85Yld1cHlXeDBQQk9uZlJyQ2szQkl4TnZUYWtWYkFZbmxwWEJwNlk0R0tDTngyZE5lQ0s0VTJhOFkiLCJtYWMiOiJiOTc0MjdkODU5NmZhZTQ5NWRmNGNhMTRhNTU3N2I4MTAzMDc0NjhiNzIyMDZhM2I2YmEwMzEwMjQ3Mjk5OTIyIiwidGFnIjoiIn0%3D; oddsportalcom_session=eyJpdiI6IlBsQ0NRVVBoc1RQYVltR2Z1Zzc2QUE9PSIsInZhbHVlIjoieFJGd01mQmc3YXN4RWU4NWVmdWszMkxKUXkrVjFpRW9MTU81aDdhcXNYclhBZkZjNGFHcTkybGpEL1BjaTJLams0Rm8rbFZXY2J4c2w0SUFNcUlMRk9mMmtvbTAxRk1yMFdtVG1vek56Tk1YaEhwRDZJWGs1MERqcjB3QW1DUWoiLCJtYWMiOiI5ODY0MDVlNmI4OGQ5NWU0NjlhZDVmYzIwODliOWM5OGEwMjhhM2QzMWUxNzEzMzljYTAwNjc4ODlhN2EyMmUwIiwidGFnIjoiIn0%3D; _sg_b_p=%2Ffootball%2Fbolivia%2Fdivision-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fbarracas-central-rosario-central-EXVtB08r%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fbarracas-central-rosario-central-EXVtB08r%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fbarracas-central-rosario-central-EXVtB08r%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fbarracas-central-rosario-central-EXVtB08r%2F%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fboca-juniors-lanus-hr5lUuFK%2F%2C%2Ffootball%2Fengland%2Fpremier-league-2019-2020%2Fliverpool-norwich-4IMoMG3q%2C%2Ffootball%2Fargentina%2Fliga-profesional%2Fboca-juniors-lanus-hr5lUuFK%2F; _sg_b_v=7%3B27421%3B1686336536',
      'dnt': '1',
      'pragma': 'no-cache',
      'referer': 'https://www.oddsportal.com/football/argentina/liga-profesional/',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1'
  }
  headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6IjlnbW1jTXUrd21OQWJlVjdYb1lnQXc9PSIsInZhbHVlIjoiamhINnJqTERmb2hQZEQxR3htRDh2MCs3YjFTYkVDZm9xRUlqSWZ4UklEd3V2Uko2bnk1Y1g1T0tRRktsZFFLTm90STIyK1JySVJsTlpCMmVyR2ZlbitoeUlDeE5OVktoaDRRZVBZWm1ra3hEYkwwSE9ITmViUWtBRTBaWGpXY1ciLCJtYWMiOiI3ZjI1OWMyNjljZTEwMjc5MjM0OWEyNDRlMmVmODU2MTFlOGFmZDJhYTZmNjAzOGNlZWNiNjM2YjkyOGJmMTNkIiwidGFnIjoiIn0=',
        'Connection': 'keep-alive',
        'Referer': 'https://www.oddsportal.com/football/argentina/liga-profesional/barracas-central-rosario-central-EXVtB08r/',
        'Cookie': 'op_lang=en; op_cookie-test=ok; XSRF-TOKEN=eyJpdiI6IlYxTS9EN3BXdWM0a3JzKytTV0tNMlE9PSIsInZhbHVlIjoiajVJYW8zanY4Q2lvb09qdm5UZXNidVJUNVdsKzU3dFQwaDJKM2diMGpSdG5VcUM2OXZISVlodWhxTGE3bVZDY1NleUZBNmd3MjNxbHFVc3RDTEd5TEV5OWJzdUoxOXBJVzI4M1ZnakhGOGtwM1VvSDZlTEE1aHRUc3hYeTllbzgiLCJtYWMiOiJiOGVlYTBkNzVlNDg5MTEzMGJlODdjYjgxMTlhNjkxZDQyOTkzN2RhYWJmYzI4MTI3Y2UzMTA1ODcyNWMxODk5IiwidGFnIjoiIn0^%^3D; oddsportalcom_session=eyJpdiI6ImhwbUE1NDAvcG8xNjM5YmlUbmcxekE9PSIsInZhbHVlIjoia0gyM2g1eXZFMUpEdGc3aWxQMjg2dGxOeGR5ODhENHdySitScHB2RnBjQnMyZTBVVXBNWmpabWFjMG50UGpPTXdEeDJ6VHBqa1NsSzJoLzc1OXZETGdwT05qSU9ud09DYktUVVZDbXR2Q3E0NTBjVUovNG1vZmJycElUTHM2RTEiLCJtYWMiOiJiYmY0NmZmMGFjYzdhMmViYmNiOTNhZjVmYWY2YjkzODQzZWU5MTNlZDMwMjMzM2E0MGRlNWU4ODAyNDQ0NDkxIiwidGFnIjoiIn0^%^3D; op_user_time_zone=2; op_user_full_time_zone=37; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jun+09+2023+16^%^3A23^%^3A09+GMT^%^2B0200+(Central+European+Summer+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=df1d7549-ca67-4cd7-b26e-8117066d9f55&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0004^%^3A1^%^2CSTACK42^%^3A1&geolocation=SI^%^3B061&AwaitingReconsent=false; _hjSessionUser_3147261=eyJpZCI6IjQ4MDI5YTJjLTBlMGUtNTRlNS05ZjVjLWY1YTM4ZjZkYTAwYyIsImNyZWF0ZWQiOjE2ODYzMTYwNzEzMjYsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample_3147261=0; _sg_b_v=3^%^3B717^%^3B1686320244; OptanonAlertBoxClosed=2023-06-09T13:07:52.663Z; eupubconsent-v2=CPtFxnAPtFxnAAcABBENDICsAP_AAAAAAChQJGtf_X__b2_j-_7_f_t0eY1P9_7_v-0zjhfdl-8N2f_X_L8X52M7vF36pqoKuR4ku3LBIQVlHOHcDUmw6okVryPsbk2cr7NKJ7PEmnMbO2dYGH9_n13T-ZKY7___f__z_v-v________7-3f3__p___-2_e_V_99zfn9_____9vP___9v-_9_3gAAAAAAAAAAAAD4AAABwkAIAGgC8xUAEBeYyACAvMdAEABoAGYAZQC8yEAIAMwAyiUAMAMwAygF5lIAgANAAzADKAXmAAA.f_gAAAAAAAAA; _ga=GA1.2.341376778.1686316070; _gid=GA1.2.2028750720.1686316073; _ga_5YY4JY41P1=GS1.1.1686318366.2.1.1686320632.14.0.0; _sg_b_n=1686316108842; _hjSession_3147261=eyJpZCI6Ijk5NTczZGQ0LTMzNTgtNDk0My1hYzkyLTQ4MzZmZjE3MTdmNSIsImNyZWF0ZWQiOjE2ODYzMTgzNjY4MzgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _sg_b_p=^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2Fbarracas-central-rosario-central-EXVtB08r^%^2F^%^2C^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2Fgimnasia-l-p-huracan-OWvTMc7f^%^2F^%^2C^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2Fgimnasia-l-p-huracan-OWvTMc7f^%^2F^%^2C^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2Fgimnasia-l-p-huracan-OWvTMc7f^%^2F^%^2C^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2Fgimnasia-l-p-huracan-OWvTMc7f^%^2F^%^2C^%^2Fregister^%^2Fre^%^2C^%^2F^%^2C^%^2Ffootball^%^2Fargentina^%^2Fliga-profesional^%^2F; op_user_login_id=440624; op_user_login_hash=38a85111bfccef6528177b48928e3927; op_user_logout=0; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkhVZzE4VE0yQ044VE1nZnBVcm9PeFE9PSIsInZhbHVlIjoiZXpaSitjOUVxdzVST1NPWC9ycHE2ZDEwb3NpTGZQR2N2N25oVkVDVHZIVSt4OEtXOFJ1bm4wYmMwcm1rTXZ1Ykpzb3VtOENDWDg0N0lteXFCb0xtcVBVODZldU9JUzhDeHNLZWk4eHA3RXhhTUNVeU9iTG13LzlWa2FjciszbkRwL3F1bmxyKzUrU2V6amN1eHQwYVhRPT0iLCJtYWMiOiJiOTVmYTY2MTM2ZjE4YmIxYjI0ZmVlMTM3NjYzNzM3YWVjYzIyY2ViYjU4MWViMDQ3NTg2YTg0ZjY1MmM4MDkxIiwidGFnIjoiIn0^%^3D; op_user_cookie=5501456865; op_user_hash=6f2bd3495dd5e9111c6bcc0423e46e56; op_user_time=1686320587; _gat_UA-821699-19=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
  matches_data = nu.make_request(url, headers)
  bookie_list = [{"Name":"W.Hill", "Matches": []}, {"Name":"Bet365", "Matches": []}, {"Name":"Pinncl", "Matches": []}]
  xhash_urls = []
  status_urls = []
  urls_1x2 = []
  fh_urls = []
  ggng_urls = []
  dnb_urls = []
  oddeven_urls = []
  xhash_rs = []
  if(matches_data and 'd' in matches_data and 'oddsData' in matches_data['d'] and matches_data['d']['oddsData']):
      event_list = [event for event in matches_data['d']['oddsData']]
      url_paths = extractURLPaths(base_url, event_list, country, league)
      for path in url_paths:
        xhash_urls.append(f"{base_url}{path}/")
      greenlets = [gevent.spawn(nu.make_requestHTML, url, headers1) for url in xhash_urls]
      gevent.joinall(greenlets)
      for greenlet in greenlets:
        xhash_rs.append(greenlet.value)

      xhashes = extractXHashes(xhash_rs, url_paths)
      for encodeId, data in xhashes.items():
        status_urls.append(f"https://www.oddsportal.com/feed/postmatch-score/1-{encodeId}-{data['xhash']}.dat")
        urls_1x2.append(f"https://www.oddsportal.com/feed/match-event/1-1-{encodeId}-1-2-{data['xhash']}.dat")
        fh_urls.append(f"https://www.oddsportal.com/feed/match-event/1-1-{encodeId}-1-3-{data['xhash']}.dat")
        ggng_urls.append(f"https://www.oddsportal.com/feed/match-event/1-1-{encodeId}-13-2-{data['xhash']}.dat")
        dnb_urls.append(f"https://www.oddsportal.com/feed/match-event/1-1-{encodeId}-6-2-{data['xhash']}.dat")
        oddeven_urls.append(f"https://www.oddsportal.com/feed/match-event/1-1-{encodeId}-10-2-{data['xhash']}.dat")
      
      status_rs = nu.fetch_data(status_urls, headers)
      u1x2_rs = nu.fetch_data(urls_1x2, headers2)
      fh_rs = nu.fetch_data(fh_urls, headers2)
      ggng_rs = nu.fetch_data(ggng_urls, headers2)
      dnb_rs = nu.fetch_data(dnb_urls, headers)
      oddeven_rs = nu.fetch_data(oddeven_urls, headers)

      bookie_list = oddsportalExtractData(status_rs, u1x2_rs, fh_rs, ggng_rs, dnb_rs, oddeven_rs, xhashes, tag)
  return bookie_list

def createMatch(odds, fh, ggng, dnb, oe, name):
    fh_data = []
    dnb_data = []
    ggng_data = []
    oe_data = []
    ov = {}
    un = {}
    match = []
    if isinstance(ggng, list) and ggng:
        ggng_data.extend((ggng[0], ggng[1]))
    elif isinstance(ggng, dict) and ggng: 
        ggng_data.extend((ggng['0'], ggng['1']))

    if isinstance(fh, list) and fh:
        fh_data.extend((fh[0], fh[2], fh[1]))
    elif isinstance(fh, dict) and fh: 
        fh_data.extend((fh['0'], fh['2'], fh['1']))

    if isinstance(dnb, list) and dnb:
        dnb_data.extend((dnb[0], dnb[1]))
    elif isinstance(dnb, dict) and dnb: 
        dnb_data.extend((dnb['0'], dnb['1']))

    if isinstance(oe, list) and oe:
        oe_data.extend((oe[0], oe[1]))
    elif isinstance(oe, dict) and oe: 
        oe_data.extend((oe['0'], oe['1']))

    if isinstance(odds, list):
        match = Match(name=name, home_odd=odds[0], away_odd=odds[2], draw_odd=odds[1], over=ov, under=un, dnb=dnb_data,
                fh1x2=fh_data, ggng=ggng_data, odd_even=oe_data)
    elif isinstance(odds, dict):
        match = Match(name=name, home_odd=odds['0'], away_odd=odds['2'], draw_odd=odds['1'], over=ov, under=un, dnb=dnb_data,
                fh1x2=fh_data, ggng=ggng_data, odd_even=oe_data)
    return match

def extractURLPaths(url, event_list, country, league):
    url_paths = []
    response = nu.make_requestHTML(url, headers)
    if(response):
      soup = BeautifulSoup(response, 'html.parser')
      next_matches_tag = soup.find('next-matches')
      if(next_matches_tag):
        comp_data = next_matches_tag.get(':comp-data')
      else:
        comp_data = []
      for event in event_list:
          if(not comp_data):
            continue
          start_index = comp_data.find('encodeEventId":"'+event+'"')
          end_index = start_index + 555
          text = comp_data[start_index:end_index]
          pattern = rf'url":"\\/football\\/{country}\\/{league}\\/([^\\/]+)-([A-Za-z0-9]+)\\/'
          match = re.search(pattern, text)
          if match:
              path = match.group(1)
              encodeId = match.group(2)
              url_paths.append(f"{path}-{encodeId}")
    return url_paths
def extractXHashes(html_rs, url_paths):
    xhashes = {}
    for i in range(0, len(html_rs)):
        if(not html_rs[i]):
           continue
        soup = BeautifulSoup(html_rs[i], 'lxml')
        name = soup.title.get_text().split(" Betting ")[0]
        event_tag = soup.find('event')
        event_html = str(event_tag)
        # Use regular expressions to find the 'xhash' value
        xhash_pattern = r'xhash&quot;:&quot;(.*?)&quot;'
        xhash_match = re.search(xhash_pattern, event_html)
        if xhash_match:
            xhash = xhash_match.group(1)
            encodeId = url_paths[i][-8:]
            xhashes[encodeId] = {'xhash': urllib.parse.unquote(xhash), 'match_name': name}
        else:
            print("No 'xhash' value found in the HTML.")
    return xhashes

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeOddsportalALPTeamNames,
        "BSA": normalizeOddsportalBSATeamNames,
        "BSB": normalizeOddsportalBSBTeamNames,
        "CPA": normalizeOddsportalCPATeamNames,
        "ELP": normalizeOddsportalELPTeamNames,
        "PL1": normalizeOddsportalPL1TeamNames,
        "USM": normalizeOddsportalUSMTeamNames,
        'EPL': normalizeOddsportalEPLTeamNames,
        'EFL': normalizeOddsportalEFLTeamNames,
        'EL1': normalizeOddsportalEL1TeamNames,
        'EL2': normalizeOddsportalEL2TeamNames,
        'SP': normalizeOddsportalSPTeamNames,
        'IFD': normalizeOddsportalIFDTeamNames,
        'IPD': normalizeOddsportalIPDTeamNames,
        'SPD': normalizeOddsportalSPDTeamNames,
        'SSD': normalizeOddsportalSSDTeamNames,
        'FL1': normalizeOddsportalFL1TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeOddsportalALPTeamNames(team_name):
  return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeOddsportalBSATeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeOddsportalBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeOddsportalCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeOddsportalELPTeamNames(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeOddsportalPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeOddsportalUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeOddsportalEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeOddsportalEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeOddsportalEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeOddsportalEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeOddsportalSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeOddsportalIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeOddsportalIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeOddsportalSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeOddsportalSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeOddsportalFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]

if __name__ == '__main__':
    bookie_list = EPL()
    for bookie in bookie_list:
        pd.set_option('display.max_colwidth', None)
        dF = pd.DataFrame.from_dict(bookie)
        print(dF)