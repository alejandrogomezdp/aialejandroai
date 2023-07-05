from flask import Flask, request, render_template, redirect, url_for
import openai

app = Flask(__name__)

openai.api_key = "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"

@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Usuario o contraseña inválidos')
    return render_template('login.html')

def valid_login(username, password):
    # Aquí puedes implementar tu lógica de autenticación
    return True

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response = None
    if request.method == 'POST':
        user_input = request.form['message']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en programación reconocido y tutor de codificación. Estás ayudando a un profesional con un problema de codificación."},
                {"role": "user", "content": user_input}
            ]
        )
        response = response.choices[0].message['content']
    return render_template('chat.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
