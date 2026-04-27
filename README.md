# sirtechify.com

Channel home base for the [SirTechify](https://www.youtube.com/@sirtechify) YouTube show — *Hardware where it doesn't belong.* New episodes every other Saturday.

Flask + HTML/CSS/JS, deployed on Vercel (Python 3.12 runtime).

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000. The contact-form and subscribe-list mail backends read `MAIL_USERNAME` and `MAIL_PASSWORD` from the environment (see `.env.example`); the site renders fine without them — mail-sending endpoints fail quietly.

## Endpoints

- `GET /` — landing page (hero, episodes, about, connect)
- `GET /api/health` — JSON liveness probe
- `POST /send_email` — contact-form backend (JSON `{name, email, message}`)
- `POST /api/subscribe` — mailing-list backend (JSON `{email}`); UI deferred until ~2 weeks before EP 1

## Episodes

`static/data/episodes.json` is the public episode index. Entries are appended one-by-one as each YouTube upload goes live — until EP 1 publishes, the site renders a "standing by" placeholder.

## Security posture

- Per-IP rate limits via Flask-Limiter: `/send_email` 5 per 15 min, `/api/subscribe` 3 per hour. Memory-backed, so it's a guardrail against bursty abuse rather than a strict distributed limit.
- Werkzeug `ProxyFix` wired so the limiter sees the real client IP from Vercel's `X-Forwarded-For` rather than the edge.
- Defense-in-depth headers via Flask `after_request`: strict CSP locked to `'self'` + `fonts.googleapis.com`, `fonts.gstatic.com`, `cdnjs.cloudflare.com`; plus `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and a `Permissions-Policy` denying geolocation/mic/camera/payment/usb.
- Newline/null-byte injection guards on submitted email fields before they're used as mail headers.

## Deploy

Auto-deploys to Vercel on push to `main`. Required env vars in the Vercel project: `MAIL_USERNAME`, `MAIL_PASSWORD`.
