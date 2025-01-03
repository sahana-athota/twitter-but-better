import client
import encryptionfile as enc
import tagmanagement as tg
import userdetails
def user_insertion(username,password,topics):
    topicsnew = topics +',education,fashion,sports'
    client.sqlquery(f"insert into user_info values(NULL,'{username}','{enc.encrypt_message(password)}','{topicsnew}');")
    print('tnew',topicsnew)
    tg.new_user(username)

def getid(username):
    return eval(client.sqlquery(f"select user_id from user_info where username = '{username}'")[0])[0]

def get_hashtags(post_id):
    return ((eval(client.sqlquery(f"select hashtag from all_posts where post_id={post_id}")[0]))[0]).split(',')

def returnpostid_hashtag(hashtag):
    return [eval(i)[0] for i in client.sqlquery(f"select post_id from all_posts where hashtag like '%{hashtag}%'")[:-1]]

def return_username_postcontents(text):
    return [eval(i)[0] for i in client.sqlquery(f"select username from all_posts where text like '%{text}%'")[:-1]]

def return_hashtags_with_username(username):
    return [eval(i)[0] for i in client.sqlquery(f"select hashtag from tagmanagement where username like '%{username}%'")[:-1]]

def return_dislikedhashtags_with_username(username):
    return [eval(i)[0] for i in client.sqlquery(f"select disliked_hashtags from tagmanagement where username = '{username}'")[:-1]]

def getpassword(username):
    return enc.decrypt_message(eval(client.sqlquery(f"select password from user_info where username = '{username}'")[0])[0])

def gettopics(username):
    return ((eval(client.sqlquery(f"select topics from user_info where username = '{username}'")[0])[0]).split(','))

def getpostwithid(id):
    return [(eval(i))[0] for i in client.sqlquery(f"select text from all_posts where post_id = '{id}';")[:-1]]

def getuserposts_everyone():
    return [(eval(i))[0] for i in client.sqlquery(f"select text from all_posts;")[:-1]]

def getuserposts_postid(post_id):
    return [eval(client.sqlquery(f"select text from all_posts where post_id='{post_id}';")[0])[0]]

def getallposthashtagandpostid():
    l = [eval(i) for i in client.sqlquery(f"select post_id,hashtag from all_posts")[:-1]]
    return (l)

def checkinitialization():
    out = client.sqlquery("select hashtag from all_posts;")
    a = ''
    for i in ((out)[:-1]):
        if 'education,fashion,sports' in (eval(i)[0]):
            a = True
            break
        a = False
    if not a:
        import userdetails
        userdetails.insertpost('admin', 'Twitter But Better is so cool, more people should start using this!!!', 'education,fashion,sports')

def gethashtagswithpost(post):
    out = eval(client.sqlquery(f"select hashtag from all_posts where text = '{post}'")[:-1][0])[0].split(',')
    hashtags = ''
    for i in out:
        hashtags += '#'+i+' '

    return((hashtags))

def reset_password(username,currentpassword,newpassword):
    if userdetails.auth(username,currentpassword):
        try:
            client.sqlquery(f"update user_info set password = '{enc.encrypt_message(newpassword)}' where username = '{username}'")
        except:
            pass
        return True
    else:
        return False
def all_posts_by_a_user(username):
    l = [(i) for i in client.sqlquery(f"select text,hashtag from all_posts where username = '{username}'")][:-1]
    l1 = [eval(i) for i in l]
    return l1

def check_if_user_already_exists(username):
    return bool(eval(client.sqlquery(f"select count(*) from user_info where username ='{username}' group by username ")[:-1][0])[0])

#set-up
def installation():
    #client.sqlquery("drop DATABASE project;")
    '''client.sqlquery("CREATE DATABASE project;")
    client.sqlquery("use project")
    client.sqlquery("create table user_info(user_id int AUTO_INCREMENT,username varchar(20),password varchar(20),topics varchar(100), primary key(user_id,username));")
    client.sqlquery("create table all_posts (post_id int AUTO_INCREMENT ,user_id int, username varchar(20), text varchar(200), primary key(post_id));")
    '''
    client.sqlquery("use project")
    client.sqlquery("create table post_info(user_id int, tag varchar(16382))")