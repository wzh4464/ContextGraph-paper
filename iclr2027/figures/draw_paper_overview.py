"""Vector figures for the paper: outcome overview, failure case, and method.

Layout follows the communication roles of ACE (ICLR 2026) Figures 1/2/4.
Artwork, labels, and data are specific to ContextGraph. No projected results.
"""
from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

OUT=Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
                     'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,
                     'axes.spines.right':False,'axes.linewidth':.6})
INK='#243849'; BLUE='#3971A6'; ORANGE='#B9742A'; GREEN='#3D7865'; GREY='#9AA3AC'
CG_RED='#C73527'

def save(fig,name):
    for ext in ('pdf','svg','png'):
        output = OUT/f'{name}.{ext}'
        fig.savefig(output,dpi=220,bbox_inches='tight',pad_inches=.025)
        if ext == 'svg':
            output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines())+'\n')
    plt.close(fig)

# Each panel has its own population and protocol. Source: existing main tables.
data={'verified500':{'labels':['None','FAISS Flat','ExpeL','Agent KB','ExpeRepair','ReasoningBank','ACE','Supermemory','CG'],
                    'resolved':[308,326,312,320,318,335,311,318,346],'n':500,
                    'model':'DeepSeek V4 Pro 0813','agent':'mini-SWE-agent',
                    'author_adaptations':['ExpeRepair','ACE']},
      'related99_crossmodel':{'models':['GPT-5.4','DeepSeek','Kimi','MiniMax'],
                   'control':[[21,98],[30,98],[18,97],[19,98]],
                   'memory':[[34,98],[34,97],[28,98],[27,98]]},
      'related99_retry':{'passes':[1,2,3],'control':[14,16,25],'memory':[21,25,27],'n':99}}
(OUT/'paper_overview_data.json').write_text(json.dumps(data,indent=2)+'\n')
fig,axs=plt.subplots(1,3,figsize=(7.6,2.25),gridspec_kw={'width_ratios':[1.65,1.05,1]})
fig.subplots_adjust(left=.06,right=.99,bottom=.36,top=.80,wspace=.38)
a=axs[0]; d=data['verified500']; vals=np.array(d['resolved'])/5
a.bar(range(len(vals)),vals,color=[GREY]+[BLUE]*(len(vals)-2)+[CG_RED],width=.67)
for i,v in enumerate(vals):a.text(i,v+2.0,f'{v:.1f}',ha='center',fontsize=6.5)
a.set(ylim=(0,82),xticks=range(len(vals)),xticklabels=d['labels'],ylabel='Resolved (%)')
a.tick_params(axis='x',labelsize=6.5,rotation=50,length=0)
plt.setp(a.get_xticklabels(),ha='right',rotation_mode='anchor')
a.set_title('(a) Verified500',fontsize=9,fontweight='bold',pad=16)
a.text(.5,1.04,'DeepSeek V4 Pro 0813 / mini-SWE-agent',transform=a.transAxes,ha='center',fontsize=6.5,color=INK)
a=axs[1]; d=data['related99_crossmodel']; x=np.arange(4)
c=[100*n/t for n,t in d['control']]; m=[100*n/t for n,t in d['memory']]
a.bar(x-.17,c,width=.33,color=GREY,label='No memory');a.bar(x+.17,m,width=.33,color=CG_RED,label='ContextGraph')
a.set(ylim=(0,42),xticks=x,xticklabels=d['models'],ylabel='Resolved / completed (%)')
a.tick_params(axis='x',labelsize=7,rotation=30,length=0)
a.set_title('(b) Related-Lite99',fontsize=9,fontweight='bold',pad=16)
a.text(.5,1.04,'Historical single attempt',transform=a.transAxes,ha='center',fontsize=7,color=INK)
a=axs[2]; d=data['related99_retry']
a.plot(d['passes'],d['control'],'o-',color=GREY,ms=4,lw=1.5,label='No memory')
a.plot(d['passes'],d['memory'],'s-',color=CG_RED,ms=4,lw=1.5,label='Memory')
for xx,yy in zip(d['passes'],d['memory']):a.text(xx,yy+1.0,str(yy),ha='center',fontsize=7,color=CG_RED)
for xx,yy in zip(d['passes'],d['control']):a.text(xx,yy-2.7,str(yy),ha='center',fontsize=7,color='#66727C')
a.axhline(25,color='#CBD3DB',ls=':',lw=.8,zorder=0)
a.set(xlim=(.8,3.2),ylim=(0,32),xticks=[1,2,3],xlabel='Cumulative passes',ylabel='Resolved tasks / 99')
a.set_title('(c) Earlier useful solutions',fontsize=9,fontweight='bold',pad=16)
a.text(.5,1.04,'Related-Lite99 / curated episodes',transform=a.transAxes,ha='center',fontsize=7,color=INK)
a.legend(frameon=False,fontsize=6.5,loc='lower right')
for a in axs:
    a.tick_params(axis='y',labelsize=7,width=.6,length=2)
    a.set_axisbelow(True);a.grid(axis='y',color='#E7ECF0',lw=.5)
save(fig,'paper_results_overview')
if '--overview-only' in sys.argv:
    raise SystemExit(0)

def canvas(h):
    f,a=plt.subplots(figsize=(7.6,h));f.subplots_adjust(left=0,right=1,bottom=0,top=1)
    a.set(xlim=(0,7.6),ylim=(0,h));a.axis('off');return f,a
def box(a,x,y,w,h,title,body,fc,ec=BLUE,title_size=10,body_size=9):
    a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.04',facecolor=fc,edgecolor=ec,lw=.8))
    a.text(x+.12,y+h-.16,title,ha='left',va='top',fontsize=title_size,fontweight='bold',color=ec)
    a.text(x+.12,y+h-.46,body,ha='left',va='top',fontsize=body_size,linespacing=1.4,color=INK)
def arrow(a,p,q,color=INK,style='-',rad=0):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=9,lw=.85,color=color,linestyle=style,connectionstyle=f'arc3,rad={rad}'))

fig,a=canvas(1.57)
box(a,.02,.27,2.15,1.18,'Current condition','Lazy User + nested query\nScalar lookup: passes','#EDF4FB',BLUE)
box(a,2.52,.27,2.15,1.18,'Historical condition','Named-tuple constructor\nStandalone range: passes','#FBF2E8',ORANGE)
box(a,5.03,.27,2.53,1.18,'Joint condition','Lazy User inside named-tuple range\nSame candidate: fails','#F8EEEE','#A64747')
a.text(2.34,.90,'+',ha='center',va='center',fontsize=20,color=INK)
arrow(a,(4.73,.9),(4.98,.9))
a.text(3.80,.10,'Observed on one Django12663 development repair; condition descriptions are schematic.',ha='center',va='center',fontsize=8,color='#5E6D79')
save(fig,'condition_interaction')

fig,a=canvas(2.94)
a.text(.03,2.80,'SOURCE CONSTRUCTION',fontsize=9,fontweight='bold',color=BLUE)
a.text(4.95,2.80,'Reusable evidence from historical versions',fontsize=8,color='#5E6D79')
xs=[.03,1.92,3.88,5.76]; widths=[1.58,1.65,1.57,1.79]
box(a,xs[0],1.71,widths[0],.93,'Historical repair','Issue, patch, code\nVersions V- and V+','#EDF4FB',BLUE,9,8.5)
box(a,xs[1],1.71,widths[1],.93,'Build witness','Requirement r + W(I, A, O)\nInput / action / observer','#EDF4FB',BLUE,9,8)
box(a,xs[2],1.71,widths[2],.93,'Source executions','Same input and observer\nBefore / after behavior','#EDF4FB',BLUE,9,8)
box(a,xs[3],1.71,widths[3],.93,'Frozen source graph','Requirements, witnesses\nInput / operation edges','#EDF4FB',BLUE,9,8.5)
for i in range(3):arrow(a,(xs[i]+widths[i]+.04,2.16),(xs[i+1]-.04,2.16),BLUE)
a.text(.03,1.36,'CURRENT REPAIR',fontsize=9,fontweight='bold',color=GREEN)
box(a,xs[0],.29,widths[0],.91,'Public task','Issue + inspected code\nCurrent operation','#F0F4F7',INK,9,8.5)
box(a,xs[1],.29,widths[1],.91,'Select and read','FAISS top-3 source IDs\nGraph joins full records','#EDF4FB',BLUE,9,8.5)
box(a,xs[2],.29,widths[2],.91,'Compose conditions','Bind source input roles\nto the current operation','#FBF2E8',ORANGE,9,8)
box(a,xs[3],.29,widths[3],.91,'Execute and refine','Execute supplied checks\nObserve, edit, repeat','#EDF5F0',GREEN,9,8.5)
for i in range(3):arrow(a,(xs[i]+widths[i]+.04,.75),(xs[i+1]-.04,.75))
a.plot([6.65,6.65,2.73,2.73],[1.68,1.47,1.47,1.24],color=BLUE,lw=.85)
arrow(a,(2.73,1.30),(2.73,1.21),BLUE)
a.text(4.13,1.51,'same source identities; complete witnesses and relations',fontsize=7.1,color=BLUE,ha='center',va='bottom')
arrow(a,(7.40,.56),(7.40,.88),GREEN,rad=.7)
a.text(3.80,.09,'Submitted patch → official verifier + common Joint / Preserve / Combined checks',ha='center',va='center',fontsize=8,color=INK)
save(fig,'memory_method_ace')
