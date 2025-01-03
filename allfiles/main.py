import requests

from flask import *
import userdetails
import scrapping
import sql_actual
import tagmanagement
import json
import time
import comments
start = time.time()
end = time.time()
tm = end - start
x = open('time.txt', 'w')
x.write(str(end - start))
x.close()

app = Flask(__name__)
app.secret_key = 'hi'


# app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

@app.route('/')
def redirtemp():
    return render_template('home.html')


@app.route('/login', methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        session['password'] = password

        return redirect(url_for("print"))
    else:
        return render_template('index_#.html')

@app.route('/about')
def about():
    return render_template('aboutpage.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        usernamenew = request.form['usernamenew']
        passwordnew = request.form['passwordnew']
        passwordnew2 = request.form['passwordnew2']
        if passwordnew2 != passwordnew:
            return '<p>Looks like the 2 passwords written are different. </p>'
        if userdetails.finduser(usernamenew) == True:
            return '<p>This username has already been taken. </p>'
        topics = request.form['topic']
        session['usernamenew'] = usernamenew
        session['passwordnew'] = passwordnew
        session['topics'] = topics
        return redirect(url_for("onboarding"))
    else:
        return render_template('register_#.html')


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output)  # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output)  # this converts the json output to a python dictionary
    print(result)  # Printing the new dictionary
    print(type(result))  # this shows the json converted as a python dictionary
    return result


@app.route('/onboarding')
def onboarding():
    sql_actual.user_insertion(session['usernamenew'], session['passwordnew'],session['topics'])
    session['username'] = session['usernamenew']
    session['password'] = session['passwordnew']
    username = session['username']

    try:
        a = userdetails.auth(session['usernamenew'], session['passwordnew'])
    except :
        return '<p>Looks like this user is not registered! </p>'
    if a == True:
        import tagmanagement as tg
        tg.top_topics(username)
        return redirect(url_for("confirm_onboard"))
    else:
        return '<p>Looks like password is wrong!</p>'


@app.route('/user')
def print():
    try:
        if sql_actual.check_if_user_already_exists(session['username']): #if username exist
            if userdetails.auth(session['username'], session['password']): #if username,pwd pair is correct
                return redirect(url_for("confirm_onboard"))
            else:
                return  '<p>Looks like password is wrong!</p>'
        else:
            return '<p>Looks like this user does not exist!</p>'


    except:
        return '<p>There has been some error trying to log you in</p>'

@app.route('/confirm_onboard')
def confirm_onboard():
    return render_template('onboarding.html')


@app.route('/mainpage', methods=["POST", "GET"])
def mainpage():
    if request.method == "POST":
        try:
            postcontents = request.form["likedpost"]
            username = session["username"]
            tags = userdetails.find_posttags_with_postcontent(postcontents)
            tagmanagement.add_tags_to_user(username, tags)
            return redirect(url_for("mainpage"))
        except:
            try:
                postcontents = request.form["dislikedpost"]
                username = session["username"]
                tags = userdetails.find_posttags_with_postcontent(postcontents)
                tagmanagement.dislikepost(tags, username)
                return redirect(url_for("mainpage"))
            except:
                postcontents = request.form["commentpost"]
                comment = request.form["comment"]
                username = session["username"]
                post_id = userdetails.find_postid_with_postcontent(eval(postcontents)[0])
                comments.input_comment(post_id, username, comment)
                return redirect(url_for("mainpage"))


    else:
        sql_actual.checkinitialization()
        topic = userdetails.gettopics(session["username"])
        text = scrapping.scrape(topic)
        usrnm = session["username"]

        list_of_hashtags = sql_actual.return_hashtags_with_username(usrnm)[0][:-1].split(',')
        set_of_hashtags = set(list_of_hashtags)
        lhashtags = [(list_of_hashtags.count(i), i) for i in set_of_hashtags]

        list_of_dislikedhashtags = sql_actual.return_dislikedhashtags_with_username(usrnm)[0][:-1].split(',')
        set_of_dislikedhashtags = set(list_of_dislikedhashtags)
        ldisliked = [(list_of_dislikedhashtags.count(i), i) for i in set_of_dislikedhashtags]

        lhashtags.sort(reverse=True)
        ldisliked.sort(reverse=True)

        #getweights returns weights taking into account liked and disliked hashtags
        def getweights(topics):
            weight = 0
            # adding from liked
            for i in lhashtags:
                if i[1] == topics:
                    weight += i[0]

            # reducing weight if disliked
            for i in ldisliked:
                if i[1] == topics:
                    weight -= i[0]

            return weight

        postidandhash = sql_actual.getallposthashtagandpostid()
        list1 = []
        for i in postidandhash:
            listofhashtaglocal = i[1].split(',')
            weight = 0
            for j in listofhashtaglocal:
                weight += getweights(j)
            list1.append((weight, i[0]))

        list1.sort(reverse=True)
        postidlist = [i[1] for i in list1]
        posts = [sql_actual.getpostwithid(i)[0] for i in postidlist]
        global post_with_hashtags_comments
        post_with_hashtags_comments = []

        for i in range(len(posts)):
            a=posts[i]
            post_with_hashtags_comments.append([a, sql_actual.gethashtagswithpost(a),comments.allcomments(postidlist[i]),sql_actual.return_username_postcontents(a)])

        for i in post_with_hashtags_comments:
            c=i[2]
            if c[0]=="":
                i[2]=["No comments yet"]
            
        

        return render_template('mainpage.html', text=(text), sessionusername=session["username"], topic=topic,
                               posts=post_with_hashtags_comments)


@app.route('/postcreationpage', methods=["POST", "GET"])
def postcreation():
    if request.method == "POST":
        username = session['username']
        postcontents = request.form['postcontent']
        if postcontents=='':
            return '<p>User post cannot be empty.</p>'
        posttags = request.form['posttags']
        session['postcontents'] = postcontents
        session['posttags'] = posttags
        userdetails.insertpost(username, postcontents, posttags)
        return redirect(url_for("mainpage"))
    else:
        return render_template('postcreationpage.html')
@app.route('/confirm_passwordreset')
def confirm_passwordreset():
    return render_template('confirm_passwordreset.html')

@app.route('/passwordreset', methods=["POST", "GET"])
def pwdreset():
    if request.method == "POST":
        username = session['username']
        passwordold = request.form['passwordold']
        passwordnew = request.form['passwordnew']
        a = sql_actual.reset_password(username,passwordold,passwordnew)
        if  a == False:
            return '<p>Looks like password is wrong!</p>'
        else:
            return redirect(url_for("confirm_passwordreset"))
    else:
        return render_template('resetpassword.html')


@app.route('/about/<user>', methods=["POST", "GET"])
def about_user(user):
    sql_actual.checkinitialization()
    return render_template('aboutuser.html', posts=sql_actual.all_posts_by_a_user(user),username = user)

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)

'''
1. get topics while user registration
2. add post via website --> done
3. auto refresh of code while updation to database --> pending for new user creation
4. hashtag system --> done


5.Like post
'''
