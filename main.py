import requests
import json

def login_truthfinder():
    url = "https://api2.truthfinder.com/v1/authenticate"

    payload = json.dumps({
        "email": "cashpro@cashprohomebuyers.com",
        "password": "tech6491",
        "sessionId": "1d565c79",
        "sessionCreated": "1695449537"
    })
    headers = {
        'authority': 'api2.truthfinder.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'api-key': 'B7QbTIt3PtAID67cRtfQwrgzL0H3qU5buaxp17PoZ98',
        'app-id': 'tf-web',
        'content-type': 'application/json',
        'device-id': 'ba3be71b-83f8-4b43-bdcb-aa9d52eb8367',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/login',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=Ha6rl_lgi9_ykeTFajsG8MsCR9cX8XjlwiMoSim4Jlw-1695461085-0-AWaMc2g2Ov5Yq1cE/OQnxDikV26HN3oqwugWO6Akbv5kCH/Mt2kVMSDTt4N5yfscEh5oSzDZDTreRy21F7IsT56YSeg7zUd55YU6DPWpuWw4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.json()
    token = r['accessToken']
    print(token)
    return token

def truth_search_address(address):
    url = f"https://us-autocomplete-pro.api.smartystreets.com/lookup?auth-id=2617637110263865&search={address}"
    base = "https://www.truthfinder.com/dashboard/reports/"

    payload = {}
    headers = {
        'authority': 'us-autocomplete-pro.api.smartystreets.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/dashboard',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()['suggestions']
    if r:
        for address in r:
            print(address)
            if address['state'] == "GA":
                # ga:dalton:30721:3440freedomln
                url = f"{base}{address['state'].lower()}:{address['city'].lower()}:{address['zipcode']}:{address['street_line'].lower().replace(' ', '')}"
                return url
    return None

def report_truthfinder(address, jwt):
    url = f"https://api2.truthfinder.com/v1/me/records/{address.split('/')[-1]}/report?defer_extended_data=false"

    payload = {}
    headers = {
        'authority': 'api2.truthfinder.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'api-key': 'B7QbTIt3PtAID67cRtfQwrgzL0H3qU5buaxp17PoZ98',
        'app-id': 'tf-web',
        'authorization': f'Bearer {jwt}',
        'device-id': 'ba3be71b-83f8-4b43-bdcb-aa9d52eb8367',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/dashboard/reports/ga:dalton:30721:3440freedomln',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=wLzTbwmTQl8ITfizbSI_Eb9wxMELAsTMZP4qSWbO0Io-1695463099-0-AQGIa5LuYsilxmSwBqLwgLEG8IhjZCL7A80kzkPZelMRSDJ30G11U9kiGlyjjdToAVliim+cgxHXcpiuhMr9q4Wf+axArSwREeI+CHNy2w/V'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    print(r)
    return r

def send_request_truthfinder(jwt, url):
    headers = {
        'authority': 'api2.truthfinder.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'api-key': 'B7QbTIt3PtAID67cRtfQwrgzL0H3qU5buaxp17PoZ98',
        'app-id': 'tf-web',
        'authorization': f'Bearer {jwt}',
        'device-id': 'ba3be71b-83f8-4b43-bdcb-aa9d52eb8367',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/dashboard/reports/ga:dalton:30721:3440freedomln',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=wLzTbwmTQl8ITfizbSI_Eb9wxMELAsTMZP4qSWbO0Io-1695463099-0-AQGIa5LuYsilxmSwBqLwgLEG8IhjZCL7A80kzkPZelMRSDJ30G11U9kiGlyjjdToAVliim+cgxHXcpiuhMr9q4Wf+axArSwREeI+CHNy2w/V'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)

def main():
    address_db = '3440 Freedom Lane'
    jwt_token = login_truthfinder()
    url = truth_search_address(address_db)
    print(send_request_truthfinder(jwt_token, url))
    if url:
        r = report_truthfinder(url, jwt_token)
    return url

print(main())

