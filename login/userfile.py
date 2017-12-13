user = input('Insert Username:\n')
passwd = input('Insert Password:\n')

with open('userdata','a') as f:
    f.write(user+':'+passwd)
