import os, random, string, cherrypy
import CherrypyMako

CherrypyMako.setup()

root_dir = os.path.abspath( os.path.dirname(__file__))

ADMINPASSWORD_FILE = "adminpassword.txt"
ADMINPASSWORD_LEN = 16

class CommandHelper:
    def __init__(self):
        self.output = ""
        self.user = {} # user state
        self.app = {} # app state
        self.config = {} # config state

    def puts(self, s):
        if len(self.output) > 0:
            self.output += "\n"
        self.output += s

class Root(object):
    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        return {"name": "Billy Bob Thornton"}


    @cherrypy.expose
    @cherrypy.tools.mako(filename="console.html")
    def console(self, **params):
        command_text = params.get("command_input")
        cmdhelper = CommandHelper()
        if command_text != None:
            args = command_text.split()
                
            name = args[0]
            #print('name', name)
            module = None
            try:
                module = __import__("cmd." + name, fromlist=[None])
            except:
                cmdhelper.output = "No such command: '" + name + "'"
            #print('module', module)
            if module:
                if module.run:
                    module.run(args, cmdhelper)
                else:
                    raise "Module has no 'run' command"
        return {"output": cmdhelper.output}

    @cherrypy.expose
    @cherrypy.tools.mako(filename="admin/index.html")
    def admin(self, name="admin"):
        return {"name": name}



def gen_password(passlen):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(passlen))

def get_admin_password():
    try:
        password = open(ADMINPASSWORD_FILE).read()
    except IOError:
        password = gen_password(ADMINPASSWORD_LEN)
        open(ADMINPASSWORD_FILE, 'w').write(password)
    print("Admin Password: ", password)
    return password

admin_password = get_admin_password()

def validate_password(realm, username, password):
    if username == "admin" and password == admin_password:
       return True
    return False

if __name__ == '__main__':
   cherrypy.quickstart(Root(), '/', 'server.conf')
