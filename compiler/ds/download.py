from time import sleep

from httpx import get
import subprocess
import sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://download-bbs.miyoushe.com"


def retry(func):
    def wrapper(*args, **kwargs):
        for _ in range(10):
            try:
                return func(*args, **kwargs)
            except Exception:
                print("retrying...")
                sleep(1)
                continue

    return wrapper


@retry
def get_version():
    return get(
        "https://bbs-api.miyoushe.com/misc/wapi/getLatestPkgVer?channel=miyousheluodi",
        verify=False,
    ).json()["data"]["version"]


version = get_version()
apk_url = f"{url}/app/mihoyobbs_{version}_miyousheluodi.apk"
print(f"download version {version} from {apk_url}")

command = f"wget -O mihoyobbs.apk {apk_url}"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

print("命令输出:\n", output.decode())
print("错误信息:\n", error.decode())
