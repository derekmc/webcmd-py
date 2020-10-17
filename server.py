import cherrypy, string, random

ADMINPASSWORD_FILE = "adminpassword.txt"
ADMINPASSWORD_LEN = 16
class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

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
