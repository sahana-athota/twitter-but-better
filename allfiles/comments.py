import sql_actual
import client
import userdetails
#create table com_info(com_id int NOT NULL auto_increment,username varchar(50),post_id int, text varchar(80),primary key(com_id));

# to give all comments under a specific post
def allcomments(post_id):
    p=client.sqlquery(f"select username,text from com_info where post_id={post_id}")
    a=[]
    for i in p[:-1]:
        s=""
        if i!="('',)":
            s=eval(i)[0]+" : "+eval(i)[1]
        a.append(s)
    return a

def allcomments_postcontent(postcontent):
    post_id=userdetails.find_postid_with_postcontent(postcontent)
    allcomments(post_id)


#giving usernames/userid? of those who commented under a specific post
def users_commented(post_id):
    return ((eval(client.sqlquery(f"select user_id from com_info where post_id={post_id}")[0]))[0]).split(',')

#inserting new info into the comment table
def input_comment(post_id,username,text):
    print("here")
    client.sqlquery(f"insert into com_info values(NULL,'{username}','{post_id}','{text}');")
    print("works!")

