"""End-to-end checks against a disposable MySQL installation. Python 3 standard library only.
Run: python tests/integration.py http://127.0.0.1:8088
Admin credentials supplied via DG_TEST_ADMIN_EMAIL and DG_TEST_ADMIN_PASSWORD environment vars.
"""
import os,re,sys,time,json,urllib.request,urllib.parse,http.cookiejar
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8088').rstrip('/')
results=[]
class Client:
 def __init__(self):self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def get(self,path):
  try:r=self.opener.open(BASE+'/'+path);return r.status,r.geturl(),r.read().decode()
  except urllib.error.HTTPError as e:return e.code,e.url,e.read().decode()
 def post(self,path,data):
  try:r=self.opener.open(BASE+'/'+path,urllib.parse.urlencode(data).encode());return r.status,r.geturl(),r.read().decode()
  except urllib.error.HTTPError as e:return e.code,e.url,e.read().decode()
 def token(self,path='dashboard.php'):
  s=self.get(path)[2];return re.search(r'name="csrf" value="([^"]+)"',s)[1]
def check(name,condition):
 results.append({'test':name,'result':'PASS' if condition else 'FAIL'})
 print(results[-1]['result'],name)
 if not condition:raise AssertionError(name)
def action(c,a,**kw):return c.post('action.php',{'csrf':c.token(),'action':a,**kw})
a=Client();m=Client();stamp=str(int(time.time()));email='learner'+stamp+'@example.test';pw='LearnerPassword2026!'
check('Unauthenticated dashboard redirects to login','index.php' in m.get('dashboard.php')[1])
check('Invalid CSRF rejected',m.post('signup.php',{'csrf':'bad'})[2].find('expired')>=0)
form={'csrf':m.token('signup.php'),'name':'Integration Learner','email':email,'interests':'PHP','password':'weak','confirm':'weak'}
check('Weak password rejected','10–72' in m.post('signup.php',form)[2])
form.update(password=pw,confirm=pw);form['csrf']=m.token('signup.php')
check('Registration works','Account created' in m.post('signup.php',form)[2])
form['csrf']=m.token('signup.php');check('Duplicate email rejected','already registered' in m.post('signup.php',form)[2])
check('Incorrect password rejected','incorrect' in m.post('index.php',{'csrf':m.token('index.php'),'email':email,'password':'wrong'})[2])
check('Member login works','Hello, Integration.' in m.post('index.php',{'csrf':m.token('index.php'),'email':email,'password':pw})[2])
check('Member cannot access admin',m.get('admin.php')[0]==403)
check('Member cannot export report',m.get('report.php')[0]==403)
check('Action CSRF enforced',m.post('action.php',{'action':'complete','id':1,'csrf':'bad'})[0]==403)
check('Event registration works','You are registered' in action(m,'event_join',id=1)[2])
check('Duplicate event rejected','already registered' in action(m,'event_join',id=1)[2])
check('Resource completion works','Completed · Undo' in action(m,'complete',id=1)[2])
check('Resource undo works','Mark completed' in action(m,'uncomplete',id=1)[2])
check('Search filters resources','Django Girls tutorial' not in m.get('resources.php?q=PHP')[2])
check('Profile update works','Integration Updated' in action(m,'profile',name='Integration Updated',interests='PHP',bio='Learning safely.')[2])
topic=action(m,'topic',title='Test discussion '+stamp,body='<script>alert(1)</script> A question.');tid=re.search(r'topic=(\d+)',topic[1])[1]
check('Discussion escaped','&lt;script&gt;' in topic[2] and '<script>alert(1)</script>' not in topic[2])
check('Reply works','Helpful reply' in action(m,'reply',id=tid,body='Helpful reply')[2])
check('Admin login works','dashboard.php' in a.post('index.php',{'csrf':a.token('index.php'),'email':os.environ['DG_TEST_ADMIN_EMAIL'],'password':os.environ['DG_TEST_ADMIN_PASSWORD']})[1])
check('Admin page loads',a.get('admin.php')[0]==200)
check('Analytics CSV exports','events_joined' in a.get('report.php')[2])
# Find test member from admin page and promote to mentor.
html=a.get('admin.php')[2];segment=html.split(email)[1];uid=re.search(r'name="id" value="(\d+)"',segment)[1]
check('Role assignment works','Saved successfully' in action(a,'user_update',id=uid,role='mentor',active=1)[2])
# Create a second member and request mentorship.
b=Client();email2='mentee'+stamp+'@example.test'
b.post('signup.php',{'csrf':b.token('signup.php'),'name':'Test Mentee','email':email2,'interests':'PHP','password':pw,'confirm':pw})
b.post('index.php',{'csrf':b.token('index.php'),'email':email2,'password':pw})
check('Mentorship request works','pending' in action(b,'mentor_request',id=uid,message='Help with PHP forms.')[2].lower())
html=m.get('mentorship.php')[2];rid=re.search(r'name="action" value="mentor_response"><input type="hidden" name="id" value="(\d+)"',html)[1]
check('Mentor acceptance works','Accepted' in action(m,'mentor_response',id=rid,status='accepted')[2])
# Attendance on member registration
check('Attendance recording works','Saved successfully' in action(a,'attendance',id=1,user_id=uid,attended=1)[2])
check('Member sees attendance','Attendance confirmed' in m.get('events.php')[2])
# Content create/update/delete
r=action(a,'event_save',title='Test event '+stamp,description='Test event',starts_at='2027-01-01T10:00',location='Lab',capacity=1)
check('Admin event create works','Test event '+stamp in r[2])
eid=re.search(r'name="action" value="event_save"><input type="hidden" name="id" value="(\d+)"',r[2].split('Test event '+stamp)[1])[1]
check('Event update works','Changed title' in action(a,'event_save',id=eid,title='Changed title',description='Updated',starts_at='2027-01-01T10:00',location='Lab',capacity=1)[2])
check('Limited event first place works','You are registered' in action(b,'event_join',id=eid)[2])
check('Full event rejects second member','This event is full' in action(m,'event_join',id=eid)[2])
check('Event cancellation works','You are registered' not in action(b,'event_leave',id=eid)[2])
check('Admin event delete works','Changed title' not in action(a,'event_delete',id=eid)[2])
check('Invalid resource URL rejected','valid http or https' in action(a,'resource_save',title='Bad link',category='PHP',url='javascript:alert(1)',description='Bad')[2])
rr=action(a,'resource_save',title='Test resource '+stamp,category='PHP',url='https://www.php.net/',description='Test resource')
check('Resource creation works','Test resource '+stamp in rr[2])
resid=re.search(r'name="action" value="resource_save"><input type="hidden" name="id" value="(\d+)"',rr[2].split('Test resource '+stamp)[1])[1]
check('Resource editing works','Edited resource '+stamp in action(a,'resource_save',id=resid,title='Edited resource '+stamp,category='PHP',url='https://www.php.net/',description='Edited')[2])
check('Resource deletion works','Edited resource '+stamp not in action(a,'resource_delete',id=resid)[2])
check('Admin moderation works','Test discussion '+stamp not in action(a,'topic_delete',id=tid)[2])
check('Suspension works','Saved successfully' in action(a,'user_update',id=uid,role='member',active=0)[2])
check('Suspended session blocked','index.php' in m.get('dashboard.php')[1])
check('Logout works','index.php' in b.post('logout.php',{'csrf':b.token()})[1])
check('Logged out dashboard protected','index.php' in b.get('dashboard.php')[1])
unknown='throttle'+stamp+'@example.test'
for _ in range(5):b.post('index.php',{'csrf':b.token('index.php'),'email':unknown,'password':'wrong'})
check('Login throttling works','Too many attempts' in b.post('index.php',{'csrf':b.token('index.php'),'email':unknown,'password':'wrong'})[2])
check('Installer cannot run through browser',b.get('tools/install.php')[0]==403)
open(os.path.join(os.path.dirname(__file__),'results.json'),'w').write(json.dumps(results,indent=2))
print(f'{len(results)} checks passed. Test accounts remain in disposable DB only.')
