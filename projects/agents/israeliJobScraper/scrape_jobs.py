#!/usr/bin/env python3
import csv
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

CSV_OUT_HEADERS = ["company name", "job title", "link to posting"]

ATS_HOST_HINTS = [
    "boards.greenhouse.io",
    "jobs.lever.co",
    "myworkdayjobs.com",
    "smartrecruiters.com",
    "workable.com",
    "ashbyhq.com",
    "comeet.co",
    "bamboohr.com",
    "recruitee.com",
    "jobvite.com",
    "successfactors",
    "taleo.net",
    "icims.com",
    "talentlms",
]

AGGREGATORS = ["linkedin.com", "indeed.", "glassdoor.", "ziprecruiter.", "monster."]

DATE_TEXT_PATTERNS = [
    r"Posted on\s+([A-Za-z]{3,9}\.?,?\s+\d{1,2},\s+\d{4})",
    r"Posted\s*:\s*([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})",
    r"(\d{4}-\d{2}-\d{2})",
]


def log(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def fetch(url: str) -> Optional[str]:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=45)
        if r.status_code >= 400:
            return None
        return r.text
    except Exception:
        return None


def within_days(date_str: str, days: int) -> bool:
    try:
        dt = dateparser.parse(date_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - dt) <= timedelta(days=days)
    except Exception:
        return False


def extract_jsonld_job(html: str) -> Tuple[Optional[str], Optional[str]]:
    # returns (title, datePosted)
    try:
        import json

        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script", {"type": "application/ld+json"}):
            try:
                data = json.loads(script.string or "{}")
            except Exception:
                continue
            objs = data if isinstance(data, list) else [data]
            for obj in objs:
                if not isinstance(obj, dict):
                    continue
                at = obj.get("@type")
                if at == "JobPosting" or (isinstance(at, list) and "JobPosting" in at):
                    title = obj.get("title")
                    date_posted = obj.get("datePosted") or obj.get("datePublished")
                    if title or date_posted:
                        return title, date_posted
    except Exception:
        pass
    return None, None


def extract_visible_date(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    for pat in DATE_TEXT_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def extract_title_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""


def same_site_job_link(career_url: str, href: str) -> bool:
    from urllib.parse import urlparse

    try:
        cu = urlparse(career_url)
        hu = urlparse(href)
        return cu.netloc == hu.netloc and any(
            s in hu.path.lower() for s in ["/job", "/jobs", "/careers", "/positions", "/opportunities"]
        )
    except Exception:
        return False


def gather_job_links(career_url: str, html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("#"):
            continue
        if href.startswith("/"):
            from urllib.parse import urljoin

            href = urljoin(career_url, href)
        if not href.startswith("http"):
            continue
        if any(host in href for host in AGGREGATORS):
            continue
        if any(host in href for host in ATS_HOST_HINTS) or same_site_job_link(career_url, href):
            links.append(href)
    # de-dup while preserving order
    seen = set()
    out = []
    for u in links:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out[:60]  # cap per-company scan


def read_companies(csv_path: str) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            name = row[0].strip()
            url = row[1].strip()
            if not name or not url:
                continue
            items.append((name, url))
    return items


def write_jobs(csv_path: str, rows: List[Tuple[str, str, str]]):
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_OUT_HEADERS)
        for r in rows:
            writer.writerow(r)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Collect 10 recent (<=30d) job postings from companies list")
    parser.add_argument("--companies", type=str, required=True, help="Path to companies.csv")
    parser.add_argument("--out", type=str, default="jobs.csv", help="Output CSV path")
    parser.add_argument("--max", type=int, default=10, help="Max results")
    parser.add_argument("--days", type=int, default=30, help="Recency window in days")
    args = parser.parse_args()

    companies = read_companies(args.companies)
    results: List[Tuple[str, str, str]] = []
    scanned = 0

    for company, careers_url in companies:
        if len(results) >= args.max:
            break
        careers_html = fetch(careers_url)
        if not careers_html:
            continue
        job_links = gather_job_links(careers_url, careers_html)
        for job_url in job_links:
            if len(results) >= args.max:
                break
            job_html = fetch(job_url)
            if not job_html:
                continue
            title_j, date_j = extract_jsonld_job(job_html)
            title = title_j or extract_title_from_html(job_html)
            if not title:
                continue
            date_text = date_j or extract_visible_date(job_html)
            if not date_text or not within_days(date_text, args.days):
                continue
            # Accept only if looks like a job description (not a hub page)
            soup = BeautifulSoup(job_html, "html.parser")
            body_text = soup.get_text(" ", strip=True)
            if len(body_text) < 500:
                continue
            results.append((company, title.strip(), job_url))
            # be polite
            time.sleep(0.3)
        scanned += 1
        time.sleep(0.4)

    if not results:
        log("No recent postings found within 30 days.")
        sys.exit(2)

    write_jobs(args.out, results[: args.max])
    log(f"Wrote {len(results[: args.max])} rows to {args.out}")


if __name__ == "__main__":
    main()


