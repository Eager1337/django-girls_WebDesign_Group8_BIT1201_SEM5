"""Native, editable 18-slide defence. Approved spectral preview is the theme source."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from lxml import etree
import generate_preview as theme

ROOT=Path(__file__).resolve().parent
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
COLORS=['75D5FF','D99BEE','FFB879','9EE5CD']
shape=theme.shape;text=theme.text
def slide(label,title,subtitle,notes):
 s=prs.slides.add_slide(prs.slide_layouts[6]);theme.s=s
 s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string('090A0D')
 text('section',f'{len(prs.slides):02d} / {label}',.65,.42,10,.3,11,'FF9A7E',True)
 text('headline',title,.65,1.0,11.9,1.28,36,bold=True)
 text('context',subtitle,.65,2.35,11.8,.7,18,'B0B2C2')
 shape('footer-rule',.65,6.7,12.03,.015,'30313B')
 text('student','Alusine G Dumbuya · 905005223 · DCOMP207',.65,7.04,10,.2,10,'777D8D')
 text('page-number',f'{len(prs.slides):02d} / 18',11.64,7.03,1.03,.3,12,'7F8595')
 s.notes_slide.notes_text_frame.text=notes
 return s
def cards(items,y=3.38,h=2.85):
 n=len(items);gap=.2;w=(12.03-gap*(n-1))/n
 for i,(title,body) in enumerate(items):
  x=.65+i*(w+gap)
  shape('panel-'+str(i),x,y,w,h,'17181F','30313B',MSO_SHAPE.ROUNDED_RECTANGLE)
  text('number-'+str(i),f'{i+1:02d}',x+.23,y+.2,.7,.4,19,COLORS[i%4])
  text('card-title-'+str(i),title,x+.23,y+.84,w-.46,.7,22,bold=True)
  text('card-body-'+str(i),body,x+.23,y+1.62,w-.46,h-1.7,16,'B8BAC8')
def flow(items):
 n=len(items);w=2.75;gap=.32
 for i,(title,body) in enumerate(items):
  x=.65+i*(w+gap)
  shape('flow-'+str(i),x,3.65,w,2.15,'17181F','30313B',MSO_SHAPE.ROUNDED_RECTANGLE)
  text('flow-title-'+str(i),title,x+.2,3.93,w-.4,.55,22,COLORS[i%4],True)
  text('flow-body-'+str(i),body,x+.2,4.72,w-.4,.8,16,'B8BAC8')
  if i<n-1:text('arrow-'+str(i),'›',x+w+.03,4.32,.25,.5,25,'7F8595')
def rows(items):
 for i,(a,b) in enumerate(items):
  y=3.18+i*.64
  text('row-label-'+str(i),a,.7,y,3.65,.45,18,COLORS[i%4],True)
  text('row-body-'+str(i),b,4.55,y,7.9,.5,17,'B8BAC8')
def image(route,x=6.5,y=3.15,w=6.15,h=3.22):
 path=ROOT.parent/'docs'/'screenshots'/f'{route}.png'
 if not path.exists():path=Path('/home/user/innovation-preview')/f'{route}-1440-dark.png'
 from PIL import Image
 im=Image.open(path);cropped=im.crop((0,0,im.width,min(im.height,850)))
 asset=ROOT/'assets'/f'{route}.png';asset.parent.mkdir(exist_ok=True);cropped.save(asset)
 a=theme.s.shapes.add_picture(str(asset),Inches(x),Inches(y),width=Inches(w),height=Inches(h));a.name='Local screenshot — '+route

slide('PROJECT DEFENCE','Learn. Build. Belong.','Django Girls · Freetown community management platform',
 'Introduce the student, module and academic project. This is a PHP/MySQL continuation of Assignment 1, not a Django framework app and not an official Django Girls service. The final brief says Semester 05; the earlier report says Sem4. Confirm the discrepancy with the lecturer.')
text('hero-statement','A connected place\nfor curious beginners.',.65,3.35,7.3,1.75,38,bold=True)
for i,(d,c) in enumerate([(2.8,'203A47'),(2.3,'294354'),(1.8,'41334E'),(1.3,'593747'),(.8,'785543')]):shape('!!orbit-'+str(i),9.55+(2.8-d)/2,3.25+(2.8-d)/2,d,d,None,c,MSO_SHAPE.OVAL)
text('hero-plus','+',10.51,4.02,.8,.8,46,'E8C4FF')

slide('CONTINUITY','The same community.\nA more capable platform.','The supplied authentication project becomes a complete community workspace.',
 'Original Assignment 1 source and report are the continuity evidence. The organisation and original logo remain. The CLI migration can preserve valid password hashes from the original JSON store. Existing MySQL installations must use the additive upgrade, not reinstall. No survey results or organisational endorsement are claimed.')
cards([('Starting point','PHP sign-in and signup\nOriginal organisation and logo'),('Final product','Profiles, opportunities,\nlearning and peer support'),('Preserved identity','Freetown focus\nBeginner-friendly language')])

slide('PROBLEM & USERS','Less fragmentation.\nMore clear next steps.','Problem hypothesis derived from the brief — not invented interview data.',
 'Fragmentation is a design hypothesis: beginners may struggle when event registration, resources and support sit in separate channels. No interviews or engagement measurements were conducted. Explain how the three roles organise the solution, then describe the need for future user testing.')
cards([('Learners','Find workshops, track learning\nand ask useful questions.'),('Volunteer mentors','Receive requests and guide\nbeginners through responses.'),('Organisers','Manage members, content,\nparticipation and reports.')])

slide('REQUIREMENT COVERAGE','The core brief is mapped\nto working modules.','Server-rendered PHP pages backed by real relational data.',
 'Demonstrate the requirement mapping with a real account. Dashboard statistics come from the database. User management protects the last active administrator. CSV is administrator-only. A publicly reachable live system URL remains outstanding; localhost does not satisfy that requirement automatically.')
rows([('Authentication & profile','Hashed passwords, sessions, photo and personal details'),('Personal dashboard','Participation, learning progress and role-specific links'),('Community services','Events, resources, discussions and mentorship'),('Administration','User roles, content CRUD, moderation and attendance'),('Reporting','Database statistics, audit trail and CSV export')])

slide('ROLES & JOURNEYS','One platform.\nClear boundaries.','Member, mentor and administrator permissions are enforced on the server.',
 'All private screens require a live active account. Mentor responses are limited to the assigned mentor and pending requests. Administrative routes and writes reject members even if a URL is typed manually. Self-demotion and removal of the last administrator are blocked. Explain a member event journey and administrator attendance journey.')
cards([('Member','Join events, learn, publish,\nrequest guidance and respond.'),('Mentor','Member tools plus assigned\nmentorship response controls.'),('Administrator','Manage content and users,\nreview challenges and export.')])

slide('DESIGN SYSTEM','Quiet structure.\nSpectral energy.','Black surfaces, cyan / pink / amber accents and restrained motion.',
 'The user-approved visual reference informed the spectral halos, floating panels and CSS three-dimensional auth sculpture. The website uses Arial, while the A3 portfolio follows the brief’s Tahoma 12 requirement. Motion is decorative and reduced-motion-aware. Keyboard focus, explicit labels and theme controls improve access; no formal WCAG certification is claimed.')
for i,(name,c) in enumerate([('CHARCOAL','17181F'),('CYAN','75D5FF'),('PINK','D99BEE'),('AMBER','FFB879')]):
 shape('swatch-'+name,.65+i*3.06,3.35,2.82,.77,c);text('swatch-label-'+name,name,.65+i*3.06,4.34,2.8,.4,15,'B8BAC8')
text('design-detail','Responsive at 390 / 768 / 1440 px   ·   Light and dark themes\nKeyboard labels and focus   ·   Reduced-motion-aware transitions',.65,5.23,11.8,1.0,20)

slide('ARCHITECTURE','A deliberately simple\nserver-rendered system.','No CMS, paid API or submitted-code execution service is required.',
 'Browser requests go to Apache/PHP. Config and helpers enforce sessions, escaping and PDO prepared statements. action.php handles original mutations; innovate.php handles the additive feature actions; report.php streams administrator CSV. CLI tools install or upgrade. MySQL InnoDB transactions protect capacity. PHP 8.4 and MariaDB 11.8 were tested locally; CI targets PHP 8.2/MySQL 8.')
flow([('Browser','HTML / CSS / JS\nResponsive presentation'),('PHP','Sessions / roles\nCSRF / validation'),('PDO','Prepared statements\nTransactions / locks'),('MySQL','InnoDB tables\nKeys and constraints')])

slide('RELATIONAL MODEL','Ten core tables.\nNine additive tables.','An idempotent migration expands the existing database without replacing it.',
 'Core: users, events, registrations, resources, progress, topics, replies, mentorships, audit_log, login_attempts. Additive: activity_days, challenges, challenge_submissions, projects, project_feedback, activity_feed, feed_reactions, notifications, app_migrations. Unique keys guard user/day submissions, reactions, notification dedupe and learning days. Full foreign-key ERD is in the portfolio documentation; these are domain groups, not a complete ERD.')
cards([('Core domains','Identity / participation\nLearning / peer support'),('Innovation domains','Practice / projects / feed\nReactions / notifications'),('Integrity','Foreign keys and unique keys\nVersioned additive migration')])

slide('AUTHENTICATION','Protection belongs\non every write path.','Security controls are built into routes and shared helpers.',
 'Explain password_hash and password_verify, session regeneration, CSRF for POST, output escaping and parameterised queries. Photos are MIME/dimension/size checked and given random filenames. Login attempts are throttled. Uploaded files are restricted. These checks are not an external penetration test. HTTPS, operational backups, recovery and hosting hardening remain production work.')
rows([('Identity','Password hashing, session regeneration and suspension checks'),('Writes','POST + CSRF + role and ownership checks'),('Rendering','Escape user text; no submitted-code execution'),('Uploads','Validated JPG / PNG / WebP, random filenames, limits'),('Data access','Prepared queries and transaction-protected mutations')])

slide('EVENTS & PARTICIPATION','A place is reserved.\nCapacity stays protected.','Real registration, cancellation, attendance and calendar views.',
 'When joining, the server locks the event row, checks time, duplicate membership and capacity, then inserts and commits. Administrators record attendance. The 43 core checks include duplicate registration, full capacity, cancellation and attendance. Countdowns are display enhancements, not the source of capacity truth.')
flow([('Discover','Browse a workshop\nReview time and location'),('Validate','Lock event row\nCheck capacity and duplicate'),('Participate','Save registration\nAllow cancellation'),('Confirm','Administrator records\nAttendance evidence')])

slide('CORE COMMUNITY','Learning is more useful\nwhen support is nearby.','Resources, discussions and mentorship work together.',
 'Resource completion is reversible and backed by a unique user/resource record. Discussion bodies and replies are escaped. Mentorship requests are directed to active mentors and can be accepted or declined by the assigned mentor. There is no private chat or email service. Public activity only exposes appropriate milestones; private challenge code stays private.')
cards([('Learning library','Search resources and record\ncompleted learning.'),('Peer discussion','Start topics, reply and\nreceive in-app feedback alerts.'),('Mentorship','Request support and track\nassigned-mentor responses.')])

slide('EIGHT INNOVATIONS','From administration\nto an active learning space.','Eight additions — implemented locally, not placeholders.',
 'List all eight and connect each to a user need. They do not prove engagement gains. Streaks depend on meaningful activity, challenges use manual review, feed contains real entries, projects accept links/text rather than executable uploads, calendar uses event data, search excludes private data, inbox is in-app only, and theme preferences persist locally.')
for i,t in enumerate(['Streaks & milestones','Daily coding challenges','Community feed & cheers','Project showcase & feedback','Calendar & countdowns','Global search','Persistent in-app inbox','Light / dark + reduced motion']):
 x=.65+(i%2)*6.12;y=3.17+(i//2)*.75
 text('innovation-'+str(i),f'{i+1:02d}  {t}',x,y,5.8,.5,21,COLORS[i%4])

# Preserve the approved representative layout, rebuilt through its own source.
import copy
source=Presentation(ROOT/'preview.pptx').slides[0]
s=prs.slides.add_slide(prs.slide_layouts[6]);theme.s=s;s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string('090A0D')
for a in source.shapes:s.shapes._spTree.insert_element_before(copy.deepcopy(a.element),'p:extLst')
s.notes_slide.notes_text_frame.text=source.notes_slide.notes_text_frame.text

slide('FEED & PROJECTS','Make your work visible.\nKeep feedback useful.','Real activity, explicit reactions and moderated project conversations.',
 'A project stores description and an optional validated HTTP(S) link. User text is escaped. Owners and administrators can delete; feedback deletion is administrator-only. Reaction keys prevent duplicates. Project deletion removes its feed and cascades feedback. The displayed screenshot is from a disposable local test installation, not live community adoption.')
text('feed-explanation','Publish a small build.\nInvite constructive feedback.\nCelebrate a real milestone.',.65,3.55,5.5,2.0,25)
image('hub');text('shot-caption','Actual local screenshot · fictional test activity',6.5,6.39,6.1,.25,10,'7F8595')

slide('DISCOVERY & PREFERENCES','Find what matters.\nReturn on your terms.','Calendar, global search, persistent inbox and accessible themes.',
 'Calendar reads actual workshops and current member registrations. Event reminders appear when the app is opened for a registered event within 48 hours, deduplicated per event; no background scheduler or email/push exists. Search covers members/events/resources/topics/projects without private email, submissions or inbox content. Theme storage failures do not break forms. Reduced motion removes decorative animations.')
rows([('Calendar','Month navigation, registered badges and live countdowns'),('Search','Five public community domains; private content excluded'),('Inbox','Own persistent notifications and mark-read controls'),('Preferences','Local theme persistence and reduced-motion support')])

slide('VERIFICATION','Evidence before\ncompletion claims.','Automated checks used a disposable local installation.',
 '43 baseline HTTP, 42 innovation HTTP and 8 transactional helper checks passed. Browser matrix: 17 routes × 3 widths × 2 themes = 102 checks. It checked overflow, JavaScript errors, theme persistence and reduced motion. Upgrade ran twice successfully. These are not 102 separate human usability studies or a formal accessibility/security audit. Actual Windows execution and desktop PowerPoint motion playback remain unverified.')
for i,(num,label) in enumerate([('43','Core HTTP checks'),('42','Innovation HTTP checks'),('8','Helper / streak checks'),('102','Browser combinations')]):
 x=.65+i*3.06;text('stat-'+str(i),num,x,3.5,2.82,1.0,57,COLORS[i%4],True);text('stat-label-'+str(i),label,x,4.75,2.82,.8,17,'B8BAC8')
text('qa-caveat','PHP syntax passed · No browser JS errors · Idempotent upgrade\nWindows execution and desktop PowerPoint playback still need verification.',.65,5.76,12,.72,16,'B8BAC8')

slide('HANDOVER','Upgrade safely.\nDo not reinstall your data.','Windows/XAMPP source package and private GitHub delivery.',
 'Back up the populated database and existing folder. Copy the updated source but retain config.local.php and uploads. Run upgrade-windows.bat with MySQL running; it invokes tools/upgrade.php and adds tables/seeds only. Fresh users use the fresh installer. GitHub is private and requires lecturer access. localhost works only on the machine running XAMPP. A public live URL is outstanding and needs hosting or explicit lecturer acceptance.')
cards([('Existing installation','Back up → preserve config\nand uploads → additive upgrade'),('Source repository','Private GitHub\nLecturer collaborator required'),('Deployment status','Localhost only\nPublic live URL outstanding')])

slide('EVALUATION','A complete local prototype.\nAn honest next step.','Core requirements and eight innovations are implemented; deployment is not overstated.',
 'Conclude with implemented scope, evidence and limitations. No guaranteed grade, ranking or engagement impact. Next priorities: real user feedback, Windows walkthrough, production security/backups, public PHP hosting if required, account recovery, and desktop PowerPoint transition/animation validation. Mention semester discrepancy and academic assistance disclosure. Invite questions about capacity locks, schema integrity, challenge safety and migration preservation.')
cards([('Demonstrated','Core + eight innovations\nLocal regression evidence'),('Still to validate','Windows walkthrough\nHosted URL / lecturer approval'),('Defence discussion','Why PHP? Why transactions?\nHow is user data preserved?')])

def motion(s,index):
 # Morph choice with standard fade fallback for older PowerPoint/LibreOffice.
 MC='http://schemas.openxmlformats.org/markup-compatibility/2006';P='http://schemas.openxmlformats.org/presentationml/2006/main';M='http://schemas.microsoft.com/office/powerpoint/2015/09/main'
 if index in (2,13):
  alt=etree.Element('{'+MC+'}AlternateContent',nsmap={'mc':MC,'p':P,'p159':M})
  choice=etree.SubElement(alt,'{'+MC+'}Choice',Requires='p159');tr=etree.SubElement(choice,'{'+P+'}transition',spd='med');etree.SubElement(tr,'{'+M+'}morph',option='byObject')
  fallback=etree.SubElement(alt,'{'+MC+'}Fallback');tr=etree.SubElement(fallback,'{'+P+'}transition',spd='med');etree.SubElement(tr,'{'+P+'}fade');s._element.append(alt)
 else:
  tr=OxmlElement('p:transition');tr.set('spd','med');tr.append(OxmlElement('p:fade'));s._element.append(tr)
 # One click fades the main headline in; avoid scattered animation.
 headline=next(a for a in s.shapes if a.name=='headline')
 timing=OxmlElement('p:timing');timing.append(etree.fromstring(f'''<p:tnLst xmlns:p="{P}"><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="4" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="5" dur="500"/><p:tgtEl><p:spTgt spid="{headline.shape_id}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>'''));s._element.append(timing)
for i,s in enumerate(prs.slides,1):motion(s,i)
assert len(prs.slides)==18
prs.save(ROOT/'presentation.pptx');print(ROOT/'presentation.pptx')