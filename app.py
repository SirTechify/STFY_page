from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Load environment variables
load_dotenv()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        msg = Message(
            'New Contact Form Submission',
            recipients=[os.getenv('MAIL_USERNAME')]
        )
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)

        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        print(f"\n=== New Subscription Request ===")
        print(f"Request data: {request.json}")
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            print("Error: No email provided")
            return jsonify({'error': 'Email is required'}), 400

        print(f"Processing subscription for email: {email}")
        print(f"Mail configuration: {app.config['MAIL_USERNAME']}")
        # Create message for new subscriber
        msg = Message(
            'New Mailing List Subscriber',
            recipients=[os.getenv('MAIL_USERNAME')]
        )
        print(f"Message created: {msg}")
        msg.body = f"New subscriber: {email}\n\nThey want to receive updates about new YouTube videos and Instagram posts."
        print(f"Message body set")
        
        try:
            mail.send(msg)
            print(f"Successfully sent email to {os.getenv('MAIL_USERNAME')}")
            return jsonify({'message': 'Successfully subscribed!'}), 200
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

    except Exception as e:
        import traceback
        print(f"\n=== Error processing subscription ===")
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
