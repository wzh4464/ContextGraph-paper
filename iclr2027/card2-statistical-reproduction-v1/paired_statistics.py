"""Paired exploratory statistics only after every frozen task's evidence passes."""
import argparse
import hashlib
import json
from math import comb
from pathlib import Path

import numpy as np


def summarize(audit,left,right):
    ids=audit['target_ids']
    if not ids or len(ids)!=len(set(ids)):raise ValueError('Invalid fixed denominator')
    arms=[audit['arms'][name]['records'] for name in (left,right)]
    for rows in arms:
        if set(rows)!=set(ids):raise ValueError('Never shrink the frozen denominator to an intersection')
        if any(r.get('errors') or r.get('verification_valid') is not True or
               not isinstance(r.get('resolved'),bool) for r in rows.values()):
            raise ValueError('Unvalidated or missing verdict: no complete-case effect estimate')
    counts={'both':0,'left_only':0,'right_only':0,'neither':0}
    for iid in ids:
        a,b=[r[iid]['resolved'] for r in arms]
        counts['both' if a and b else 'left_only' if a else 'right_only' if b else 'neither']+=1
    n=len(ids);discordant=counts['left_only']+counts['right_only']
    p=min(1.,2*sum(comb(discordant,k) for k in range(min(counts['left_only'],counts['right_only'])+1))/2**discordant)
    # Multinomial resampling is exactly paired task bootstrap for binary outcomes.
    samples=np.random.default_rng(42).multinomial(n,np.array(list(counts.values()))/n,size=200000)
    interval=np.quantile((samples[:,2]-samples[:,1])/n,[.025,.975]).tolist()
    return {'benchmark':audit['benchmark'],'manifest_sha256':audit['manifest_sha256'],
        'left':left,'right':right,'n':n,'pair_counts':counts,
        'resolved':{left:counts['both']+counts['left_only'],right:counts['both']+counts['right_only']},
        'right_minus_left':(counts['right_only']-counts['left_only'])/n,
        'mcnemar_exact_two_sided_p':p,'paired_bootstrap_percentile_95ci':interval,
        'bootstrap_replicates':200000,'bootstrap_seed':42,
        'interpretation_scope':'Exploratory frozen-manifest verdict comparison. Delivery, source leakage and adaptive campaign selection require separate audits.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('audit',type=Path)
    p.add_argument('--left',required=True);p.add_argument('--right',required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();result=summarize(json.loads(a.audit.read_text()),a.left,a.right)
    result['audit_sha256']=hashlib.sha256(a.audit.read_bytes()).hexdigest()
    result['analysis_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with a.out.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
