def connstr(connectionstring):
    parts = str.split(connectionstring, ";")
    for part in parts:
        a,b = str.split(part, "=")
        print("%s\n%s\n" % (a,b))
