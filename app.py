"""
sirtechify.com — Flask app
Channel home base for the SirTechify YouTube show.
Pass 1 rebrand 2026-04-25: subscribe UI deferred, contact form retained,
episode index served as static JSON.
"""
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv

# ─── App + static config ────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates',
)

# Vercel terminates TLS and proxies inbound requests; trust one X-Forwarded-*
# hop so request.remote_addr (used by the rate limiter) reflects the real
# client IP rather than Vercel's edge.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


@app.after_request
def add_security_headers(response):
    response.cache_control.max_age = 300
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
    )
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' fonts.googleapis.com cdnjs.cloudflare.com; "
        "font-src 'self' fonts.gstatic.com cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "script-src 'self' 'unsafe-inline' esm.sh cdn.vercel-insights.com; "
        "connect-src 'self' vitals.vercel-insights.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response


# ─── Mail config (used by contact form + future subscribe UI) ───────────────
load_dotenv()
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USERNAME']       = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD']       = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# ─── Rate limiting (per-IP, in-memory) ──────────────────────────────────────
# Memory storage resets on container cold-start in serverless, so this is a
# guardrail against bursty abuse, not a strict distributed limit.
limiter = Limiter(get_remote_address, app=app, storage_uri='memory://')


@app.errorhandler(429)
def ratelimit_handler(_e):
    return jsonify({'error': 'Too many requests, please try again later.'}), 429


# ─── Routes ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'fleet online'})


@app.route('/send_email', methods=['POST'])
@limiter.limit('5 per 15 minutes')
def send_email():
    """Contact form. Validates fields, sends a notification email if creds present."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        name    = data.get('name')
        email   = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            missing = [f for f in ['name', 'email', 'message'] if not data.get(f)]
            return jsonify({
                'success': False,
                'message': f"Missing required fields: {', '.join(missing)}",
            }), 400

        # Reject newlines/null bytes before using email as a Reply-To header
        if any(c in email for c in '\r\n\x00') or '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400

        msg = Message(
            'New contact-form submission — sirtechify.com',
            recipients=[os.getenv('MAIL_USERNAME') or 'test@example.com'],
            reply_to=email,
        )
        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

        if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
            mail.send(msg)

        return jsonify({'success': True, 'message': 'Sent.'})

    except Exception as e:
        app.logger.error(f'Error sending email: {e}')
        return jsonify({'success': False, 'message': 'Send failed.'}), 500


@app.route('/api/subscribe', methods=['POST'])
@limiter.limit('3 per hour')
def subscribe():
    """Mailing list signup. UI re-enables closer to EP 1 launch; backend stays warm."""
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400

        email = (data.get('email') or '').strip()
        if any(c in email for c in '\r\n\x00') or not email or '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({'error': 'Please provide a valid email address'}), 400

        msg = Message(
            'New mailing-list subscriber — sirtechify.com',
            recipients=[os.getenv('MAIL_USERNAME') or 'test@example.com'],
        )
        msg.body = f'New subscriber: {email}\n\nSource: sirtechify.com /api/subscribe'

        if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
            try:
                mail.send(msg)
                app.logger.info(f'Subscription email sent for {email}')
            except Exception as e:
                app.logger.error(f'Subscription email send failed: {e}')

        return jsonify({'message': 'Successfully subscribed.'}), 200

    except Exception as e:
        app.logger.error(f'Error in subscribe: {e}')
        return jsonify({'error': 'Subscription failed.'}), 500


# ─── Local dev ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
