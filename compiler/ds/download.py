from time import sleep

from httpx import get
import subprocess
import sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://download-bbs.miyoushe.com"


def retry(func):
    """retry 10 times"""
    def wrapper(*args, **kwargs) -> str:
        """retry 10 times"""
        for _ in range(10):
            try:
                return func(*args, **kwargs)
            except Exception:  # skipcq: PYL-W0703
                print("retrying...")
                sleep(1)
                continue
        return None

    return wrapper


@retry
def get_version():
    """get version"""
    return get(
        "https://bbs-api.miyoushe.com/misc/wapi/getLatestPkgVer?channel=miyousheluodi",
        verify=False,
    ).json()[
        "data"
    ]["version"]


version = get_version()
apk_url = f"{url}/app/mihoyobbs_{version}_miyousheluodi.apk"
print(f"download version {version} from {apk_url}")

command = f"wget -O mihoyobbs.apk {apk_url}"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # skipcq: BAN-B602
output, error = process.communicate()

print("命令输出:\n", output.decode())
print("错误信息:\n", error.decode())
