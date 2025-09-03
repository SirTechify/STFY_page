from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from flask_mail import Mail, Message
import os
import sys
from dotenv import load_dotenv

# Initialize Flask app with static file configuration
app = Flask(__name__, 
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')

# Ensure static files are served with the correct MIME type
@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

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

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'python_version': sys.version
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-image')
def test_image():
    # Test if we can access static files
    try:
        return send_file('static/images/profile/profile.jpg', mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

@app.route('/<path:path>')
def static_proxy(path):
    # First try to serve static files
    static_file = os.path.join(app.static_folder, path)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return send_from_directory(app.static_folder, path)
    
    # Then try to serve template files
    template_file = os.path.join(app.template_folder, path)
    if os.path.exists(template_file) and os.path.isfile(template_file):
        return send_from_directory(app.template_folder, path)
    
    # If file not found, serve index.html for SPA routing
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Check for missing required fields
        if not all([name, email, message]):
            missing = [field for field in ['name', 'email', 'message'] if not data.get(field)]
            return jsonify({
                "success": False, 
                "message": f"Missing required fields: {', '.join(missing)}"
            }), 400
            
        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({
                "success": False,
                "message": "Invalid email format"
            }), 400

        msg = Message(
            'New Contact Form Submission',
            recipients=[os.getenv('MAIL_USERNAME') or 'test@example.com']
        )
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        # Only try to send email if we have valid credentials
        if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
            mail.send(msg)
        
        return jsonify({
            "success": True, 
            "message": "Email sent successfully!"
        })
        
    except Exception as e:
        app.logger.error(f"Error sending email: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "An error occurred while sending the email"
        }), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
            
        email = data.get('email').strip()
        
        # Basic email validation
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({'error': 'Please provide a valid email address'}), 400

        # Prepare the notification email
        msg = Message(
            'New Mailing List Subscriber',
            recipients=[os.getenv('MAIL_USERNAME') or 'test@example.com']
        )
        msg.body = f"New subscriber: {email}\n\nThey want to receive updates about new YouTube videos and Instagram posts."
        
        # Only try to send email if we have valid credentials
        if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
            try:
                mail.send(msg)
                app.logger.info(f"Subscription email sent for {email}")
            except Exception as e:
                app.logger.error(f"Error sending subscription email: {str(e)}")
                # Continue execution even if email fails
        
        return jsonify({'message': 'Successfully subscribed!'}), 200

    except Exception as e:
        app.logger.error(f"Error in subscribe endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your subscription'}), 500


# Vercel requires an app variable for serverless functions
app = app if 'app' in locals() else app

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
