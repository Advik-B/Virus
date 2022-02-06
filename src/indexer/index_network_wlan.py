import subprocess
import re


def show_profile_list(
    command: list = ("netsh", "wlan", "show", "profiles"),
    regex: str = r"(?:Profile\s*:\s(.*))",
):
    result_raw = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    result_raw_decoded = result_raw.stdout.decode("utf-8").replace("\r", "")
    return re.findall(regex, result_raw_decoded)


def find_wifi_passwd(SSID: str) -> str:
    result_raw = subprocess.run(
        ["netsh", "wlan", "show", "profile", SSID, "key=clear"],
        stdout=subprocess.PIPE,
        shell=True,
    )
    result_raw_decoded = result_raw.stdout.decode("utf-8").replace("\r", "")
    return re.search(r"KeyC:\s(.*)", result_raw_decoded)

print(find_wifi_passwd("72-F-2.4Ghz"))
