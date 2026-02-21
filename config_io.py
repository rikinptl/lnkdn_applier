"""
Read config from reference Auto_job_applier_linkedIn and write it back to .py files.
Used by the web app to load defaults and persist form data before starting the bot.
"""
import os
import json
import subprocess
import sys

REFERENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference")
CONFIG_DIR = os.path.join(REFERENCE_DIR, "config")


def _py_value_repr(v):
    """Format a Python value for assignment in .py file."""
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(repr(x) for x in v) + "]"
    return repr(v)


def _write_personals(data: dict) -> None:
    path = os.path.join(CONFIG_DIR, "personals.py")
    header = """'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/
Copyright (C) 2024 Sai Vignesh Golla
License:    GNU Affero General Public License
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn
'''

# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

"""
    lines = [
        f"first_name = {_py_value_repr(data.get('first_name', ''))}",
        f"middle_name = {_py_value_repr(data.get('middle_name', ''))}",
        f"last_name = {_py_value_repr(data.get('last_name', ''))}",
        f"phone_number = {_py_value_repr(data.get('phone_number', ''))}",
        f"current_city = {_py_value_repr(data.get('current_city', ''))}",
        f"street = {_py_value_repr(data.get('street', ''))}",
        f"state = {_py_value_repr(data.get('state', ''))}",
        f"zipcode = {_py_value_repr(data.get('zipcode', ''))}",
        f"country = {_py_value_repr(data.get('country', ''))}",
        f"ethnicity = {_py_value_repr(data.get('ethnicity', 'Decline'))}",
        f"gender = {_py_value_repr(data.get('gender', 'Decline'))}",
        f"disability_status = {_py_value_repr(data.get('disability_status', 'Decline'))}",
        f"veteran_status = {_py_value_repr(data.get('veteran_status', 'Decline'))}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


def _write_questions(data: dict) -> None:
    path = os.path.join(CONFIG_DIR, "questions.py")
    header = """'''
Author:     Sai Vignesh Golla
Copyright (C) 2024 Sai Vignesh Golla
License:    GNU Affero General Public License
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn
'''

# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

"""
    lines = [
        f"default_resume_path = {_py_value_repr(data.get('default_resume_path', 'all resumes/default/resume.pdf'))}",
        f"years_of_experience = {_py_value_repr(data.get('years_of_experience', '5'))}",
        f"require_visa = {_py_value_repr(data.get('require_visa', 'No'))}",
        f"website = {_py_value_repr(data.get('website', ''))}",
        f"linkedIn = {_py_value_repr(data.get('linkedIn', ''))}",
        f"us_citizenship = {_py_value_repr(data.get('us_citizenship', 'U.S. Citizen/Permanent Resident'))}",
        f"desired_salary = {data.get('desired_salary', 120000)}",
        f"current_ctc = {data.get('current_ctc', 800000)}",
        f"notice_period = {data.get('notice_period', 30)}",
        f"linkedin_headline = {_py_value_repr(data.get('linkedin_headline', ''))}",
        f"linkedin_summary = {_py_value_repr(data.get('linkedin_summary', ''))}",
        f"cover_letter = {_py_value_repr(data.get('cover_letter', ''))}",
        f"user_information_all = {_py_value_repr(data.get('user_information_all', ''))}",
        f"recent_employer = {_py_value_repr(data.get('recent_employer', 'Not Applicable'))}",
        f"confidence_level = {_py_value_repr(data.get('confidence_level', '8'))}",
        f"pause_before_submit = {_py_value_repr(data.get('pause_before_submit', True))}",
        f"pause_at_failed_question = {_py_value_repr(data.get('pause_at_failed_question', True))}",
        f"overwrite_previous_answers = {_py_value_repr(data.get('overwrite_previous_answers', False))}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


def _write_search(data: dict) -> None:
    path = os.path.join(CONFIG_DIR, "search.py")
    header = """'''
Author:     Sai Vignesh Golla
Copyright (C) 2024 Sai Vignesh Golla
License:    GNU Affero General Public License
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn
'''

# LINKEDIN SEARCH PREFERENCES

"""
    lines = [
        f"search_terms = {_py_value_repr(data.get('search_terms', ['Software Engineer']))}",
        f"search_location = {_py_value_repr(data.get('search_location', ''))}",
        f"switch_number = {data.get('switch_number', 30)}",
        f"randomize_search_order = {_py_value_repr(data.get('randomize_search_order', False))}",
        f"sort_by = {_py_value_repr(data.get('sort_by', ''))}",
        f"date_posted = {_py_value_repr(data.get('date_posted', 'Past week'))}",
        f"salary = {_py_value_repr(data.get('salary', ''))}",
        f"easy_apply_only = {_py_value_repr(data.get('easy_apply_only', True))}",
        f"experience_level = {_py_value_repr(data.get('experience_level', []))}",
        f"job_type = {_py_value_repr(data.get('job_type', []))}",
        f"on_site = {_py_value_repr(data.get('on_site', []))}",
        f"companies = {_py_value_repr(data.get('companies', []))}",
        f"location = {_py_value_repr(data.get('location', []))}",
        f"industry = {_py_value_repr(data.get('industry', []))}",
        f"job_function = {_py_value_repr(data.get('job_function', []))}",
        f"job_titles = {_py_value_repr(data.get('job_titles', []))}",
        f"benefits = {_py_value_repr(data.get('benefits', []))}",
        f"commitments = {_py_value_repr(data.get('commitments', []))}",
        f"under_10_applicants = {_py_value_repr(data.get('under_10_applicants', False))}",
        f"in_your_network = {_py_value_repr(data.get('in_your_network', False))}",
        f"fair_chance_employer = {_py_value_repr(data.get('fair_chance_employer', False))}",
        f"pause_after_filters = {_py_value_repr(data.get('pause_after_filters', True))}",
        f"about_company_bad_words = {_py_value_repr(data.get('about_company_bad_words', []))}",
        f"about_company_good_words = {_py_value_repr(data.get('about_company_good_words', []))}",
        f"bad_words = {_py_value_repr(data.get('bad_words', []))}",
        f"security_clearance = {_py_value_repr(data.get('security_clearance', False))}",
        f"did_masters = {_py_value_repr(data.get('did_masters', True))}",
        f"current_experience = {data.get('current_experience', 5)}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


def _write_secrets(data: dict) -> None:
    path = os.path.join(CONFIG_DIR, "secrets.py")
    header = """'''
Author:     Sai Vignesh Golla
Copyright (C) 2024 Sai Vignesh Golla
License:    GNU Affero General Public License
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn
'''

"""
    lines = [
        f"username = {_py_value_repr(data.get('username', 'username@example.com'))}",
        f"password = {_py_value_repr(data.get('password', 'example_password'))}",
        f"use_AI = {_py_value_repr(data.get('use_AI', False))}",
        f"ai_provider = {_py_value_repr(data.get('ai_provider', 'openai'))}",
        f"llm_api_url = {_py_value_repr(data.get('llm_api_url', 'https://api.openai.com/v1/'))}",
        f"llm_api_key = {_py_value_repr(data.get('llm_api_key', 'not-needed'))}",
        f"llm_model = {_py_value_repr(data.get('llm_model', 'gpt-5-mini'))}",
        f"llm_spec = {_py_value_repr(data.get('llm_spec', 'openai'))}",
        f"stream_output = {_py_value_repr(data.get('stream_output', False))}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


def _write_settings(data: dict) -> None:
    path = os.path.join(CONFIG_DIR, "settings.py")
    header = """'''
Author:     Sai Vignesh Golla
Copyright (C) 2024 Sai Vignesh Golla
License:    GNU Affero General Public License
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn
'''

"""
    lines = [
        f"close_tabs = {_py_value_repr(data.get('close_tabs', False))}",
        f"follow_companies = {_py_value_repr(data.get('follow_companies', False))}",
        f"run_non_stop = {_py_value_repr(data.get('run_non_stop', False))}",
        f"alternate_sortby = {_py_value_repr(data.get('alternate_sortby', True))}",
        f"cycle_date_posted = {_py_value_repr(data.get('cycle_date_posted', True))}",
        f"stop_date_cycle_at_24hr = {_py_value_repr(data.get('stop_date_cycle_at_24hr', True))}",
        f"generated_resume_path = {_py_value_repr(data.get('generated_resume_path', 'all resumes/'))}",
        f"file_name = {_py_value_repr(data.get('file_name', 'all excels/all_applied_applications_history.csv'))}",
        f"failed_file_name = {_py_value_repr(data.get('failed_file_name', 'all excels/all_failed_applications_history.csv'))}",
        f"logs_folder_path = {_py_value_repr(data.get('logs_folder_path', 'logs/'))}",
        f"click_gap = {data.get('click_gap', 1)}",
        f"run_in_background = {_py_value_repr(data.get('run_in_background', False))}",
        f"disable_extensions = {_py_value_repr(data.get('disable_extensions', False))}",
        f"safe_mode = {_py_value_repr(data.get('safe_mode', True))}",
        f"smooth_scroll = {_py_value_repr(data.get('smooth_scroll', False))}",
        f"keep_screen_awake = {_py_value_repr(data.get('keep_screen_awake', True))}",
        f"stealth_mode = {_py_value_repr(data.get('stealth_mode', True))}",
        f"showAiErrorAlerts = {_py_value_repr(data.get('showAiErrorAlerts', False))}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")


def write_all_config(full_config: dict) -> None:
    """Write full config dict to reference config/*.py files."""
    _write_personals(full_config.get("personals", {}))
    _write_questions(full_config.get("questions", {}))
    _write_search(full_config.get("search", {}))
    _write_secrets(full_config.get("secrets", {}))
    _write_settings(full_config.get("settings", {}))


def read_config_from_reference() -> dict:
    """Run a script in reference dir that exports config as JSON."""
    script = """
import sys
import json
sys.path.insert(0, %r)
from config import personals, questions, search, secrets, settings

out = {
    "personals": {
        "first_name": personals.first_name,
        "middle_name": personals.middle_name,
        "last_name": personals.last_name,
        "phone_number": personals.phone_number,
        "current_city": personals.current_city,
        "street": personals.street,
        "state": personals.state,
        "zipcode": personals.zipcode,
        "country": personals.country,
        "ethnicity": personals.ethnicity,
        "gender": personals.gender,
        "disability_status": personals.disability_status,
        "veteran_status": personals.veteran_status,
    },
    "questions": {
        "default_resume_path": questions.default_resume_path,
        "years_of_experience": questions.years_of_experience,
        "require_visa": questions.require_visa,
        "website": questions.website,
        "linkedIn": questions.linkedIn,
        "us_citizenship": questions.us_citizenship,
        "desired_salary": questions.desired_salary,
        "current_ctc": questions.current_ctc,
        "notice_period": questions.notice_period,
        "linkedin_headline": questions.linkedin_headline,
        "linkedin_summary": questions.linkedin_summary,
        "cover_letter": questions.cover_letter,
        "user_information_all": getattr(questions, "user_information_all", ""),
        "recent_employer": questions.recent_employer,
        "confidence_level": questions.confidence_level,
        "pause_before_submit": questions.pause_before_submit,
        "pause_at_failed_question": questions.pause_at_failed_question,
        "overwrite_previous_answers": questions.overwrite_previous_answers,
    },
    "search": {
        "search_terms": search.search_terms,
        "search_location": search.search_location,
        "switch_number": search.switch_number,
        "randomize_search_order": search.randomize_search_order,
        "sort_by": search.sort_by,
        "date_posted": search.date_posted,
        "salary": search.salary,
        "easy_apply_only": search.easy_apply_only,
        "experience_level": search.experience_level,
        "job_type": search.job_type,
        "on_site": search.on_site,
        "companies": search.companies,
        "location": search.location,
        "industry": search.industry,
        "job_function": search.job_function,
        "job_titles": search.job_titles,
        "benefits": search.benefits,
        "commitments": search.commitments,
        "under_10_applicants": search.under_10_applicants,
        "in_your_network": search.in_your_network,
        "fair_chance_employer": search.fair_chance_employer,
        "pause_after_filters": search.pause_after_filters,
        "about_company_bad_words": search.about_company_bad_words,
        "about_company_good_words": search.about_company_good_words,
        "bad_words": search.bad_words,
        "security_clearance": search.security_clearance,
        "did_masters": search.did_masters,
        "current_experience": search.current_experience,
    },
    "secrets": {
        "username": secrets.username,
        "password": secrets.password,
        "use_AI": secrets.use_AI,
        "ai_provider": secrets.ai_provider,
        "llm_api_url": secrets.llm_api_url,
        "llm_api_key": secrets.llm_api_key,
        "llm_model": secrets.llm_model,
        "llm_spec": secrets.llm_spec,
        "stream_output": secrets.stream_output,
    },
    "settings": {
        "close_tabs": settings.close_tabs,
        "follow_companies": settings.follow_companies,
        "run_non_stop": settings.run_non_stop,
        "alternate_sortby": settings.alternate_sortby,
        "cycle_date_posted": settings.cycle_date_posted,
        "stop_date_cycle_at_24hr": settings.stop_date_cycle_at_24hr,
        "generated_resume_path": settings.generated_resume_path,
        "file_name": settings.file_name,
        "failed_file_name": settings.failed_file_name,
        "logs_folder_path": settings.logs_folder_path,
        "click_gap": settings.click_gap,
        "run_in_background": settings.run_in_background,
        "disable_extensions": settings.disable_extensions,
        "safe_mode": settings.safe_mode,
        "smooth_scroll": settings.smooth_scroll,
        "keep_screen_awake": settings.keep_screen_awake,
        "stealth_mode": settings.stealth_mode,
        "showAiErrorAlerts": settings.showAiErrorAlerts,
    },
}
# Convert non-JSON-serializable
def sanitize(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, list):
        return [sanitize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    return str(obj)
print(json.dumps(sanitize(out)))
""" % REFERENCE_DIR
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=REFERENCE_DIR,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return get_default_config()
        return json.loads(result.stdout.strip())
    except Exception:
        return get_default_config()


def get_default_config() -> dict:
    """Return default config structure when reference is not runnable."""
    return {
        "personals": {
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "phone_number": "",
            "current_city": "",
            "street": "",
            "state": "",
            "zipcode": "",
            "country": "",
            "ethnicity": "Decline",
            "gender": "Decline",
            "disability_status": "Decline",
            "veteran_status": "Decline",
        },
        "questions": {
            "default_resume_path": "all resumes/default/resume.pdf",
            "years_of_experience": "5",
            "require_visa": "No",
            "website": "",
            "linkedIn": "",
            "us_citizenship": "U.S. Citizen/Permanent Resident",
            "desired_salary": 120000,
            "current_ctc": 800000,
            "notice_period": 30,
            "linkedin_headline": "",
            "linkedin_summary": "",
            "cover_letter": "",
            "user_information_all": "",
            "recent_employer": "Not Applicable",
            "confidence_level": "8",
            "pause_before_submit": True,
            "pause_at_failed_question": True,
            "overwrite_previous_answers": False,
        },
        "search": {
            "search_terms": ["Software Engineer", "Software Developer"],
            "search_location": "United States",
            "switch_number": 30,
            "randomize_search_order": False,
            "sort_by": "",
            "date_posted": "Past week",
            "salary": "",
            "easy_apply_only": True,
            "experience_level": [],
            "job_type": [],
            "on_site": [],
            "companies": [],
            "location": [],
            "industry": [],
            "job_function": [],
            "job_titles": [],
            "benefits": [],
            "commitments": [],
            "under_10_applicants": False,
            "in_your_network": False,
            "fair_chance_employer": False,
            "pause_after_filters": True,
            "about_company_bad_words": [],
            "about_company_good_words": [],
            "bad_words": [],
            "security_clearance": False,
            "did_masters": True,
            "current_experience": 5,
        },
        "secrets": {
            "username": "username@example.com",
            "password": "example_password",
            "use_AI": False,
            "ai_provider": "openai",
            "llm_api_url": "https://api.openai.com/v1/",
            "llm_api_key": "not-needed",
            "llm_model": "gpt-5-mini",
            "llm_spec": "openai",
            "stream_output": False,
        },
        "settings": {
            "close_tabs": False,
            "follow_companies": False,
            "run_non_stop": False,
            "alternate_sortby": True,
            "cycle_date_posted": True,
            "stop_date_cycle_at_24hr": True,
            "generated_resume_path": "all resumes/",
            "file_name": "all excels/all_applied_applications_history.csv",
            "failed_file_name": "all excels/all_failed_applications_history.csv",
            "logs_folder_path": "logs/",
            "click_gap": 1,
            "run_in_background": False,
            "disable_extensions": False,
            "safe_mode": True,
            "smooth_scroll": False,
            "keep_screen_awake": True,
            "stealth_mode": True,
            "showAiErrorAlerts": False,
        },
    }
