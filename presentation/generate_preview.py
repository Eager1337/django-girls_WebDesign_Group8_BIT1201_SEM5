from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

ROOT=Path(__file__).resolve().parent
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string('090A0D')
def shape(name,x,y,w,h,fill,line=None,kind=MSO_SHAPE.RECTANGLE):
 a=s.shapes.add_shape(kind,Inches(x),Inches(y),Inches(w),Inches(h));a.name=name
 if fill:a.fill.solid();a.fill.fore_color.rgb=RGBColor.from_string(fill)
 else:a.fill.background()
 if line:a.line.color.rgb=RGBColor.from_string(line);a.line.width=Pt(.8)
 else:a.line.fill.background()
 return a
def text(name,txt,x,y,w,h,size=18,color='F4F4F8',bold=False):
 a=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));a.name=name
 tf=a.text_frame;tf.word_wrap=True;tf.margin_left=tf.margin_right=0;tf.margin_top=tf.margin_bottom=0
 for i,line in enumerate(txt.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Arial';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
 return a
text('section','13 / MEANINGFUL PRACTICE',.65,.42,8,.3,11,'FF9A7E',True)
text('headline','Progress is earned.\nNot counted in clicks.',.65,1.05,8,1.6,40,bold=True)
text('context','A small daily build becomes a reviewed learning milestone.',.68,2.78,9,.4,18,'B0B2C2')
# A quiet spectral orbit built from native editable line shapes.
for i,(diam,col) in enumerate([(2.1,'203A47'),(1.76,'294354'),(1.42,'41334E'),(1.08,'593747'),(.74,'785543')]):
 shape('orbit-'+str(i),10.8+(2.1-diam)/2,.62+(2.1-diam)/2,diam,diam,None,col,MSO_SHAPE.OVAL)
text('orbit-plus','+',11.49,1.13,.75,.9,48,'E8C4FF')
for i,(num,title,body,col) in enumerate([
 ('01','Try a challenge','Save code or a written approach.\nSubmitted code is never executed.','75D5FF'),
 ('02','Receive a review','An administrator approves it\nor asks for improvements.','D99BEE'),
 ('03','Earn your momentum','Dated activity builds streaks.\nBadges reflect real milestones.','FFB879')]):
 x=.65+i*4.08
 shape('step-panel-'+num,x,3.52,3.87,2.36,'17181F','30313B',MSO_SHAPE.ROUNDED_RECTANGLE)
 text('step-number-'+num,num,x+.24,3.76,.7,.4,21,col)
 shape('step-line-'+num,x+.24,4.3,.45,.035,col)
 text('step-title-'+num,title,x+.24,4.56,3.4,.48,23,bold=True)
 text('step-copy-'+num,body,x+.24,5.13,3.38,.65,15,'B8BAC8')
shape('evidence-rule',.65,6.37,12.03,.015,'30313B')
text('evidence','VERIFIED LOCALLY   /   42 innovation checks + 8 helper checks passed',.65,6.63,10,.32,13,'A7ACBA')
text('page-number','13 / 18',11.64,6.63,1.03,.3,12,'7F8595')
text('student','Alusine G Dumbuya · 905005223 · DCOMP207',.65,7.04,10,.2,10,'777D8D')
# Standard fade is the interoperable preview transition. Morph-compatible object names are stable.
transition=OxmlElement('p:transition');transition.set('spd','med');transition.append(OxmlElement('p:fade'))
s._element.insert(list(s._element).index(s._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}clrMapOvr'))+1,transition)
s.notes_slide.notes_text_frame.text=('Representative slide 13 of the planned 18-slide defence. Explain the daily challenge workflow: authenticated member stores text or code; no execution engine exists; administrator manually reviews; milestones use dated meaningful actions. The activity-day key prevents multiple credits on one date. Current streak accepts activity yesterday but breaks at a gap. Evidence: 42 HTTP feature checks and 8 CLI helper checks on a disposable local DB. Baseline also passes 43 checks. Do not claim improved engagement, guaranteed grades, public hosting or desktop PowerPoint playback verification. The final deck will add restrained entrances and Morph-compatible transitions after preview approval.')
prs.save(ROOT/'preview.pptx')
print(ROOT/'preview.pptx')