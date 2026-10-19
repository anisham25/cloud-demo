# Where is this app running? — from localhost to Vercel

The demo for our tech talk, **How Cloud Computing Powers Modern Applications**.
A tiny Flask app whose page asks the server "where are you?". On a laptop it answers
**my laptop**; on Vercel it answers **Vercel**, with the region and machine it is running on.

| File | What it does |
|---|---|
| `app.py` | Flask app: serves the page locally and answers `GET /api/where` |
| `public/index.html` | The page. On Vercel, files in `public/` are served from the CDN |
| `requirements.txt` | Python packages to install (just Flask) |
| `tests/test_app.py` | Unit tests: `pip install pytest`, then `pytest -q` |

## Step 1 — Run it locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

Open http://127.0.0.1:5000. The page says **my laptop** and region **local**.
It works, but only here: `127.0.0.1` ("localhost") means *this computer*. A phone or a
classmate's laptop can't reach it, and it stops the moment you close the terminal.

## Step 2 — Why a cloud platform (Vercel)

Vercel is a platform-as-a-service. You connect a GitHub repo; Vercel builds it, serves
`public/` from its global CDN, runs `app.py` as a serverless function that scales with
traffic, gives you an HTTPS URL, and redeploys on every `git push`. It detects Flask
automatically, so there is no config file. The free **Hobby** plan is enough for this demo.

## Step 3 — Deploy

1. Push the project to a new GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Cloud demo"
   git branch -M main
   git remote add origin https://github.com/<you>/cloud-demo.git
   git push -u origin main
   ```
2. Sign up at vercel.com with your GitHub account, then go to **vercel.com/new**.
3. **Import** the `cloud-demo` repository and check the settings:

| Setting | Value | Why |
|---|---|---|
| Project Name | `cloud-demo` | Becomes part of the URL, e.g. `cloud-demo-<something>.vercel.app` |
| Framework Preset | detected automatically | Vercel sees `app.py` with a Flask `app` and knows how to run it |
| Root Directory | `./` | Where the app lives in the repo |
| Build and Output Settings | leave the defaults | Vercel installs `requirements.txt` for you; nothing else to build |
| Environment Variables | none | Our app needs no secrets |

4. Click **Deploy**. About a minute later you get a live URL.

## Step 4 — Test it

- Open the `.vercel.app` URL on your phone (or any other device). It says **Vercel**,
  with a region code (for example `iad1`) and a machine name.
- Stop the local server (Ctrl+C) and refresh `localhost:5000`: it's gone. The phone still works,
  because the app now runs on Vercel's computers, not yours.
- Tap **Ask again** a few times, and have others do the same: *copy alive for* and
  *requests this copy served* show copies being reused, and new ones starting.

## Step 5 — Behind the scenes

In the Vercel dashboard, open the project:

- **Deployments → the latest → Build Logs:** clone from GitHub, install dependencies, build, deploy.
- **Deployment summary:** the page is a **static asset** (CDN); `app.py` became one **function**.
- **Logs:** one line per request to `/api/where`, with status code and duration.
- **Settings → Functions:** the region your function runs in.

What happened: Vercel cloned the repo, installed Flask, uploaded `public/` to its CDN and
packaged `app.py` as a function. A request for `/` is answered by the nearest CDN location;
a request for `/api/where` starts (or reuses) a copy of the function in its region.

Push a change to `main` and a new deployment starts by itself. Each deployment keeps its own
URL, and you can roll back to an older one from the dashboard.

**Why the hit counter varies:** each copy has its own memory, and copies are created and removed
as traffic changes. Anything that must be shared or kept — users, posts, votes — belongs in a
database, not in a Python variable.

## Clean up

Project → **Settings** → scroll down → **Delete Project**.
