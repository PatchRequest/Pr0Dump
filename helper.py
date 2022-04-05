import requests


def loginUser(username,password):
    print("[*] Loggin in for user: " + username)
    token, captchaSolution= solveCaptche()
    data = {
        "name":username,
        "password":password,
        "token":token,
        "captcha":captchaSolution
    }
    x = requests.post('https://pr0gramm.com/api/user/login', data=data)
    print("[+] Logged in for user: " + username)
    return x
    
def solveCaptche():
    print("[*] Requesting Captcha")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',

    }
    x = requests.get('https://pr0gramm.com/api/user/captcha',headers=headers)
    xJson = x.json()
    
    token = xJson['token']
    captache = xJson['captcha']
    print(captache)
    captchaSolution = input("Captcha: ")

    return token, captchaSolution