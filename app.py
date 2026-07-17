from werkzeug.exceptions import NotFound
from uuid import uuid4

from flask import (
    flash,
    Flask, 
    redirect, 
    render_template,
    request, 
    session,
    url_for,
) 

from todos.utils import error_for_list_title, find_list_by_id, error_for_todo_title

app = Flask(__name__)
app.secret_key='secret1' #Set up a secret key

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

# redirect start page
@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

@app.route("/lists")
def get_lists():
    return render_template('lists.html', lists=session['lists'])

# create a new todo list
@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip() 
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template("new_list.html", title=title)
    
    session['lists'].append({ #saves lists in session
        'id': str(uuid4()),
        'title': title, 
        'todos': [],
    })

    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>")
def show_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    return render_template('list.html', lst=lst)

# create a new todo object
@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form["todo"].strip() ### this line gets the value of todo, "todo": "Buy milk", <input name="todo">, line 47 list.html

    lst = find_list_by_id(list_id, session["lists"]) ## access all list dictionary saved in session
    if not lst:
        raise NotFound(description="List not found") #from module werkzeug.exceptions raises a 404 response when the list_id does not exist

    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template("list.html", lst=lst)

    lst["todos"].append({ ## session["lists"] = [
                          #     {
                          #         "id": "...",
                          #         "title": "...",
                          #         "todos": []
                          #     }
                          # ]. what is session? a dictionary where we store different objects?
        'id': str(uuid4()),
        'title': todo_title,
        'completed': False, 
    })

    flash("The todo object was added.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id)) #from. show_list(list_id)

if __name__ == "__main__":
    app.run(debug=True, port=5003)