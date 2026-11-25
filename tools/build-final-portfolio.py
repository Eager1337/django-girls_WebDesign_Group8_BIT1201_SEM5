"""Build the revised five-page A3 portfolio from actual final screenshots."""
from pathlib import Path
import re,shutil,html
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from docx import Document
from docx.shared import Mm,Pt,Inches
import qrcode
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs';S=D/'screenshots';S.mkdir(exist_ok=True)
def get_fonts():
    candidates = [
        ('C:/Windows/Fonts/tahoma.ttf', 'C:/Windows/Fonts/tahomabd.ttf'),
        ('/usr/share/wine/fonts/tahoma.ttf', '/usr/share/wine/fonts/tahomabd.ttf'),
        ('/tmp/fonts/tahoma.ttf', '/tmp/fonts/tahomabd.ttf'),
        ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'),
    ]
    for r, b in candidates:
        if Path(r).exists() and Path(b).exists():
            return r, b
    return candidates[-1]
FONT, BOLD = get_fonts()
source=Path('/home/user/innovation-preview')
if source.exists():
 for p in source.glob('*-1440-dark.png'):shutil.copy2(p,S/(p.name.replace('-1440-dark','')))
 for width in (390,768,1440):shutil.copy2(source/f'hub-{width}-dark.png',S/f'mobile-{width}.png')
 shutil.copy2(source/'results.json',D/'visual-results.json')
tables={
'users':'PK id; UNIQUE email | hash, role, active, profile',
'events':'PK id | date, capacity, location',
'registrations':'PK/FK user_id + event_id | attendance',
'resources':'PK id | title, category, url',
'progress':'PK/FK user_id + resource_id | completion',
'topics':'PK id; FK user_id | title, body',
'replies':'PK id; FK user_id, topic_id | body',
'mentorships':'PK id; FK member_id, mentor_id | UNIQUE pair, status',
'audit_log':'PK id; FK user_id nullable | action, time',
'login_attempts':'PK email | attempts, last_attempt',
'activity_days':'PK/FK user_id + activity_date | dated practice',
'challenges':'PK id | prompt, difficulty, active',
'challenge_submissions':'PK id; FK user_id, challenge_id | UNIQUE user/date, review',
'projects':'PK id; FK user_id | description, url',
'project_feedback':'PK id; FK user_id, project_id | body',
'activity_feed':'PK id; FK user_id | kind, source_id, url',
'feed_reactions':'PK/FK user_id + feed_id | explicit cheer',
'notifications':'PK id; FK user_id | UNIQUE user/dedupe, read',
'app_migrations':'PK version | applied_at'}
edges=[('users','registrations'),('events','registrations'),('users','progress'),('resources','progress'),('users','topics'),('users','replies'),('topics','replies'),('users','mentorships'),('users','audit_log'),('users','activity_days'),('users','challenge_submissions'),('challenges','challenge_submissions'),('users','projects'),('users','project_feedback'),('projects','project_feedback'),('users','activity_feed'),('users','feed_reactions'),('activity_feed','feed_reactions'),('users','notifications')]
im=Image.new('RGB',(2200,1550),'#f5f5fa');dr=ImageDraw.Draw(im);f=ImageFont.truetype(FONT,21);fb=ImageFont.truetype(BOLD,29)
pos={k:(30+(i%4)*550,40+(i//4)*300) for i,k in enumerate(tables)}
for a,b in edges:
 x,y=pos[a];xx,yy=pos[b];dr.line((x+255,y+125,xx+255,yy+125),fill='#b8bac8',width=2)
for i,(k,v) in enumerate(tables.items()):
 x,y=pos[k];dr.rounded_rectangle((x,y,x+510,y+235),radius=16,fill='white',outline='#9398aa',width=2);dr.rounded_rectangle((x,y,x+510,y+56),radius=12,fill='#17181f');dr.text((x+16,y+12),k,font=fb,fill=['#75d5ff','#d99bee','#ffb879'][i%3])
 for j,t in enumerate(v.split(' | ')):dr.text((x+16,y+83+j*49),t,font=f,fill='#30313b')
im.save(D/'erd.png')
(D/'erd.mmd').write_text('erDiagram\n'+''.join(f' {a} ||--o{{ {b} : relates\n' for a,b in edges)+''.join(f' {k} {{\n string key "{v}"\n }}\n' for k,v in tables.items()))
for name,url in [('github-qr','https://github.com/EagerBeaversl/django-girls-community-final'),('local-system-qr','http://localhost/django-girls/')]:qrcode.make(url).save(D/(name+'.png'))
pages=[
('01 / Organisation, problem and research',[
('Organisation and continuity','A Freetown-focused beginner coding community inspired by Django Girls. This academic prototype is not an official Django Girls service. It continues the supplied Assignment 1 PHP authentication project, organisation and original logo; it does not use the Django framework.'),
('Mission, vision and users','Help women and beginners learn, build and belong through practical resources and supportive peers. Intended users are learners, volunteer mentors and administrators. Services include workshops, learning resources, discussion, mentoring and project feedback.'),
('Problem and proposed solution','Design hypothesis: scattered event sign-up, resources and peer support can make the next learning step unclear. Centralise participation, personal progress, questions and guidance behind secure accounts. No interviews, survey statistics or measured engagement gains are claimed.'),
('Research and scope','Sources: supplied assignment brief and original source/report; official PHP and OWASP guidance for implementation rationale. Functional evidence comes from disposable local tests. Public hosting, formal usability studies and production certification are outside the verified scope.'),
('Assessment identity','Student ID: 905005223 · Course: BIT2101 · Module: DCOMP207 Advanced Web Programming. Submitted for Semester 05 assessment. Academic community prototype.')]),
('02 / UI/UX, mood board and navigation',[
('Approved spectral direction','Black/graphite surfaces, cyan #75D5FF, pink #D99BEE and amber #FFB879 highlights. Floating panels, quiet typography and spectral halos follow the approved visual reference. Auth pages use a decorative CSS 3D cube; no external animation service is needed.'),
('Typography, controls and accessibility','Website: Arial/Helvetica. Portfolio: Tahoma 12 pt throughout. Visible focus, explicit labels, escaped validation messages and password visibility controls. Cards stack on small screens. Themes persist locally; reduced-motion preferences remove decorative movement. No formal WCAG audit is claimed.'),
('Navigation and wireframes','Public Home/login ↔ Signup. Protected Overview, Profile, Events, Library, Community, Mentorship and Members. Administration is role-gated. Innovation navigation adds Discover, Daily challenge, Project lab, Calendar, Search, Milestones and Inbox. Existing wireframes record the base layout; final screenshots show its revised treatment.'),
('Meaningful practice','Read daily prompt → save text/code → manual admin review → revise or earn approval. Dated completions, posts, replies, submissions, projects and feedback earn activity; visits and reactions do not. Private submitted code is never executed or published in the feed.')]),
('03 / Actual interface evidence',[
('Local screenshots','Genuine captures of the revised PHP application. Any visible test/demo activity is fictional and belongs to the disposable test database, not the student’s Windows records. Full-resolution screenshots are included in docs/screenshots/.')]),
('04 / Architecture, ERD and workflows',[
('System structure','Browser HTML/CSS/JS → Apache/PHP → PDO prepared statements → MySQL/InnoDB. action.php handles core mutations; innovate.php handles additive features; report.php streams admin CSV. CLI tools install or upgrade. Ten core plus nine additive tables are shown below; SQL is authoritative.'),
('Keys and relationships','Lines connect one-to-many FK relationships. mentorships has two user roles (member and mentor). login_attempts and app_migrations are independent. activity_feed.source_id is polymorphic, not a database FK; application cleanup removes related topic/resource/project entries. Composite/unique keys prevent duplicate participation, dates, reactions and notifications.'),
('Critical workflows','Login: CSRF → throttle → active account/password verify → regenerate session. Event join: transaction/row lock → check past/full/duplicate → insert/commit. Challenge: per-user lock → one submission/date → manual review → escaped feedback. Project: owner/admin deletion → dependent feedback/feed cleanup.'),
('Security and limits','Prepared queries, hashing, escaping, POST/CSRF, role/ownership checks, session flags and validated random-named photos. No email recovery, email/push notifications, private chat or untrusted code execution. Production hosting still needs HTTPS, backups and operational hardening.')]),
('05 / Final product, verification and handover',[
('Eight innovations implemented','1 Streaks/badges; 2 reviewed daily challenges; 3 real activity feed/reactions; 4 projects/feedback; 5 calendar/countdowns; 6 global search; 7 persistent own inbox; 8 themes/reduced motion. Search excludes private email, submissions and inbox text. Event reminders are created on app opening within 48 hours, not by a background scheduler.'),
('Verification evidence','43 core HTTP + 42 innovation HTTP + 8 transactional helper checks passed. Browser: 17 routes × 3 widths × 2 themes = 102 combinations; no JavaScript errors, no page overflow, theme persistence and reduced motion passed. PHP syntax passed; additive upgrade ran twice. Linux PHP 8.4/MariaDB 11.8 tested. Windows/XAMPP and desktop PowerPoint playback require verification.'),
('Safe Windows handover','Existing installation: export DB and back up folder; copy updated source while retaining config.local.php and uploads; start MySQL; run upgrade-windows.bat. Do not reinstall or import base schema over populated data. Fresh install only: create empty django_girls DB and run install-windows.bat, choosing your own administrator.'),
('Submission limitations','GitHub is private: lecturer collaborator access is required. localhost QR works only on the XAMPP machine and is NOT a public live URL. The live-system requirement remains outstanding: host PHP/MySQL or obtain explicit lecturer approval. No guaranteed grade or adoption claim. The editable 18-slide deck includes notes, fades and Morph with fallback; verify motion in desktop PowerPoint.')])]
pdfmetrics.registerFont(TTFont('Tahoma',FONT));pdfmetrics.registerFont(TTFont('TahomaBold',BOLD));W,H=A3;M=43;CW=W-2*M
c=canvas.Canvas(str(D/'A3_Portfolio.pdf'),pagesize=A3)
style=ParagraphStyle('body',fontName='Tahoma',fontSize=12,leading=18,textColor=HexColor('#30313b'));bold=ParagraphStyle('bold',parent=style,fontName='TahomaBold')
def para(s,y,b=False):
 p=Paragraph(html.escape(s.replace('→',' > ').replace('↔',' / ')),bold if b else style);_,h=p.wrap(CW,H);p.drawOn(c,M,H-y-h);return y+h+9
def img(file,y,w,h,x=M):
 im=Image.open(file);r=min(w/im.width,h/im.height);iw=im.width*r;ih=im.height*r;c.drawImage(ImageReader(im),x+(w-iw)/2,H-y-ih,width=iw,height=ih)
doc=Document();sec=doc.sections[0];sec.page_width=Mm(297);sec.page_height=Mm(420);sec.top_margin=Mm(15);sec.bottom_margin=Mm(15);sec.left_margin=Mm(15);sec.right_margin=Mm(15)
for name in ('Normal','Title','Heading 1','Heading 2'):
 st=doc.styles[name];st.font.name='Tahoma';st.font.size=Pt(12);st.paragraph_format.space_after=Pt(7)
sec.footer.paragraphs[0].text='DCOMP207 Advanced Web Programming · Django Girls Freetown Community'
routes=['index','signup','dashboard','events','resources','community','challenges','hub','calendar']
for i,(title,blocks) in enumerate(pages,1):
 c.setFillColor(HexColor('#090a0d'));c.rect(0,H-110,W,110,fill=1,stroke=0);c.setFillColor(HexColor('#75d5ff'));c.rect(M,H-85,5,46,fill=1,stroke=0)
 c.setFont('TahomaBold',12);c.setFillColor(HexColor('#f4f4f8'));c.drawString(M+18,H-49,'DJANGO GIRLS / FREETOWN COMMUNITY');c.setFont('Tahoma',12);c.drawString(M+18,H-78,'DCOMP207 · FINAL PROJECT · 21 NOVEMBER 2026')
 y=133;y=para(title,y,True)
 if i>1:doc.add_page_break()
 doc.add_heading('DJANGO GIRLS / '+title,1)
 for heading,body in blocks:
  y=para(heading,y,True);y=para(body,y)+7
  p=doc.add_paragraph();p.add_run(heading).bold=True;doc.add_paragraph(body)
 if i==1:
  img(S/'index.png',y+10,CW,295);doc.add_picture(str(S/'index.png'),width=Inches(9.4),height=Inches(4.3))
 elif i==2:
  img(D/'wireframes.png',y+6,CW,240);doc.add_picture(str(D/'wireframes.png'),width=Inches(9.4),height=Inches(4.4))
 elif i==3:
  table=doc.add_table(rows=3,cols=3)
  for j,route in enumerate(routes):
   x=M+(j%3)*(CW/3);yy=y+10+(j//3)*260
   image=Image.open(S/(route+'.png'));image=image.crop((0,0,image.width,min(850,image.height)));p=D/(route+'-crop.jpg');image.save(p,quality=88)
   c.setFont('TahomaBold',12);c.drawString(x,H-yy,route.title());img(p,yy+13,CW/3-10,220,x)
   cell=table.cell(j//3,j%3);cell.paragraphs[0].add_run(route.title()).bold=True;cell.add_paragraph().add_run().add_picture(str(p),width=Inches(3.0),height=Inches(1.65))
 elif i==4:
  img(D/'erd.png',y+2,CW,465);doc.add_picture(str(D/'erd.png'),width=Inches(9.4),height=Inches(5.6))
 elif i==5:
  for j,(name,title,url) in enumerate([('github-qr','GITHUB / PRIVATE','https://github.com/EagerBeaversl/django-girls-community-final'),('local-system-qr','SYSTEM / LOCAL ONLY','http://localhost/django-girls/')]):
   yy=y+12+j*124;img(D/(name+'.png'),yy,108,108);p=Paragraph(title+'<br/>'+url,style);_,hh=p.wrap(CW-130,120);p.drawOn(c,M+130,H-yy-hh)
  t=doc.add_table(rows=1,cols=2)
  for j,name in enumerate(['github-qr','local-system-qr']):t.cell(0,j).paragraphs[0].add_run().add_picture(str(D/(name+'.png')),width=Inches(1.2))
  doc.add_paragraph('GitHub: https://github.com/EagerBeaversl/django-girls-community-final\nSystem (local only): http://localhost/django-girls/')
  doc.add_picture(str(D/'dashboard-crop.jpg'),width=Inches(9.4),height=Inches(3.7))
 c.setFont('Tahoma',12);c.setFillColor(HexColor('#626776'));c.drawString(M,35,'DCOMP207 Advanced Web Programming · Django Girls Community');c.drawRightString(W-M,35,f'Page {i} of 5');c.showPage()
c.save();doc.save(D/'A3_Portfolio.docx');print('Built revised 5-page A3 PDF and editable DOCX.')