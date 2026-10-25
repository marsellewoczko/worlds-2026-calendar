#!/usr/bin/env python3
"""Worlds 2026 match feed. Uses LoL Esports' undocumented web API; no dependencies."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from html import escape
import json
import os
import re
import time
import tempfile
import argparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
STATE = ROOT / "data" / "events.json"
# Bump when rendered event text changes, so existing subscriptions update once.
EVENT_FORMAT_VERSION = 3
BASE = "https://esports-api.lolesports.com/persisted/gw"
# Key used by the public LoL Esports website, NOT a personal API credential.
WEB_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
FROM = datetime(2026, 10, 1, tzinfo=timezone.utc)
TO = datetime(2026, 12, 1, tzinfo=timezone.utc)


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0)


def parse_time(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Naive date from API")
    return result.astimezone(timezone.utc)


def get(endpoint, params=None):
    query = urlencode({"hl": "en-US", **(params or {})})
    request = Request(
        BASE + "/" + endpoint + "?" + query,
        headers={
            "x-api-key": os.getenv("LOL_ESPORTS_API_KEY") or WEB_KEY,
            "User-Agent": "worlds-2026-community-calendar/1.0",
            "Accept": "application/json",
        },
    )
    err = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=20) as response:
                payload = json.load(response)
            data = payload.get("data")
            if not isinstance(data, dict):
                raise ValueError("LoL Esports returned an unexpected schema")
            return data
        except Exception as exc:
            err = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"LoL Esports API failure ({endpoint}): {err}")


def league_id():
    override = os.getenv("WORLDS_LEAGUE_ID")
    if override:
        return override
    leagues = get("getLeagues").get("leagues") or []
    for item in leagues:
        if str(item.get("slug", "")).lower() == "worlds":
            return str(item["id"])
    for item in leagues:
        if "world" in str(item.get("name", "")).lower() and "champ" in str(item.get("name", "")).lower():
            return str(item["id"])
    raise RuntimeError("Worlds league not found. Override WORLDS_LEAGUE_ID if necessary.")


def download(league):
    first = get("getSchedule", {"leagueId": league}).get("schedule")
    if not isinstance(first, dict):
        raise RuntimeError("Schedule unavailable")
    events = {}
    seen = set()
    pages = [first]
    for direction in ("older", "newer"):
        page = first
        for _ in range(36):
            token = (page.get("pages") or {}).get(direction)
            if not token or token in seen:
                break
            seen.add(token)
            page = get("getSchedule", {"leagueId": league, "pageToken": token}).get("schedule")
            if not isinstance(page, dict):
                raise RuntimeError("Schedule pagination failed")
            pages.append(page)
            dates = []
            for event in page.get("events") or []:
                try:
                    dates.append(parse_time(event["startTime"]))
                except (KeyError, ValueError, TypeError):
                    pass
            if dates and ((direction == "older" and max(dates) < FROM) or
                          (direction == "newer" and min(dates) >= TO)):
                break
        else:
            raise RuntimeError("Pagination exceeded safety cap")
    for page in pages:
        batch = page.get("events")
        if not isinstance(batch, list):
            raise RuntimeError("Schedule page has no events list")
        for event in batch:
            if isinstance(event, dict):
                ident = event.get("id") or (event.get("match") or {}).get("id")
                if ident is not None:
                    events[str(ident)] = event
    return list(events.values())


def team_name(team):
    if not isinstance(team, dict):
        return "TBD"
    for key in ("code", "name", "slug"):
        name = str(team.get(key) or "").strip()
        if name and name.lower() not in ("none", "tbd", "to be determined"):
            return name
    return "TBD"


def normalized(event):
    if not isinstance(event, dict):
        return None
    league = event.get("league")
    if isinstance(league, dict) and league.get("slug") not in (None, "worlds"):
        return None
    if event.get("type") not in (None, "match"):
        return None
    try:
        start = parse_time(event["startTime"])
    except (KeyError, ValueError, TypeError, AttributeError):
        return None
    if not FROM <= start < TO:
        return None
    match = event.get("match") or {}
    if not isinstance(match, dict):
        return None
    mid = str(event.get("id") or match.get("id") or "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", mid):
        return None
    teams = match.get("teams") or []
    if not isinstance(teams, list) or len(teams) != 2:
        return None
    try:
        bo = int((match.get("strategy") or {}).get("count", 1))
    except (ValueError, TypeError):
        bo = 1
    if bo not in (1, 3, 5):
        bo = 1
    item = {
        "id": mid,
        "start": start.isoformat().replace("+00:00", "Z"),
        "team1": team_name(teams[0]),
        "team2": team_name(teams[1]),
        "stage": str(event.get("blockName") or "Worlds 2026")[:120],
        "best_of": bo,
        "state": str(event.get("state") or "unstarted"),
        "format_version": EVENT_FORMAT_VERSION,
    }
    # Only explicit API game wins count as a score. Missing values are not 0–0.
    if item["state"] in ("inProgress", "completed"):
        scores = [
            team.get("result", {}).get("gameWins")
            if isinstance(team, dict) and isinstance(team.get("result"), dict) else None
            for team in teams
        ]
        target = bo // 2 + 1
        valid = all(type(score) is int and 0 <= score <= target for score in scores)
        if valid and (item["state"] != "completed" or
                      (max(scores) == target and min(scores) < target)):
            item["score"] = scores
    return item


def merge(previous, events, current):
    result = dict(previous)
    changes = 0
    accepted = 0
    for raw in events:
        item = normalized(raw)
        if not item:
            continue
        accepted += 1
        prior = result.get(item["id"])
        # A temporary missing result must not erase a previously verified score
        # for the same participants and match state, or claim it was rechecked.
        if ("score" not in item and prior and "score" in prior and
                all(item[key] == prior.get(key) for key in ("team1", "team2", "state"))):
            item["score"] = prior["score"]
            if "score_checked_at" in prior:
                item["score_checked_at"] = prior["score_checked_at"]
        elif "score" in item and item["state"] == "inProgress":
            item["score_checked_at"] = current.isoformat().replace("+00:00", "Z")
        old_data = {k: v for k, v in (prior or {}).items() if k not in ("sequence", "last_modified")}
        if item == old_data:
            continue
        item["sequence"] = int(prior.get("sequence", -1)) + 1 if prior else 0
        item["last_modified"] = current.isoformat().replace("+00:00", "Z")
        result[item["id"]] = item
        changes += 1
    if not accepted:
        raise RuntimeError("No matching Worlds 2026 events; refusing to publish an empty feed")
    return result, changes


def ordered(state):
    return sorted(state.values(), key=lambda item: (item["start"], item["id"]))


def ical_escape(text):
    return str(text).replace("\r\n", "\n").replace("\r", "\n").replace("\\", "\\\\").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def folded(line):
    # RFC 5545: 75 OCTETS, not 75 Unicode characters.
    parts, linepart, size = [], "", 0
    for char in line:
        width = len(char.encode("utf-8"))
        if size + width > 75:
            parts.append(linepart)
            linepart, size = " " + char, width + 1
        else:
            linepart, size = linepart + char, size + width
    parts.append(linepart)
    return "\r\n".join(parts)


def stamp(value):
    return parse_time(value).strftime("%Y%m%dT%H%M%SZ")


def make_ics(state):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Marsel Lewoczko//Worlds 2026 Fan Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Worlds 2026 | LoL Matches",
        "X-WR-CALDESC:Unofficial Worlds 2026 match calendar by Marsel Lewoczko",
        "REFRESH-INTERVAL;VALUE=DURATION:PT1H",
    ]
    for event in ordered(state):
        start = parse_time(event["start"])
        end = start + timedelta(hours={1: 1, 3: 3, 5: 5}[event["best_of"]])
        name = f'{event["team1"]} vs {event["team2"]} | Worlds 2026 (Bo{event["best_of"]})'
        detail = (f'{event["stage"]} | Worlds 2026.\n'
                  'End time is an estimate.')
        if "score" in event:
            score = f'{event["team1"]} {event["score"][0]}–{event["score"][1]} {event["team2"]}'
            if event["state"] == "completed":
                detail = f'Wynik końcowy / Final result: {score}\n\n' + detail
            elif event["state"] == "inProgress" and event.get("score_checked_at"):
                checked = parse_time(event["score_checked_at"]).strftime("%Y-%m-%d %H:%M UTC")
                detail = (f'Live: {score}\n'
                           f'Ostatnie pobranie / Last fetched: {checked}.\n'
                           'Wynik z ostatniej synchronizacji, nie w czasie rzeczywistym. / '
                           'Score from the last sync, not a real-time feed.\n\n') + detail
        detail += '\n\nCreated by Marsel Lewoczko — https://marsellewoczko.com'
        canceled = event["state"].lower() in ("cancelled", "canceled")
        lines.extend([
            "BEGIN:VEVENT",
            f'UID:worlds2026-riot-{event["id"]}@marsellewoczko.com',
            f'DTSTAMP:{stamp(event["last_modified"])}',
            f'LAST-MODIFIED:{stamp(event["last_modified"])}',
            f'SEQUENCE:{event["sequence"]}',
            f'DTSTART:{start.strftime("%Y%m%dT%H%M%SZ")}',
            f'DTEND:{end.strftime("%Y%m%dT%H%M%SZ")}',
            "SUMMARY:" + ical_escape(name),
            "DESCRIPTION:" + ical_escape(detail),
            "STATUS:CANCELLED" if canceled else "STATUS:CONFIRMED",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ])
    lines.append("END:VCALENDAR")
    return "\r\n".join(folded(line) for line in lines) + "\r\n"


def make_html(state, current):
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    data = json.dumps(ordered(state), ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return template.replace("%%EVENTS%%", data).replace("%%UPDATED%%", escape(current.strftime("%d %b %Y, %H:%M UTC")))


def atomic_write(path, content):
    """Replace each output only after its complete contents have been written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def run():
    current = now_utc()
    identifier = league_id()
    incoming = download(identifier)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if not isinstance(state, dict):
        raise ValueError("State file is corrupt")
    merged, changes = merge(state, incoming, current)
    # Render everything before replacing any existing output. API/schema/render
    # failures must leave the last successful build and state untouched.
    ics = make_ics(merged).encode("utf-8")
    html = make_html(merged, current).encode("utf-8")
    screenshot = (ROOT / "assets" / "calendar-example.jpg").read_bytes()
    static_files = {name: (ROOT / "static" / name).read_bytes()
                    for name in ("robots.txt", "sitemap.xml")}
    state_bytes = (json.dumps(merged, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    for name, content in static_files.items():
        atomic_write(SITE / name, content)
    atomic_write(SITE / "assets" / "calendar-example.jpg", screenshot)
    atomic_write(SITE / "calendar.ics", ics)
    atomic_write(SITE / "index.html", html)
    atomic_write(SITE / ".nojekyll", b"")
    if merged != state:
        atomic_write(STATE, state_bytes)
    print(f"Worlds league={identifier}; Riot events={len(incoming)}; published={len(merged)}; changed={changes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=STATE)
    parser.add_argument("--site", type=Path, default=SITE)
    args = parser.parse_args()
    STATE, SITE = args.state.resolve(), args.site.resolve()
    run()
