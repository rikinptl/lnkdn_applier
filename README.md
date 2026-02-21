# LinkedIn Auto Job Applier — Config & Pipeline Website

This project wraps the [Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn) reference repo in a **form-based website** so you can:

- **Sign in with Google** and keep your config and applied jobs under your account (stored in Supabase).
- **Fill in all bot configuration** (personals, application answers, search preferences, secrets, settings) in one place.
- **Start** the job-application pipeline (writes your config to the reference repo and runs the bot).
- **Stop** the pipeline at any time.
- **View and sync applied jobs** per user (from the bot’s CSV into your account).

## Setup

1. **Reference repo**  
   The reference is already cloned in `reference/`. If you need to re-clone:
   ```bash
   git clone https://github.com/GodsScion/Auto_job_applier_linkedIn.git reference
   ```

2. **Python**  
   Use Python 3.10+.

3. **Dependencies for this site**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Dependencies for the bot** (in `reference/`):
   ```bash
   cd reference
   pip install undetected-chromedriver pyautogui setuptools openai flask-cors flask
   ```
   Also install [Chrome](https://www.google.com/chrome) and, if not using `stealth_mode`, the matching [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/).

5. **Supabase and Google sign-in (optional)**  
   - Use your Supabase project. In **SQL Editor**, run `supabase/schema.sql` to create tables and RLS.  
   - For **Sign in with Google**: see **[docs/GOOGLE_SIGNIN_SETUP.md](docs/GOOGLE_SIGNIN_SETUP.md)** (Google Cloud OAuth + Supabase + Vercel).  
   - Copy `.env.example` to `.env` and set `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` from Project Settings → API. **Do not commit `.env`.**

## Run the website

From the project root:

```bash
python app.py
```

Then open **http://localhost:5001**.

- **Sign in with Google** to store config and applied jobs under your account. Without sign-in, config uses `config.json` and jobs from the bot’s CSV.
- Use the **Personals**, **Questions & Resume**, **Search**, **Secrets & AI**, and **Settings** tabs to fill in details.
- Click **Save config** to persist (to your account if signed in, else to `config.json`).
- **Load from reference** reloads from `reference/config/*.py`.
- **Start pipeline** saves the form, writes config to the reference repo and runs the bot. Chrome will open.
- **Stop pipeline** terminates the bot.
- **Applied jobs** tab: view jobs; when signed in, **Sync from bot CSV** imports from the bot’s CSV into your account.

## Deploy to Vercel

- Connect the repo to [Vercel](https://vercel.com); the project is configured via `vercel.json`.
- Set environment variables in Vercel: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`.
- **Pipeline (Start/Stop bot)** does not run on Vercel; use the app locally to run the LinkedIn bot. On Vercel you can still sign in, edit config, view/sync applied jobs, and save to Supabase.

## Disclaimer

This tool is for educational use. Comply with LinkedIn’s terms of service and use at your own risk. See the [reference repo](https://github.com/GodsScion/Auto_job_applier_linkedIn) for full disclaimer and license (AGPL-3.0).
