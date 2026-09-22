"""Preserve the three-panel visual structure without inventing final results."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.6})
fig,axs=plt.subplots(1,3,figsize=(7.6,2.0))
fig.subplots_adjust(left=.03,right=.99,bottom=.12,top=.81,wspace=.27)
items=[('(a) Repair success','E07 | four matched benchmarks','Official resolved / planned','Verified150 · Related99\nLoLBench100 · DeepSWE113'),('(b) Measured omissions','E15 | independent held-out tasks','Joint · Preserve · Combined','Current-contract checks\nsealed independently of repairs'),('(c) Development mechanisms','E03 | 24 development targets','I−H separate vs. joint checks','C−B relations · C−G composer\nF−C supplied observations')]
for a,(title,sub,metric,desc) in zip(axs,items):
    a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
    a.set_title(title,fontsize=9,fontweight='bold',pad=16)
    a.text(.5,1.04,sub,transform=a.transAxes,ha='center',fontsize=7,color='#243849')
    a.axhline(.93,color='#9AA3AC',lw=.6)
    a.text(.5,.71,'TBD',ha='center',va='center',fontsize=16,fontweight='bold',color='#B51F2D')
    a.text(.5,.47,metric,ha='center',va='center',fontsize=7.2,color='#243849')
    a.text(.5,.23,desc,ha='center',va='center',fontsize=7,color='#647280',linespacing=1.5)
fig.text(.5,.015,'CG-Fixed-v1 specification | results await release freeze and evaluation',ha='center',fontsize=7,color='#B51F2D')
for ext in ['pdf','svg','png']:
    fig.savefig(P/f'paper_final_overview.{ext}',dpi=220,bbox_inches='tight',pad_inches=.025)
plt.close(fig)
(P/'paper_final_overview_data.json').write_text(json.dumps({'status':'pending_no_results','variant':'CG-Fixed-v1','official_resolution_E07':None,'independent_completeness_E15':None,'attribution_E03':None,'historical_figure_preserved':'paper_results_overview.pdf'},indent=2)+'\n')
