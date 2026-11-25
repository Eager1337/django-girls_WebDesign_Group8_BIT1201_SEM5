"""Browser QA on a disposable installation. Requires Playwright and Chrome."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json
base=os.environ.get('DG_TEST_URL','http://127.0.0.1:8088')
out=Path(os.environ.get('DG_SCREENSHOT_DIR','docs/screenshots-final'));out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROME_PATH','/usr/bin/google-chrome'),args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000})
 page.on('pageerror',lambda e:errors.append(str(e)))
 for theme in ['dark','light']:
  for width in [390,768,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   for route in ['index','signup']:
    page.goto(base+'/'+route+'.php');page.evaluate('(t)=>{localStorage.setItem("dg-theme",t)}',theme);page.reload();page.wait_for_timeout(1100)
    assert page.evaluate('document.documentElement.dataset.theme')==theme
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(width,route,theme)
    assert page.locator('.prism-face').count()==6
    page.screenshot(path=str(out/f'{route}-{width}-{theme}.png'),full_page=True);checks.append([route,width,theme])
 page.goto(base+'/index.php')
 page.get_by_label('Email address').fill(os.environ['DG_TEST_ADMIN_EMAIL'])
 page.get_by_label('Password',exact=True).fill(os.environ['DG_TEST_ADMIN_PASSWORD'])
 page.get_by_role('button',name='Sign in →').click();page.wait_for_url('**/dashboard.php')
 for theme in ['dark','light']:
  page.evaluate('(t)=>localStorage.setItem("dg-theme",t)',theme)
  for width in [390,768,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   for route in ['dashboard','events','resources','community','mentorship','members','profile','admin','hub','challenges','showcase','calendar','search','achievements','notifications']:
    response=page.goto(base+'/'+route+'.php');page.wait_for_timeout(1100)
    assert response.status==200,(route,response.status)
    assert page.evaluate('document.documentElement.dataset.theme')==theme
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(width,route,theme)
    assert not page.evaluate('Boolean(window.untrustedExecuted)')
    page.screenshot(path=str(out/f'{route}-{width}-{theme}.png'),full_page=True);checks.append([route,width,theme])
 page.locator('.theme-toggle').click();selected=page.evaluate('document.documentElement.dataset.theme');page.reload()
 assert page.evaluate('document.documentElement.dataset.theme')==selected
 page.emulate_media(reduced_motion='reduce')
 assert page.locator('.reveal').first.evaluate('e=>getComputedStyle(e).animationName')=='none'
 assert not errors,errors
 (out/'results.json').write_text(json.dumps(dict(checks=checks,total=len(checks),js_errors=errors,reduced_motion='PASS',theme_persistence='PASS'),indent=2))
 print(f'PASS {len(checks)} viewport/theme checks, reduced motion, theme persistence, no JS errors')
 browser.close()