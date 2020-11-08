
help = """ This is the help command """

def run(args, cmd):
   for i in range(1000):
     cmd.puts("i: %s" % i)
   cmd.puts("Help Command")
