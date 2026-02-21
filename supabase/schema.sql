-- Run this in Supabase SQL Editor to create tables and RLS for per-user config and applied jobs.
-- Requires Supabase Auth (e.g. Google) to be enabled in Authentication -> Providers.

-- User config: one row per user, full config JSON
create table if not exists public.user_config (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  config jsonb not null default '{}',
  updated_at timestamptz not null default now(),
  unique(user_id)
);

-- Applied jobs: one row per application per user
create table if not exists public.applied_jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  job_id text not null,
  title text,
  company text,
  hr_name text,
  hr_link text,
  job_link text,
  external_job_link text,
  date_applied text,
  created_at timestamptz not null default now(),
  unique(user_id, job_id)
);

-- RLS: users can only access their own rows
alter table public.user_config enable row level security;
alter table public.applied_jobs enable row level security;

create policy "user_config_select" on public.user_config for select using (auth.uid() = user_id);
create policy "user_config_insert" on public.user_config for insert with check (auth.uid() = user_id);
create policy "user_config_update" on public.user_config for update using (auth.uid() = user_id);

create policy "applied_jobs_select" on public.applied_jobs for select using (auth.uid() = user_id);
create policy "applied_jobs_insert" on public.applied_jobs for insert with check (auth.uid() = user_id);
create policy "applied_jobs_update" on public.applied_jobs for update using (auth.uid() = user_id);
create policy "applied_jobs_delete" on public.applied_jobs for delete using (auth.uid() = user_id);

-- Optional: allow service role to insert applied_jobs for a user (used by backend sync)
-- Service role bypasses RLS by default, so no extra policy needed for sync.
