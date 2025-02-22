
import ipaddress
import socket

def look_up_ip(ip: str) -> dict[str, str]:
    '''
    Takes in an IP-Address and returns information about the IP-Address
    '''

    info: list[str, str] = {
        "Address": ip
    }

    def get_public_info(ip: str) -> None:
        info["Domain Name"] = socket.getnameinfo((ip, 0), 0)[0]
    
    try:
        tip = ipaddress.ip_address(ip)
        if isinstance(tip, ipaddress.IPv4Address):
            info["Type"] = "IPv4"
        else:
            info["Type"] = "IPv6"
        
        if tip.is_private:
            info["Range"] =  "Private"
        elif tip.is_global:
            info["Range"] =  "Public"
            get_public_info(ip)
        else:
            info["Range"] =  "Special"
            get_public_info(ip)
    except ValueError:
        return "Invalid IP Address"
    
    return info

def pretty_print(d: dict[str, str]) -> None:
    print(d["Address"], ": ")
    for k, inst in enumerate(d):
        print(f"    {inst} is {d[inst]}")
        
pretty_print(look_up_ip("192.168.178.1"))
pretty_print(look_up_ip("1.1.1.1"))
pretty_print(look_up_ip("8.8.8.8"))
pretty_print(look_up_ip("2001:4860:4860::8888"))