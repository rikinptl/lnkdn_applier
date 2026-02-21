# Sign in with Google – Setup Guide

Your app already has the **"Sign in with Google"** button and code. To make it work, complete these three steps: **Google Cloud**, **Supabase**, and **Vercel**.

---

## Step 1: Google Cloud Console (OAuth credentials)

1. Go to **[Google Cloud Console](https://console.cloud.google.com/)** and sign in.
2. Create or select a **project** (top bar → project dropdown → **New Project** if needed).
3. Open **APIs & Services** → **Credentials** (left sidebar).
4. Click **+ Create Credentials** → **OAuth client ID**.
5. If asked to configure the **OAuth consent screen**:
   - Choose **External** (or Internal for workspace-only) → **Create**.
   - Fill **App name** (e.g. "LinkedIn Job Applier") and **User support email**.
   - Add your email under **Developer contact**. Save.
6. Back to **Create OAuth client ID**:
   - **Application type:** **Web application**.
   - **Name:** e.g. "LinkedIn Job Applier Web".
   - Under **Authorized redirect URIs** click **Add URI** and add:
     ```text
     https://YOUR_SUPABASE_PROJECT_REF.supabase.co/auth/v1/callback
     ```
     Replace `YOUR_SUPABASE_PROJECT_REF` with your Supabase project reference (from Supabase Dashboard → Project Settings → General → Reference ID, or the subdomain in your project URL: `https://xxxxx.supabase.co` → `xxxxx`).
   - Save.
7. Copy the **Client ID** and **Client secret**; you’ll paste them into Supabase next.

---

## Step 2: Supabase (enable Google and URLs)

1. Go to **[Supabase Dashboard](https://supabase.com/dashboard)** → your project.
2. **Authentication** (left sidebar) → **Providers**.
3. Find **Google** and turn it **On**.
4. Paste the **Client ID** and **Client secret** from Google. Save.
5. **Authentication** → **URL Configuration**:
   - **Site URL:** your app’s public URL, e.g.  
     `https://lnkdn-applier-nvr5.vercel.app`  
     (no trailing slash)
   - **Redirect URLs:** add your live app URL and (for local testing) localhost, e.g.  
     `https://lnkdn-applier-nvr5.vercel.app`  
     `http://localhost:5001`  
     The app sends users back to the current page after sign-in, so these must match where your app is served.
   - Save.

After this, "Sign in with Google" will redirect to Google and then back to your app; Supabase will restore the session automatically.

---

## Step 3: Vercel (env vars)

1. **[Vercel](https://vercel.com/dashboard)** → your project → **Settings** → **Environment Variables**.
2. Add:
   - **SUPABASE_URL** = Supabase **Project URL** (Project Settings → API).
   - **SUPABASE_ANON_KEY** = Supabase **anon public** key (Project Settings → API).
3. **Redeploy** the project (Deployments → ⋯ → Redeploy, or push a commit).

---

## Flow summary

1. User clicks **Sign in with Google** on your site.
2. They are sent to Google to sign in (or choose an account).
3. Google redirects back to Supabase; Supabase then redirects to your **Site URL** with tokens in the URL.
4. Your app’s Supabase client reads the session and updates the UI (signed-in state, config, etc.).

No extra code is required in your repo for this flow; the existing button and Supabase auth code already implement it once the three steps above are done.
