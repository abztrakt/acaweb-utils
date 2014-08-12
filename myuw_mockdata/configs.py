userfile = open('top100usernames.txt', 'r')
usernames = [line.rstrip() for line in userfile.readlines()]
