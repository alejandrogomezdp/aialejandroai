from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////conversations.db'  # replace with your own database URI
db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True), default=func.now())

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'role': self.role,
            'conversation_id': self.conversation_id,
        }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/iniciar-sesion")
def iniciar_sesion():
    return render_template("iniciar_sesion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    messages = []  # Initialize messages here to ensure it's always defined
    if request.method == "POST":
        user_input = request.form.get("user_input")
        conv = Conversation()
        db.session.add(conv)
        db.session.commit()
        user_message = Message(content=user_input, role='user', conversation_id=conv.id)
        db.session.add(user_message)
        db.session.commit()

        messages = [msg.to_dict() for msg in Message.query.filter_by(conversation_id=conv.id).all()]

    convs = Conversation.query.all()
    return render_template("chat.html", conversations=convs, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
