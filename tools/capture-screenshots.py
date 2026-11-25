from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json
pdir=Path(__file__).resolve().parents[1]/'docs/screenshots'
pdir.mkdir(parents=True,exist_ok=True)
base=os.environ.get('DG_TEST_URL','http://127.0.0.1:8088').rstrip('/')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('DG_CHROME_PATH'),args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
 for file in ['index','signup']:
  page.goto(base+'/'+file+'.php');page.screenshot(path=str(pdir/(file+'.png')),full_page=True)
 page.goto(base+'/index.php');page.get_by_label('Email address').fill(os.environ['DG_TEST_ADMIN_EMAIL']);page.get_by_label('Password',exact=True).fill(os.environ['DG_TEST_ADMIN_PASSWORD']);page.get_by_role('button',name='Sign in →').click();page.wait_for_url('**/dashboard.php')
 for file in ['dashboard','profile','events','resources','community','mentorship','members','admin']:
  page.goto(base+'/'+file+'.php');page.screenshot(path=str(pdir/(file+'.png')),full_page=True)
 # Upload an actual PNG, exercise server validation and rendered profile image.
 page.goto(base+'/profile.php');page.locator('input[type=file]').set_input_files(str(pdir/'index.png'));page.get_by_role('button',name='Save profile →').click();page.wait_for_url('**/profile.php');assert page.locator('.profile-photo').count()==1
 # Reject PHP-like payload even if file extension looks plausible.
 bad=str(pdir/'invalid-photo.tmp');Path(bad).write_text('<?php echo "bad"; ?>')
 page.locator('input[type=file]').set_input_files(bad);page.get_by_role('button',name='Save profile →').click();page.wait_for_url('**/profile.php');assert 'Upload a JPG' in page.content()
 for width in [390,768,1440]:
  page.set_viewport_size({'width':width,'height':900})
  for file in ['dashboard','index','signup','events','resources','community','mentorship','profile','admin']:
   page.goto(base+'/'+file+'.php')
   overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth+2')
   assert not overflow,(width,file)
  page.goto(base+'/dashboard.php');page.screenshot(path=str(pdir/f'mobile-{width}.png'),full_page=True)
 assert not errors,errors
 Path(bad).unlink()
 (pdir.parent/'browser-results.json').write_text(json.dumps({'responsive_route_checks':27,'valid_photo_upload':'PASS','invalid_photo_rejection':'PASS','js_errors':errors},indent=2))
 print('Browser PASS: 27 responsive routes, valid photo upload, invalid photo rejection, no JS errors.')
 browser.close()
