import client
import encryptionfile as enc

def getpassword(username): #returns password with username as parameter
    return enc.decrypt_message(eval(client.sqlquery(f"select password from user_info where username = '{username}'")[0])[0])

def gettopics(username): #returns a list of topics taking username as parameter
    return ((eval(client.sqlquery(f"select topics from user_info where username = '{username}'")[0])[0]).split(','))

def auth(username,password): #returns True or False depeding on if password and username match, takes username and password as required parameters
    return getpassword(username) == password

def getposts(username):
    return [(eval(i))[0] for i in client.sqlquery(f"select text from all_posts where username = '{username}'")[:-1]]

def insertpost(username,postcontents,posttags):
    client.sqlquery(f"insert into all_posts(username,text,hashtag) values('{username}','{postcontents}','{posttags}')")

def find_posttags_with_postcontent(postcontent):
    return eval(client.sqlquery(f"select hashtag from all_posts where text = '{postcontent}'")[0])[0]
def find_postid_with_postcontent(postcontent):
    return eval(client.sqlquery(f"select post_id from all_posts where text = '{postcontent}'")[0])[0]
print(find_postid_with_postcontent("elon musk is uncool"))
def finduser(username):
    c=client.sqlquery("select username from user_info;")
    a=[(eval(i))[0] for i in client.sqlquery("select username from user_info;")[:-1]]
    if username in a:
        return True
    else:
        return False
#print((find_posttags_with_postcontent(("Twitter But Better is so cool, more people should start using this!!!"))))
