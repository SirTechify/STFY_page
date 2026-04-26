# sirtechify.com

Channel home base for the [SirTechify](https://www.youtube.com/@sirtechify) YouTube show — *Hardware where it doesn't belong.* New episodes every other Saturday.

Flask + HTML/CSS/JS, deployed on Vercel.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000. The contact-form and subscribe-list backends need `MAIL_USERNAME` and `MAIL_PASSWORD` env vars (Gmail app password); the site renders fine without them.

## Episodes

`static/data/episodes.json` is the public episode index. Entries are appended one-by-one as each YouTube upload goes live — until EP 1 publishes, the site renders a "standing by" placeholder.

## Deploy

Auto-deploys to Vercel on push to `main`. Required env vars in the Vercel project: `MAIL_USERNAME`, `MAIL_PASSWORD`.
