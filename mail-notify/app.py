from base import app
from flask import make_response, redirect, render_template, request, url_for

from tasks.mail import send_mail


@app.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'GET':
        response = make_response(render_template('mail.html'))
    elif request.method == 'POST':
        recipient = request.values.get('recipient', '')
        title = request.values.get('title', '')
        content = request.values.get('content', '')

        # ''' 直接寄信 '''
		# msg = Message(title, recipients=[recipient])
        # msg.body = content
        # mail_app.send(msg)
		
		# ''' 使用任務寄信 '''
		# delay 意思是發送一個任務出去，然後就不管結果了。
		# send_mail.delay(recipients=recipient, title=title, content=content)
		
		# 如果想要等待結果可以使用 wait ，像這樣
        send = send_mail.delay(recipients=recipient, title=title, content=content)
        send.wait()
        response = make_response(render_template('mail.html', status='Send success'))
    else:
        response = make_response(redirect(url_for('index')))

    return response


if __name__ == '__main__':
    app.run()