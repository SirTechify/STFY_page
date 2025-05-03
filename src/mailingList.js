import React, { useState } from 'react';

const MailingList = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      if (response.ok) {
        setShowSuccess(true);
        setEmail('');
        setMessage('Thank you for subscribing!');
      } else {
        setMessage('Sorry, something went wrong. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Sorry, something went wrong. Please try again.');
    }
  };

  return (
    <section id="mailing-list" className="mailing-list">
      <h2>Stay Updated</h2>
      <div className="mailing-list-content">
        <p>Subscribe to our mailing list to get notified about new YouTube videos and Instagram posts.</p>
        <form onSubmit={handleSubmit} className="mailing-list-form">
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Your Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn primary">
            Subscribe
          </button>
        </form>
        {message && <p className="message">{message}</p>}
      </div>
    </section>
  );
};

export default MailingList;
