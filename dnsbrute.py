import dns.resolver

res = dns.resolver.Resolver()
file = open("../wordlist/common.txt", "r")
subdoms = file.read().splitlines()
target = "bancocn.com"

for subdom in subdoms:
    try:
        sub_target = subdom + "." + target
        response = res.resolve(sub_target , "A")
        for ip in response:
            print(sub_target, "->", ip)
    except:
        pass