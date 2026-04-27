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
- Defense-in-depth headers via Flask `after_request`: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and a `Permissions-Policy` denying geolocation/mic/camera/payment/usb.
- Content-Security-Policy allows `'self'` plus the third-party origins this site actually loads from: `fonts.googleapis.com` + `fonts.gstatic.com` (Google Fonts), `cdnjs.cloudflare.com` (Font Awesome), and `esm.sh` + `cdn.vercel-insights.com` + `vitals.vercel-insights.com` (Vercel Speed Insights). Includes `'unsafe-inline'` in `script-src` to support Speed Insights' inline initializer — a known trade-off; tightening via per-request nonces is on the follow-up list.
- Newline/null-byte injection guards on submitted email fields before they're used as mail headers.

## Performance monitoring

Vercel Speed Insights is loaded inline in `templates/index.html` via the `esm.sh` CDN and reports Core Web Vitals to `vitals.vercel-insights.com`. Enable / view in the Vercel project dashboard.

## Deploy

Auto-deploys to Vercel on push to `main`. Required env vars in the Vercel project: `MAIL_USERNAME`, `MAIL_PASSWORD`.
