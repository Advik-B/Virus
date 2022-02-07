import re, subprocess, pywifi, time, typing

const = pywifi.const
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()


def getwifi_password(ssid: str) -> typing.Union[str, None]:
    """
    Get the password of the wifi
    :param ssid: SSID of the wifi
    :return: password of the wifi
    """

    cmd = ["netsh", "wlan", "show", "profile", ssid, "key=clear"]
    data = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    regex = re.compile(r"Key Content.*?(?P<pwd>\w+)")
    result = regex.search(data)
    return result.group("pwd") if result else None


def list_all_wifi():
    """
    List all the wifi
    :return: list of wifi
    """
    ifaces = wifi.interfaces()[0]
    ifaces.scan()
    time.sleep(1)
    results_ = ifaces.scan_results()
    results = []
    for result in results_:
        passwd = getwifi_password(result.ssid)
        results.append(
            {
                "ssid": result.ssid,
                "signal": result.signal * -1,
                "password": passwd or "Unknown",
            }
        )

    return results


# wifi_list = list_all_wifi()
# for wifi in wifi_list:
#     for key, value in wifi.items():
#         print("{} : {}".format(key, value))
#     print("+" * 50)


def connect_wifi(ssid: str, password: str) -> typing.Union["sucess", "failed"]:
    """
    Connect to the wifi
    :param ssid: SSID of the wifi
    :param password: password of the wifi
    :return
    """
    profile = pywifi.Profile()  # create profile instance
    profile.ssid = ssid  # name of client
    profile.auth = const.AUTH_ALG_OPEN  # auth algo
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # key management
    profile.cipher = const.CIPHER_TYPE_CCMP  # type of cipher
    profile.key = password

    ifaces = wifi.interfaces()[0]
    tmp_profile = ifaces.add_network_profile(profile)  # add new profile
    time.sleep(0.5)  # if script not working change time
    ifaces.connect(tmp_profile)  # trying to Connect
    time.sleep(0.5)  # 1s
    verify = ifaces.status()
    if verify == const.IFACE_CONNECTED:
        return "success"
    elif verify == const.IFACE_DISCONNECTED:
        return "failed"


def forget_wifi():
    """
    Remove all the wifi
    :return:
    """
    ifaces = wifi.interfaces()[0]
    ifaces.remove_all_network_profiles()
    time.sleep(0.5)


def refresh_wifi():
    global wifi, ifaces, time
    """
    Refresh the wifi
    :return:
    """
    ifaces = wifi.interfaces()[0]
    ifaces.scan()
    time.sleep(0.5)


def disconnect_wifi():
    """
    Disconnect the wifi
    :return:
    """
    ifaces = wifi.interfaces()[0]
    ifaces.disconnect()
    time.sleep(0.5)


def get_wifi_status():
    """
    Get the status of the wifi
    :return:
    """
    ifaces = wifi.interfaces()[0]
    if ifaces.status() == const.IFACE_CONNECTED:
        return "connected"
    elif ifaces.status() == const.IFACE_DISCONNECTED:
        return "disconnected"

def get_wifi_ssid():
    """
    Get the ssid of the wifi
    :return:
    """
    ifaces = wifi.interfaces()[0]
    return ifaces.current_bssid()
