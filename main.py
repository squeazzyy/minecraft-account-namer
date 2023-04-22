from concurrent.futures import ThreadPoolExecutor
from msmcauth import UserProfileInformation
from httpx import Response
import msmcauth
import random
import string
import httpx
from requests import Session


def is_username_used(username: str) -> bool:
    """
    Check if the given username has already been used and saved in "alts-named.txt" file.
    """
    with open("alts-named.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if username in line:
                return True
    return False


def main(kek: str) -> None:
    with open("proxies.txt", "r") as f:
        proxies = f.read().splitlines()
    f.close()
    proxy = random.choice(proxies)
    proxysplit = proxy.split(':')
    usernametoacc = "squeazzy_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    try:
        username, password = kek.split(":")
        with open("alts.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if username not in line:
                    f.write(line)
            f.truncate()
        session: Session = Session()
        session.proxies = {
            "https": f"{proxy}"
        }
        proxies: str = f"{proxy}"
        login: UserProfileInformation = msmcauth.login(username, password)
        access_token: str = login.access_token
        url: str = "https://api.minecraftservices.com/minecraft/profile"
        resp: Response = httpx.post(url, json={
            "profileName": usernametoacc
        }, headers={
            "authorization": f"Bearer {access_token}"
        })
        if 'Request blocked.' in resp.text:
            raise "Failed to set Name."
        print("set name to " + username + " and username name is: " + usernametoacc)
        open("alts-named.txt", 'a+').write(f"{kek} | {usernametoacc}\n")
    except Exception as ex:
        print(ex)
        main(kek)

if __name__ == '__main__':
    credentials: list[str] = open("alts.txt").read().splitlines()
    with ThreadPoolExecutor(max_workers=25) as tpe:
        tpe.map(main, credentials)
