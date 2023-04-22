from concurrent.futures import ThreadPoolExecutor
from msmcauth import UserProfileInformation
from httpx import Response
import msmcauth
import random
import string
import httpx

def main(kek: str) -> None:
    try:
        username, password = kek.split(":")
     #   session: Session = Session()
     ##   session.proxies = {
     #       "https": f"socks5h://if u want"
     #   }
     #   proxies: str = f"socks5://if u want"
        login: UserProfileInformation = msmcauth.login(username, password)#, session)
        access_token: str = login.access_token
        url: str = "https://api.minecraftservices.com/minecraft/profile"
        resp: Response = httpx.post(url, json={
            "profileName": "".join(random.choices(string.ascii_letters + string.digits, k=10))
        }, headers={
            "authorization": f"Bearer {access_token}"
        })#, proxies=proxies)
        if 'Request blocked.' in resp.text:
            raise "Failed to set Name."
        print("set name to " + username)
        open("alts-named.txt", 'a+').write(f"{kek}\n")
    except Exception as ex:
        print(ex)
        main(kek)


if __name__ == '__main__':
    credentials: list[str] = open("alts.txt").read().splitlines()
    with ThreadPoolExecutor(max_workers=5) as tpe:
        tpe.map(main, credentials)
