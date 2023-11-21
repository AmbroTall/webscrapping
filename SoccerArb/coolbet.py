import pandas as pd
from match import Match
from thefuzz import process
from db import *
import time
import json
import network_utils as nu

country = "MK"
headers = {
    'authority': 'www.coolbet.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json; charset=utf-8',
    'cookie': 'incap_ses_151_723517=ZEXwJztGjQ0vsj9KJXYYAr9IqGQAAAAAwPf8Ip4ea5nM1lOaeLYpkg==; nlbi_723517=wMFgHN5GvGY6gGn7mItahgAAAABUxT6LxXuTMNEHqPWqGLKx; incap_sh_723517=z0ioZAAAAABZjAgIBgAIz5GhpQZNw9X9xboS1tPmd6jfyxzs; visid_incap_723517=b8MlnLPXScqXOk3GSH99/L9IqGQAAAAAQkIPAAAAAACArnitATYlAcHUNfYm9iuFnhOiV7JJX/mE; _cq_duid=1.1688750291.TCAN9nB9ulSBkK4P; _cq_suid=1.1688750291.wCEbzoqcL2bB75QY; uuid=7141d482-ae8e-4e9a-9646-3026792ece60; CookieConsent={stamp:%27g4UX8dvzQH3tslbAoj7Osm3+45lKksXegvzU4FJso+0Ym6LPkoqVqw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:2%2Cutc:1688750304586%2Cregion:%27gb%27}; _gcl_au=1.1.1761597735.1688750346; _gid=GA1.2.624959962.1688750349; _tguatd={"sc":"www.coolbet.com"}; _tgpc=e262c946-9abd-58bd-b207-67427c6a79a4; _tgidts={"sh":"d41d8cd98f00b204e9800998ecf8427e","ci":"0309206e-88a7-5869-b39c-97374bae0e01","si":"cc034bb5-aaa4-5cee-9b31-4249e79388cb"}; _tgsc=cc034bb5-aaa4-5cee-9b31-4249e79388cb:-1; _tgtim=cc034bb5-aaa4-5cee-9b31-4249e79388cb:1688750714546:-1; reese84=3:TAmWaU8FIJlxMbDccqlotw==:c15MyG6A33gkdiFw05DLroFKiMjnaW1ikr7YJc1lFTsaua/E4MrZ2vCabhc5fkCmlXp/giCixPi4PIh0sT3q66A50R1O9t+uMhfgdhqcj+VCtKFLtnq0DC7Klx9O2UwKuPM6D1GaHBKB1N08wWB75++vKYZuHQszVFmrOp3ZYgg5IVOLnQCn9h2pQfIITzqdIjFdEy2irJb039gc8mqmzMqEfKMjlGZc1b9GTN/oWM1xgWm+H6CEPdE6yJO3qpLWaMLSe9M1T050yP/2hJf0XiqHHQvvIem/8mUPMMrSwXt4L9T9wE7ZtFol5ACgXK8NgT1+83ZCfFAKDyRS5cc76Opz1HjCPqNem0LJQKbaTtcAHSk6bJHzueVvZsJzZeigWc8PeFoVLkjY6J0vXBSwDCrNJtbi0KaE6kiaX9KAYE2E7afrxcmphxjPebKcVEfbHivurAYOJN/Cw0OyrQFulYCF6X3rQq+TXiB/k+71WEb2dqBjmdmU9or+KpwElPQiddQZ/7IqhtMllwk7mNz/sO8rmcHBdIOY7+KukBUNZyLzpGUGBAES5vkE2dyNDMf1:9XSugJvvvDcfz2tSndozvtC44TtuReanaNn5mShSny8=; nlbi_723517_2147483392=tiERIxBzimlqadFRmItahgAAAAAuvHV29zfQb+oQ9Fzez+hk; _tglksd={"s":"cc034bb5-aaa4-5cee-9b31-4249e79388cb","st":1688750684750,"sod":"www.coolbet.com","sodt":1688750684750,"sods":"c","sodst":1688752207907}; _dc_gtm_UA-73464905-2=1; _ga=GA1.1.1284563082.1688750347; _ga_WDFEQ1B9HW=GS1.1.1688750346.1.1.1688752208.39.0.0; _tgsid={"lpd":"{\\"lpu\\":\\"https://www.coolbet.com%2Fen%2Fsports%2Fmatch%2F2573695\\",\\"lpt\\":\\"Coolbet%20Loading...\\"}","ps":"68d350dd-7bc8-47b8-a48f-b623b0611bfb","ec":"5","pv":"1"}; incap_ses_1092_723517=0FVcYAF9EAFU/pdhJJEnD5dQqGQAAAAA7j0Vp77KUv4A+wB4isBcAw==',
    'if-none-match': 'W/"1c7f4-SwXoQq42QTAv1DKZSZn2IWJW3dw"',
    'referer': 'https://www.coolbet.com/en/sports/football/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-device': 'DESKTOP'
}
def coolbetALP():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18956&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "ALP")
def coolbetBSA():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=25152&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "BSA")
def coolbetBSB():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=20501&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "BSB")
def coolbetPP():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19508&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "PP")
def coolbetELP():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18974&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "ELP")
def coolbetPL1():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19383&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "PL1")
def coolbetUSD():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19889&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "USD")
def coolbetBPD():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18961&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "BPD")
def coolbetMLM():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19904&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "MLM")
def coolbetUSM():
    url = f"https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19093&country={country}&isMobile=0&language=en&layout=EUROPEAN&province"
    return coolbetGetData(url, headers, "USM")

def coolbetEPL():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18975&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "EPL")
def coolbetEL1():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18770&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "EL1")
def coolbetEL2():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18982&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "EL2")
def coolbetSP():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19045&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "SP")
def coolbetSC():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19048&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "SC")
def coolbetIFD():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18916&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "IFD")
def coolbetIPD():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18910&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "IPD")
def coolbetSPD():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19104&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "SPD")
def coolbetSSD():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=19103&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "SSD")
def coolbetFL1():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18849&country={country}&isMobile=0&language=en&layout=EUROPEAN&province'
    return coolbetGetData(url, headers, "FL1")
def coolbetFL2():
    url = f'https://www.coolbet.com/s/sbgate/sports/fo-category/?categoryId=18902&country={country}&isMobile=0&language=en&layout=EUROPEAN&limit=6&province'
    return coolbetGetData(url, headers, "FL2")

def coolbetGetData(url, headers, tag):
    matchdata = nu.make_requestOld(url, headers)
    coolbet_dict = {"Name":"Coolbet", "Matches": []}
    if(matchdata):
        event_list = [event['id'] for event in matchdata[0]['matches'] if event['status'] != 'LIVE']
        coolbet_dict = coolbetExtractData(event_list, tag)
    return coolbet_dict

def coolbetExtractData(event_list, tag):
    matches = []
    corrected_matches = []
    for event in event_list:
        market_ids = []
        time.sleep(0.3)
        url = f"https://www.coolbet.com/s/sbgate/sports/fo-market/sidebets?country=MK&language=en&layout=EUROPEAN&matchId={event}&matchStatus=OPEN&province"
        headers = {
            'authority': 'www.coolbet.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json; charset=utf-8',
            'cookie': 'visid_incap_723517=2m8sRFxeSVSvzXTeAer9VxkFp2QAAAAAQUIPAAAAAADcJO/TEhiirL2fJsVdZHQo; _cq_duid=1.1688667420.fyuP3kgN8xQZmVhC; uuid=fe52771e-580f-41f8-b413-2208797c6fb8; incap_ses_873_723517=88MRav6nhUCsW9qCnIUdDNFHqGQAAAAAgoCnXDVSUmOtmR3jsw2quw==; nlbi_723517=K2dtf4LMUjNS1rr0mItahgAAAAAYqsozPuiiyBmdlS/t81RY; _cq_suid=1.1688750037.00N0fEX6F4zsc6Fo; CookieConsent={stamp:%277Qn6YacOvjX8xAlIp4HifdnoO9CdvUJ3+OAEye2nr2rKJXsYtptJzQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:2%2Cutc:1688750117594%2Cregion:%27gb%27}; _gcl_au=1.1.918369140.1688750193; _gid=GA1.2.1184022370.1688750194; incap_ses_1092_723517=QlmQfyUMfXEVZpxhJJEnDwdZqGQAAAAAsbZGGVLvvZihq0/x6kY7Qg==; _fbp=fb.1.1688754442378.691229413; _tgpc=d895932f-e123-5651-9a8e-85e8906cb2b1; reese84=3:OCeoUMtqhlLsqBEMbxmJvw==:BeDLQZ1WD6dM0amlBqGaaxleWyWVubtf0ZjbNSIPEngrJwHLcRwbbHN3a7eqE/vvWUnNVRV0ewmwRH7xiTFXEF3LbuvhBZj6KQpQIERjZSE5hzWZ+BjG+NTFyfAyRPFyVc0QdgydqbNDEPVqVtAn5KlPJG2Xwy1E+Lrkrb7W/fxbyOZJReKLLvmtMbzhmvcWDev5UDJVUudsdsVkYrcxrQJCg/N1ZAX9wqJFJXI/wTByGQCRaVgYkpTWeoZkaTXRGznflAqi/mR9h5GVq8hiINV3rGam87mzEhIoDY3zdXVvQmHymvbqVKPr32SUSe+SkEup4f9oUq6VJc+KbJK8O9kYrPnfL3QiRXAHGiIMMKTStk7n3omlRgs3kk3SqE+KEp/DMu+6c6gRtOgysgbm6iOpFCZ2wqABITGGsyuYocsjsGEYUNRrG72jynFPSBeKQpmKS6t8yEgLF3b5FVYXuDFYXA0PJzDGgKzkqTM6gETYvWyNDKm4BFeuxXLgqDSGPbPIVF9hJMQhMXwcn1mSl8z1PsvG3xYhHYTlVJ+0308=:SEwA9Q6CjH0S5T2FVK17DXkCbf+n1lTVupQwzHbwBis=; nlbi_723517_2147483392=ltq0QQPspE+mEjcFmItahgAAAAAl9vABTCW2LHTqy60rUGhS; _tguatd={"sc":"(direct)"}; _tgidts={"sh":"d41d8cd98f00b204e9800998ecf8427e","ci":"2ba8a469-4a8d-5c66-aac4-99e481708186","si":"8e1b9dfc-c0f0-5632-8b8e-1daffb9b58c1"}; _tglksd={"s":"8e1b9dfc-c0f0-5632-8b8e-1daffb9b58c1","st":1688761834266,"sod":"(direct)","sodt":1688754442578,"sods":"o","sodst":1688761834266}; _tgsc=8e1b9dfc-c0f0-5632-8b8e-1daffb9b58c1:-1; _tgsid={"lpd":"{\\"lpu\\":\\"https://www.coolbet.com%2Fen%2Fsports%2Fmatch%2F2573695\\",\\"lpt\\":\\"Sports%20by%20Coolbet%3A%20The%20Most%20Transparent%20Sportsbook%20Online\\"}","ps":"3ac715bd-8161-474d-878b-b54aad71cd03","ec":"4","pv":"1"}; _tgtim=8e1b9dfc-c0f0-5632-8b8e-1daffb9b58c1:1688761839698:-1; _ga=GA1.2.923609439.1688750193; _dc_gtm_UA-73464905-2=1; _ga_WDFEQ1B9HW=GS1.1.1688761830.3.1.1688762220.46.0.0; incap_ses_1092_723517=D83bdVKtgypnsy1iJJEnDyYwqWQAAAAA8EtcRAOyG7jhqQDDGu1pGg==; visid_incap_723517=viF9PAHXRA6lAAidqfsH/hlZqGQAAAAAQUIPAAAAAAB7BHcXuS7AoM/jNxFuWij/',
            'dnt': '1',
            'pragma': 'no-cache',
            'referer': 'https://www.coolbet.com/en/sports/match/2573696',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-device': 'DESKTOP'
        }
        match_data = nu.make_requestOld(url, headers)
        if(not match_data or not 'markets' in match_data or not 'match' in match_data):
           continue
        market_groups = match_data['markets']
        h_odd = 0
        a_odd = 0
        d_odd = 0
        over = {}
        under = {}
        fg = []
        dc = []
        dnb = []
        ggng = []
        fh_m = []
        sh_m = []
        ltts = []
        fh_fg = []
        fh_dnb = []
        sh_dnb = []
        fh_ggng = []
        sh_ggng = []
        odd_even = []
        fh_odd_even = []
        for market_group in market_groups:
           for market in market_group['markets']:
                market_ids.append(market['id'])
                if(market['name'] == 'Match Result (1X2)' and len(market['outcomes']) == 3):
                    h_odd = market['outcomes'][0]['id']
                    a_odd = market['outcomes'][2]['id']
                    d_odd = market['outcomes'][1]['id']
                if(market['name'] == 'Total Goals Over / Under' and market['line'] == '2.5' and len(market['outcomes']) == 2):
                    over[2.5] = market['outcomes'][0]['id']
                    under[2.5] = market['outcomes'][1]['id']
                if(market['name'] == 'Both Teams To Score' and len(market['outcomes']) == 2):
                    ggng = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '1st Half Both Teams To Score' and len(market['outcomes']) == 2):
                    fh_ggng = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '2nd Half Both Teams To Score' and len(market['outcomes']) == 2):
                    sh_ggng = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == 'Draw No Bet' and len(market['outcomes']) == 2):
                    dnb = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '1st Half Draw No Bet' and len(market['outcomes']) == 2):
                    fh_dnb = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '2nd Half Draw No Bet' and len(market['outcomes']) == 2):
                    sh_dnb = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == 'Double Chance' and len(market['outcomes']) == 3):
                    dc.extend((market['outcomes'][0]['id'], market['outcomes'][2]['id'], market['outcomes'][1]['id']))
                if(market['name'] == 'First Team To Score' and len(market['outcomes']) == 3):
                    fg = [market['outcomes'][0]['id'], market['outcomes'][1]['id'], market['outcomes'][2]['id']]
                if(market['name'] == '1st Half First Team To Score' and len(market['outcomes']) == 3):
                    fh_fg = [market['outcomes'][0]['id'], market['outcomes'][1]['id'], market['outcomes'][2]['id']]
                if(market['name'] == 'Last Team to Score' and len(market['outcomes']) == 3):
                    ltts = [market['outcomes'][0]['id'], market['outcomes'][1]['id'], market['outcomes'][2]['id']]
                if(market['name'] == 'Odd or Even Goals' and len(market['outcomes']) == 2):
                    odd_even = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '1st Half Odd Or Even Goals' and len(market['outcomes']) == 2):
                    fh_odd_even = [market['outcomes'][0]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '1st Half Result' and len(market['outcomes']) == 3):
                    fh_m = [market['outcomes'][0]['id'], market['outcomes'][2]['id'], market['outcomes'][1]['id']]
                if(market['name'] == '2nd Half Result' and len(market['outcomes']) == 3):
                    sh_m = [market['outcomes'][0]['id'], market['outcomes'][2]['id'], market['outcomes'][1]['id']]

        home_team = match_data['match']['home_team_name']
        away_team = match_data['match']['away_team_name']
        if(home_team == None or away_team == None):
           continue
        name = f"{normalizeName(tag, home_team)} - {normalizeName(tag, away_team)}"
        match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd, over=over, under=under, dc=dc, dnb=dnb, ggng=ggng,
                      fh_ggng=fh_ggng, fh1x2=fh_m, sh1x2=sh_m, fh_dnb=fh_dnb, fg=fg, fh_fg=fh_fg, ltts=ltts, odd_even=odd_even,
                      fh_odd_even=fh_odd_even, sh_ggng=sh_ggng, sh_dnb=sh_dnb)
        matches.append(match)
        corrected_match = ids_to_odds(match, market_ids, headers)
        corrected_matches.append(corrected_match)

    coolbet_dict = {"Name":"Coolbet", "Matches": corrected_matches}
    return coolbet_dict

def ids_to_odds(match, market_ids, headers):
    url = "https://www.coolbet.com/s/sb-odds/odds/current/fo"
    payload = "{\"where\":{\"market_id\":{\"in\":[]}}}"
    payload_dict = json.loads(payload)  # Convert the payload string to a dictionary
    payload_dict['where']['market_id']['in'] = market_ids  # Update the market ID list
    new_payload = json.dumps(payload_dict)
    ids = nu.make_requestOld(url, headers, new_payload, post=True)
    if(ids):
        keys = ids.keys()
        if(match.home_odd and match.away_odd and match.draw_odd and str(match.home_odd) in keys and str(match.away_odd) in keys and str(match.draw_odd) in keys):
            match.home_odd = ids[str(match.home_odd)]['value']
            match.away_odd = ids[str(match.away_odd)]['value']
            match.draw_odd = ids[str(match.draw_odd)]['value']
        if(2.5 in match.over and 2.5 in match.under and match.over[2.5] and match.under[2.5] and str(match.over[2.5]) in keys and str(match.under[2.5]) in keys):
            match.over[2.5] = ids[str(match.over[2.5])]['value']
            match.under[2.5] = ids[str(match.under[2.5])]['value']
        if(len(match.ggng) == 2 and str(match.ggng[0]) in keys and str(match.ggng[1]) in keys):
            match.ggng = [ids[str(match.ggng[0])]['value'], ids[str(match.ggng[1])]['value']]
        if(len(match.fh_ggng) == 2 and str(match.fh_ggng[0]) in keys and str(match.fh_ggng[1]) in keys):
            match.fh_ggng = [ids[str(match.fh_ggng[0])]['value'], ids[str(match.fh_ggng[1])]['value']] 
        if(len(match.sh_ggng) == 2 and str(match.sh_ggng[0]) in keys and str(match.sh_ggng[1]) in keys):
            match.sh_ggng = [ids[str(match.sh_ggng[0])]['value'], ids[str(match.sh_ggng[1])]['value']] 
        if(len(match.dnb) == 2 and str(match.dnb[0]) in keys and str(match.dnb[1]) in keys):
            match.dnb = [ids[str(match.dnb[0])]['value'], ids[str(match.dnb[1])]['value']] 
        if(len(match.fh_dnb) == 2 and str(match.fh_dnb[0]) in keys and str(match.fh_dnb[1]) in keys):
            match.fh_dnb = [ids[str(match.fh_dnb[0])]['value'], ids[str(match.fh_dnb[1])]['value']] 
        if(len(match.sh_dnb) == 2 and str(match.sh_dnb[0]) in keys and str(match.sh_dnb[1]) in keys):
            match.sh_dnb = [ids[str(match.sh_dnb[0])]['value'], ids[str(match.sh_dnb[1])]['value']] 
        if(len(match.dc) == 3 and str(match.dc[0]) in keys and str(match.dc[1]) in keys and str(match.dc[2]) in keys):
            match.dc = [ids[str(match.dc[0])]['value'], ids[str(match.dc[1])]['value'], ids[str(match.dc[2])]['value']]
        if(len(match.fg) == 3 and str(match.fg[0]) in keys and str(match.fg[1]) in keys and str(match.fg[2]) in keys):
            match.fg = [ids[str(match.fg[0])]['value'], ids[str(match.fg[2])]['value'], ids[str(match.fg[1])]['value']]
        if(len(match.fh_fg) == 3 and str(match.fh_fg[0]) in keys and str(match.fh_fg[1]) in keys and str(match.fh_fg[2]) in keys):
            match.fh_fg = [ids[str(match.fh_fg[0])]['value'], ids[str(match.fh_fg[2])]['value'], ids[str(match.fh_fg[1])]['value']]
        if(len(match.ltts) == 3 and str(match.ltts[0]) in keys and str(match.ltts[1]) in keys and str(match.ltts[2]) in keys):
            match.ltts = [ids[str(match.ltts[0])]['value'], ids[str(match.ltts[2])]['value'], ids[str(match.ltts[1])]['value']]
        if(len(match.fh1x2) == 3 and str(match.fh1x2[0]) in keys and str(match.fh1x2[1]) in keys and str(match.fh1x2[2]) in keys):
            match.fh1x2 = [ids[str(match.fh1x2[0])]['value'], ids[str(match.fh1x2[1])]['value'], ids[str(match.fh1x2[2])]['value']]
        if(len(match.sh1x2) == 3 and str(match.sh1x2[0]) in keys and str(match.sh1x2[1]) in keys and str(match.sh1x2[2]) in keys):
            match.sh1x2 = [ids[str(match.sh1x2[0])]['value'], ids[str(match.sh1x2[1])]['value'], ids[str(match.sh1x2[2])]['value']]
        if(len(match.odd_even) == 2 and str(match.odd_even[0]) in keys and str(match.odd_even[1]) in keys):
            match.odd_even = [ids[str(match.odd_even[0])]['value'], ids[str(match.odd_even[1])]['value']] 
        if(len(match.fh_odd_even) == 2 and str(match.fh_odd_even[0]) in keys and str(match.fh_odd_even[1]) in keys):
            match.fh_odd_even = [ids[str(match.fh_odd_even[0])]['value'], ids[str(match.fh_odd_even[1])]['value']] 
        return match
    else:
       pass

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeCoolbetALPTeamNames,
        "BSA": normalizeCoolbetBSATeamNames,
        "BSB": normalizeCoolbetBSBTeamNames,
        "PP": normalizeCoolbetPPTeamNames,
        "ELP": normalizeCoolbetELPTeamNames,
        "PL1": normalizeCoolbetPL1TeamNames,
        "USD": normalizeCoolbetUSDTeamNames,
        "BPD": normalizeCoolbetBPDTeamNames,
        "MLM": normalizeCoolbetMLMTeamNames,
        "USM": normalizeCoolbetUSMTeamNames,
        'EPL': normalizeCoolbetEPLTeamNames,
        'EL1': normalizeCoolbetEL1TeamNames,
        'EL2': normalizeCoolbetEL2TeamNames,
        'SP': normalizeCoolbetSPTeamNames,
        'SC': normalizeCoolbetSCTeamNames,
        'IFD': normalizeCoolbetIFDTeamNames,
        'IPD': normalizeCoolbetIPDTeamNames,
        'SPD': normalizeCoolbetSPDTeamNames,
        'SSD': normalizeCoolbetSSDTeamNames,
        'FL1': normalizeCoolbetFL1TeamNames,
        'FL2': normalizeCoolbetFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeCoolbetALPTeamNames(team_name):
  if(team_name == 'Unión de Santa Fe'):
     return 'Union'
  return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeCoolbetBSATeamNames(team_name):
  if team_name == 'Atlético Mineiro': return 'Atletico MG'
  return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeCoolbetBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeCoolbetPPTeamNames(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeCoolbetELPTeamNames(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeCoolbetPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeCoolbetUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeCoolbetBPDTeamNames(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeCoolbetMLMTeamNames(team_name):
  if(team_name == 'Pumas UNAM'):
     return 'Universidad Nacional'
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeCoolbetUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeCoolbetEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeCoolbetEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeCoolbetEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeCoolbetSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeCoolbetSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeCoolbetIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeCoolbetIPDTeamNames(team_name):
  if(team_name == 'UCD'): return "Uni College Dublin"
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeCoolbetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeCoolbetSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeCoolbetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeCoolbetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    coolbet_dict = coolbetBSA()
    pd.set_option('display.max_colwidth', None)
    coolbetdF = pd.DataFrame.from_dict(coolbet_dict)
    print(coolbetdF)