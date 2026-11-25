"""HTTP innovation regressions. Disposable DB only; administrator credentials via environment."""
import os,re,sys,time,json,urllib.request,urllib.parse,urllib.error,http.cookiejar
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8088').rstrip('/')
results=[]
class Client:
 def __init__(self): self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def request(self,path,data=None):
  try:
   r=self.opener.open(BASE+'/'+path,None if data is None else urllib.parse.urlencode(data).encode());return r.status,r.geturl(),r.read().decode()
  except urllib.error.HTTPError as e:return e.code,e.url,e.read().decode()
 def token(self,path='dashboard.php'):return re.search(r'name="csrf" value="([^"]+)"',self.request(path)[2])[1]
 def act(self,action,**fields):return self.request('innovate.php',dict(csrf=self.token(),action=action,**fields))
def check(name,ok):
 results.append(dict(test=name,result='PASS' if ok else 'FAIL'));print(results[-1]['result'],name)
 if not ok:raise AssertionError(name)
stamp=str(time.time_ns());password='InnovationTests2026!'
anon=Client();member=Client();other=Client();admin=Client()
for route in ['hub','challenges','showcase','calendar','search','achievements','notifications']:
 check('Protected '+route,'index.php' in anon.request(route+'.php')[1])
for c,name in [(member,'Innovator'),(other,'Reviewer')]:
 email=name+stamp+'@example.test'
 c.request('signup.php',dict(csrf=c.token('signup.php'),name=name,email=email,password=password,confirm=password,interests='PHP'))
 check('Login '+name,'dashboard.php' in c.request('index.php',dict(csrf=c.token('index.php'),email=email,password=password))[1])
admin.request('index.php',dict(csrf=admin.token('index.php'),email=os.environ['DG_TEST_ADMIN_EMAIL'],password=os.environ['DG_TEST_ADMIN_PASSWORD']))
check('Innovation CSRF',member.request('innovate.php',dict(action='project',csrf='bad'))[0]==403)
check('Upgrade browser denied',anon.request('tools/upgrade.php')[0]==403)
for route in ['hub','challenges','showcase','calendar','search','achievements','notifications']:
 check('Loads '+route,member.request(route+'.php')[0]==200)
html=member.request('challenges.php')[2];cid=re.search(r'value="submit_challenge"><input type="hidden" name="id" value="(\d+)"',html)[1]
code='<script>window.untrustedExecuted=true</script> <?php echo "NOT RUN"; ?> '+stamp
response=member.act('submit_challenge',id=cid,solution=code)
check('Submission saved and escaped','&lt;script&gt;' in response[2] and '<script>window.untrustedExecuted' not in response[2])
check('Revise unapproved', 'Revised '+stamp in member.act('submit_challenge',id=cid,solution='Revised '+stamp)[2])
html=admin.request('challenges.php')[2];segment=html.split('Revised '+stamp)[1];sid=re.search(r'value="review_challenge"><input type="hidden" name="id" value="(\d+)"',segment)[1]
check('Review admin-only',member.act('review_challenge',id=sid,status='approved',review='Forbidden')[0]==403)
check('Manual review saved','Helpful review '+stamp in admin.act('review_challenge',id=sid,status='approved',review='Helpful review '+stamp)[2])
check('Approved edit blocked','cannot be changed' in member.act('submit_challenge',id=cid,solution='Overwrite')[2])
check('Review notification','coding challenge has new feedback' in member.request('notifications.php')[2])
check('No private review in other inbox','coding challenge has new feedback' not in other.request('notifications.php')[2])
title='Innovation project '+stamp
response=member.act('project',title=title,description=code,url='https://example.org/')
pid=re.search(r'project=(\d+)',response[1])[1]
check('Project safe rendering',title in response[2] and '&lt;script&gt;' in response[2])
check('URL scheme rejected','valid http or https' in member.act('project',title='Unsafe',description='Test',url='javascript:alert(1)')[2])
check('Owner deletion enforced','cannot remove' in other.act('project_delete',id=pid)[2])
check('Feedback saved','Useful feedback '+stamp in other.act('feedback',id=pid,body='Useful feedback '+stamp)[2])
check('Owner notified','left feedback on your project' in member.request('notifications.php')[2])
check('Real activity in feed',title in other.request('hub.php')[2])
html=other.request('hub.php')[2];segment=html.split(title)[1];fid=re.search(r'value="reaction"><input type="hidden" name="id" value="(\d+)"',segment)[1]
check('Reaction add','Saved successfully' in other.act('reaction',id=fid,mode='add')[2])
check('Reaction repeated safely','Saved successfully' in other.act('reaction',id=fid,mode='add')[2])
check('Reaction remove','Saved successfully' in other.act('reaction',id=fid,mode='remove')[2])
check('Global search finds project',title in member.request('search.php?q='+urllib.parse.quote(title))[2])
check('Search private exclusion','Revised '+stamp not in other.request('search.php?q='+stamp)[2])
check('Search wildcard escaping',member.request('search.php?q=%25_%21')[0]==200)
check('Invalid calendar input safe',member.request('calendar.php?month=not-a-date')[0]==200)
check('Mark own inbox read','Saved successfully' in member.act('read_all')[2])
check('Project cascade delete',title not in member.act('project_delete',id=pid)[2])
check('Deleted project absent feed',title not in other.request('hub.php')[2])
check('Deleted project 404',other.request('showcase.php?project='+pid)[0]==404)
open(os.path.join(os.path.dirname(__file__),'innovation-results.json'),'w').write(json.dumps(results,indent=2))
print(str(len(results))+' innovation checks passed. Test data remains in disposable DB only.')