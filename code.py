import requests
import base64
import re
import os

from sympy import false, true

BASE_URL = "https://newerp.kluniversity.in/index.php?r=studentinfo/studentendexamresult/download_script_frompath"

USE_MID_TAG = True  # 🔁 Toggle ON/OFF

course_map = {
	"22AD2001P": "DATA DRIVEN ARTIFICIAL INTELLIGENT SYSTEMS",
	"22CS2205P": "DESIGN & ANALYSIS OF ALGORITHMS",
	"22CSB3101P": "CRYPT ANALYSIS & CYBER DEFENSE",
	"22CSB3304P": "DIGITAL FORENSICS",
	"22EC2210P": "NETWORK PROTOCOLS & SECURITY",
	"22SDCS05P": "CLOUD BASED SECURITY SPECIALITY",
	"22AD2102R": "DATABASE MANAGEMENT SYSTEMS",
	"22CI2001": "ADAPTIVE SOFTWARE ENGINEERING",
	"22CS2002R": "AUTOMATA THEORY AND FORMAL LANGUAGES",
	"22CS2103A": "ADVANCED OBJECT ORIENTED PROGRAMMING",
	"22CS2104R": "OPERATING SYSTEMS",
	"22CS2221F": "UX DESIGN",
	"22CS2233": "INTRODUCTION TO BLOCKCHAIN AND CRYPTO CURRENCIES",
	"22CS2235F": "COMPILER DESIGN",
	"22CS4106": "PARALLEL & DISTRIBUTED COMPUTING",
	"22CSB3202": "NETWORK & INFRASTRUCTURE SECURITY",
	"22CSB3406M": "PROGRAMMING FOR SMART CONTRACTS",
	"22CSB3510": "SECURITY GOVERNANCE AND MANAGEMENT",
	"22CY1001": "ENGINEERING CHEMISTRY",
	"22EC2106": "PROCESSORS & CONTROLLERS",
	"22MT2004": "MATHEMATICAL PROGRAMMING",
	"22MT2005": "PROBABILITY, STATISTICS & QUEUEING THEORY",
	"22PH4102": "APPLIED PHYSICS",
	"22UC0010": "UNIVERSAL HUMAN VALUES AND PROFESSIONAL ETHICS",
	"OECM0002": "COST ACCOUNTING",
	"OECM0003": "DECISION ACCOUNTING",
}


cookies = {
    "kl_erp_device_id": "kl_erp_device_id",
    "SERVERID": "SERVERID",
    "PHPSESSID": "PHPSESSID",
    "_csrf": "_csrf"
}



file_ids = [
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDWTEwMDEvNTY3MDc3MTgzOTEyNzMyNi5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDU0IzNDA2TS81NjcwNzcxODM1MTI3NDA0LnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJVQzAwMTAvNTY3MDc3MTQ5MTEzMDk0NS5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDU0IzNTEwLzU2NzA3NzE4MzYxMzA4NjAucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDWTEwMDEvNTY3MDc3MTgzOTEzMDc4NC5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDU0IzNDA2TS81NjcwNzcxODM1MTMwNzQyLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJVQzAwMTAvNTY3MDc3MTQ5MTEyNzUyNS5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L09kZFNlbS9SZWd1bGFyLzQvMjJDU0IzNTEwLzU2NzA3NzE4MzYxMjc0ODUucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L0V2ZW5TZW0vUmVndWxhci80L09FQ00wMDAzLzU2NzA3Nzc2MDIxNDEyMjMucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L0V2ZW5TZW0vUmVndWxhci80L09FQ00wMDAyLzU2NzA3Nzc0NTkxNDExNzQucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJDU0IzMjAyLzU2NzA3NTU5MjE5OTI5Ny5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJDUzIyMjFGLzU2NzA3NTU4ODI5ODk0NS5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJQSDQxMDIvNTY3MDc1OTgzMzk4ODE0LnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJDU0IzMjAyLzIyMjIxNzE3NTcucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJDUzIyMjFGLzU2NzA3NTU4ODI5NDYyMS5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L09kZFNlbS9SZWd1bGFyLzMvMjJQSDQxMDIvNTY3MDc1OTgzMzk0NTU0LnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L0V2ZW5TZW0vUmVndWxhci8zLzIyQ1M0MTA2LzU2NzA3NjQ5NTAxMDk3MTAucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNC0yMDI1L0V2ZW5TZW0vUmVndWxhci8zLzIyQ1M0MTA2LzU2NzA3NjQ5NTAxMDc1NDYucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJNVDIwMDQvOTI0MDI2NDUucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJDSTIwMDEvOTIxMTQ3NDYucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJBRDIxMDJSLzkyNDMxMTgzLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJDUzIxMDNBLzkyMjIwNjkzLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJFQzIxMDYvOTIyMjY3NzIucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJDSTIwMDEvOTI4Nzk3MzIucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJFQzIxMDYvOTQ0ODI3ODAucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJNVDIwMDQvOTIxNjMwNTAucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJDUzIxMDNBLzkyMzUyNjkxLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L09kZFNlbS9SZWd1bGFyLzIvMjJBRDIxMDJSLzkyNjI1MzUyLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyTVQyMDA1Lzk4MjE2NzUzLnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMjMzLzk4MzgyMTI2LnBkZg==",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMTA0Ui85ODMxMzY5Mi5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMDAyUi85ODQwOTEzNS5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyTVQyMDA1LzU2NzA3NTE0NjU3OTMyMC5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMTA0Ui81NjcwNzUxNTM4NzkzOTMucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMjMzLzU2NzA3NTE1MDI3OTQ0MC5wZGY=",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L0V2ZW5TZW0vUmVndWxhci8yLzIyQ1MyMDAyUi81NjcwNzUyNDQ5Nzk3NzQucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L1N1bW1lclRlcm0vUmVndWxhci8yLzIyQ1MyMjM1Ri84ODgxNDEzNTMucGRm",
	"NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyMy0yMDI0L1N1bW1lclRlcm0vUmVndWxhci8yLzIyQ1MyMjM1Ri84ODgxMzgxNjUucGRm",
    "NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L0V2ZW5TZW0vUmVndWxhci80L09FQ00wMDAzLzU2NzA3Nzc2MDIxNDc3MjEucGRm",
    "NTY3MDd8cXVlc3Rpb25fcGFwZXIvMjAyNS0yMDI2L0V2ZW5TZW0vUmVndWxhci80L09FQ00wMDAyLzU2NzA3Nzc0NTkxNDc3OTAucGRm"
]

# 🔹 store course-wise file numbers
course_files = {}

def decode_info(encoded_id):
    try:
        decoded = base64.b64decode(encoded_id).decode("utf-8", errors="ignore")
        parts = decoded.split("|")[-1].split("/")

        year = parts[1] if len(parts) > 1 else "unknown_year"
        sem = parts[2] if len(parts) > 2 else "unknown_sem"
        sem = sem.replace("OddSem", "Odd").replace("EvenSem", "Even")

        course_code = parts[-2] if len(parts) >= 2 else None
        course_name = course_map.get(course_code, course_code or "unknown_course")
        safe_course_name = re.sub(r"[^a-zA-Z0-9._\-&]", "_", course_name)

        file_number = parts[-1].replace(".pdf", "")

        # 👉 store for grouping
        course_files.setdefault(safe_course_name, []).append(file_number)

        folder = os.path.join(year, sem)

        return {
            "folder": folder,
            "year": year,
            "sem": sem,
            "course": safe_course_name,
            "file_number": file_number,
            "file_id": encoded_id
        }

    except Exception:
        return {
            "folder": "misc",
            "year": "unknown",
            "sem": "unknown",
            "course": "unknown",
            "file_number": encoded_id,
            "file_id": encoded_id
        }


def get_mid_tag(course, file_number):
    files = course_files.get(course, [])

    if len(files) < 2:
        return ""

    sorted_files = sorted(files)

    if file_number == sorted_files[0]:
        return "MID1"
    else:
        return "MID2"


def download_pdf(file_data, cookies):
    url = f"{BASE_URL}&id={file_data['file_id']}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Referer": "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fview_my_answer_scripts",
    }

    folder = file_data["folder"]
    os.makedirs(folder, exist_ok=True)

    mid_tag = get_mid_tag(file_data["course"], file_data["file_number"]) if USE_MID_TAG else ""

    if USE_MID_TAG and mid_tag:
        filename = f"{file_data['year']}_{file_data['sem']}_{file_data['course']}_{mid_tag}.pdf"
    else:
        filename = f"{file_data['year']}_{file_data['sem']}_{file_data['course']}_{file_data['file_number']}.pdf"

    full_path = os.path.join(folder, filename)

    print(f"Downloading to: {full_path}")

    if os.path.exists(full_path):
        print(f"Skipping existing: {full_path}")
        return

    response = requests.get(url, headers=headers, cookies=cookies, stream=True)

    if response.status_code == 200:
        with open(full_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        print(f"Downloaded: {full_path}")
    else:
        print(f"Failed: {response.status_code}")


# 🔁 remove duplicates
unique_file_ids = list(dict.fromkeys(file_ids))

# ✅ STEP 1: preprocess all files
decoded_data = [decode_info(fid) for fid in unique_file_ids]

# ✅ STEP 2: download with MID logic
for data in decoded_data:
    download_pdf(data, cookies)