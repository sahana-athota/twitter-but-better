import mysql.connector
import userdetails
import client


def new_user(username):
    client.sqlquery(f"insert into tagmanagement values({username},'education,')")
    
def gettags(postid):
    op=client.sqlquery(f"select hashtag from all_posts where post_id={post_id}")
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
    import client
    out = client.sqlquery(f"select hashtag from tagmanagement where username = '{username}'")
    b = ''
    print() #out- all tags
    l=out[0][2:-3]
    l=l.split(',')
    fre_list=[]
    top=[]
    maxx=('0',0)
    p=0
    for i in range(len(l)):
        if l[i] not in l[0:i]:
            count=l.count(l[i])
            fre_list.append((l[i],count))

    
    fre_list2=fre_list
    for i in range(len(fre_list2)):
        for j in range(len(fre_list2)):
            if maxx[1]<fre_list2[j][1]:
                maxx=fre_list2[j]
                
        if maxx[0] not in top:
            top.append(maxx[0])
        fre_list2.remove(maxx)
        maxx=('0',0)

    s=''
    j1=top
    top=top[0:3] #to get top 3 topics
    for i in top:
        s=s+i+','
    s2=s[:-1]
    client.sqlquery(f"update user_info set topics='{s2}' where username='{username}';")
    return j1
        
