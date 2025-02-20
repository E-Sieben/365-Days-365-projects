def encode_url(s: str) -> dict[str, str]:
    from string import ascii_letters as alphabet

    def remove_used_parts(words: str, toKill: list[str]) -> list[str]:
        for i in list(words):
            toKill.remove(i)
        toKill.remove(":")
        toKill.remove("/")
        toKill.remove("/")
        return toKill
    
    s: list[str] = list(s)
    o: dict[str, any] = {
        "protocol": "",
        "thirdLevelDomain": "",
        "secondLevelDomain": "",
        "topLevelDomain": "",
        "path": "",
        "params": {}
    }
    # ? Protocols
    for char in s:
            if char not in alphabet:
                break
            o["protocol"] = o["protocol"] + char
    s = remove_used_parts(o["protocol"], s)

    # ? Domains
    s = "".join(s)
    s = s.split("/")
    domains: list[str] = s[0].split(".")

    o["secondLevelDomain"] = domains[-2]
    o["topLevelDomain"] = domains[-1]
    
    if len(domains) == 3:
        o["thirdLevelDomain"] = domains[0]
    elif len(domains) >3:
        domains.pop(-1)
        domains.pop(-1)
        o["thirdLevelDomain"] = ".".join(domains)
    s.pop(0)

    # ? Paths
    s = "/".join(s)
    path: str = s.split("?")[0]
    o["path"] = path

    # ? Params
    params = s.split("?")[1].split("&")
    p: list[tuple[str, str]] = []
    for parameter in params:
        parameter: tuple[str, str] = parameter.split("=")
        p.append((parameter[0], parameter[1]))
    o["params"] = p
    return o

encodedURL = encode_url("https://ir-example.hi.microsoft.com/Reco/V1.0/New?modeling=adw&Count=5")
for element in encodedURL:
    print(f"{element}: {encodedURL[element]}")