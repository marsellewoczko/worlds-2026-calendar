"""Optional real-browser smoke checks; pip install playwright, supply Chromium.
Usage: python tools/browser_smoke.py http://127.0.0.1:8001 --chromium /usr/bin/chromium
Requires a site generated from a nonempty schedule; never creates production data.
"""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('url')
parser.add_argument('--chromium', default='/usr/bin/chromium')
args = parser.parse_args()

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
    for timezone in ('Europe/Warsaw', 'America/New_York'):
        context = browser.new_context(viewport={'width': 390, 'height': 844}, locale='pl-PL', timezone_id=timezone)
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        response = page.goto(args.url)
        assert response.status == 200
        assert page.locator('html').get_attribute('lang') == 'pl'
        events = json.loads(page.locator('#data').text_content())
        assert events and page.locator('.event').count() == len(events)
        assert page.locator('#tz').inner_text() == timezone
        expected_time = page.evaluate("start => new Intl.DateTimeFormat('pl-PL',{hour:'2-digit',minute:'2-digit'}).format(new Date(start))", events[0]['start'])
        assert page.locator('.time').first.inner_text() == expected_time
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        feed = page.locator('#feed').inner_text()
        assert feed.endswith('/calendar.ics')
        assert page.locator('#apple').get_attribute('href') == feed.replace('http:', 'webcal:').replace('https:', 'webcal:')
        assert page.request.get(feed).status == 200
        page.locator('#copy').click()
        page.wait_for_function("document.getElementById('copy').textContent.includes('✓')")
        assert page.evaluate('navigator.clipboard.readText()') == feed
        page.locator('#en').click()
        assert page.locator('html').get_attribute('lang') == 'en'
        assert page.locator('#scheduleTitle').inner_text() == 'Match schedule'
        page.reload()
        assert page.locator('html').get_attribute('lang') == 'en'
        page.set_viewport_size({'width': 1280, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not errors, errors
        print(f'PASS {timezone}: {len(events)} matches, mobile/desktop, PL/EN, local time, clipboard, subscription')
        context.close()
    context = browser.new_context()
    context.add_init_script("Object.defineProperty(window, 'localStorage', {get(){throw new Error('Storage blocked')}})")
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(args.url)
    assert page.locator('.event').count() > 0
    page.locator('#pl').click()
    assert page.locator('html').get_attribute('lang') == 'pl'
    assert not errors, errors
    print('PASS disabled localStorage: schedule and language toggle remain usable')
    browser.close()
