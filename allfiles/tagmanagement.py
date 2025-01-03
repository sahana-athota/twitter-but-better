import mysql.connector
import userdetails
import client


def new_user(username):
    client.sqlquery(f"insert into tagmanagement values('{username}','education,sports,fashion,','')")

    
def gettags(postid):
    op=client.sqlquery(f"select hashtag from all_posts where post_id={postid}")
    hlist=[]
    for i in range(len(op)-1):
        hlist.append(eval(op[i])[0])
    return hlist



def add_tags_to_user(username,tags):
    
    out = client.sqlquery(f"select hashtag from tagmanagement where username = '{username}'")
    b = ''
    print()
    for i in (eval(out[0])):
        b+=i
    b += tags
    b+= ','
    print(b)
    client.sqlquery(f"update tagmanagement set hashtag='{b}' where username = '{username}';")

#add_tags_to_user('admin','sql,test')
def top_topics(username):

    out = client.sqlquery(f"select hashtag from tagmanagement where username = '{username}'")
    l = (eval(out[0])[0].split(',')[:-1])
    set_of_list = set(l)
    list_of_set = list(set_of_list)

    list_with_freq = [(l.count(i),i) for i in list_of_set]
    print(list_with_freq)
    list_with_freq.sort(reverse = True)
    final_list = [i[1] for i in list_with_freq]
    print(final_list)
    s = ''
    print(len(final_list))
    for i in range(3):
        s+=final_list[i]+','
    client.sqlquery(f"update user_info set topics='{s}' where username='{username}';")
    return final_list
#print(top_topics('8'))

def dislikepost(tags,username):
    out = client.sqlquery(f"select disliked_hashtags from tagmanagement where username = '{username}'")
    b = ''
    print()
    for i in (eval(out[0])):
        b += i
    b += tags
    b += ','
    print(b)
    client.sqlquery(f"update tagmanagement set disliked_hashtags='{b}' where username = '{username}';")




'''
    out = client.sqlquery(f"select disliked_hashtags from tagmanagement where username = '{username}'")
    b = ''
    print()

    for i in (eval(out[0])):
        b += i

    for i in tags:
        b += i
        b += ','
    print(b)
    client.sqlquery(f"update tagmanagement set disliked_hashtags='{b}' where username = '{username}';")
'''

#dislikepost(['tag1','tag2'],'1')