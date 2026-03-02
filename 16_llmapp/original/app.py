import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for, make_response
from graph import app_graph
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)
app.secret_key = "dog_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())
    
    config = {"configurable": {"thread_id": session["thread_id"]}}

    if request.method == "POST":
        user_msg = request.form.get("user_message")
        if user_msg:
            app_graph.invoke({"messages": [("user", user_msg)]}, config)

    messages = []
    state = app_graph.get_state(config)
    if state.values:
        for m in state.values["messages"]:
            if isinstance(m, HumanMessage):
                messages.append({"class": "user-message", "text": m.content.replace("\n", "<br>")})
            elif isinstance(m, AIMessage) and m.content:
                messages.append({"class": "bot-message", "text": m.content.replace("\n", "<br>")})
                
    return render_template("index.html", messages=messages)

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("thread_id", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)