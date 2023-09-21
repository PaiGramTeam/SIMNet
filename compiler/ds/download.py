from httpx import get

version = get("https://bbs-api.miyoushe.com/misc/wapi/getLatestPkgVer?channel=miyousheluodi").json()["data"]["version"]
apk_url = f"https://download-bbs.miyoushe.com/app/mihoyobbs_{version}_miyousheluodi.apk"
print(f"download version {version} from {apk_url}")
with open("mihoyobbs.apk", "wb") as f:
    f.write(get(apk_url).content)
