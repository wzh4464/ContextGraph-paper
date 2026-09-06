"""Classifier functions copied verbatim from the source-bound original audits."""
import hashlib
import json
import re

def inspect_history(history,expected_card=None):
    queries={};responses=[]
    for h in history:
        if h.get('role')=='assistant':
            for c in h.get('tool_calls') or []:
                if c.get('function',{}).get('name')=='query_memory':queries[c.get('id')]=c
        elif h.get('role')=='tool':
            ids=h.get('tool_call_ids') or ([h['tool_call_id']] if h.get('tool_call_id') else [])
            matching=[i for i in ids if i in queries]
            if not matching:continue
            text=h.get('content') or ''
            if not isinstance(text,str):text=json.dumps(text)
            abstained='MEMORY_ABSTAINED' in text[:1000]
            sources=re.findall(r'^\[GOLD PATCH src=([^\]]+)\]',text,re.MULTILINE)
            served=bool(sources and '\ndiff --git ' in text and not abstained)
            phases=[]
            for identifier in matching:
                args=queries[identifier].get('function',{}).get('arguments',{})
                try:args=json.loads(args) if isinstance(args,str) else args
                except ValueError:args={}
                phases.append(args.get('phase') if isinstance(args,dict) else None)
            responses.append({'tool_call_ids':matching,'response_sha256':hashlib.sha256(text.encode()).hexdigest(),
                'served':served,'source_ids':sources,'abstained':abstained,
                'query_phases':phases,'served_pre_plan':served and 'pre_plan' in phases,
                'phase_refusal':abstained and 'phase' in text[:1000].lower(),
                'exact_expected_card':bool(expected_card and expected_card in text),
                'card_headers':re.findall(r'^\[REPO PLAYBOOK [—-] ([^ ·\]]+)',text,re.MULTILINE),
                'chars':len(text),'unclassified_response':not served and not abstained})
    responded={i for r in responses for i in r['tool_call_ids']}
    return {'queries':len(queries),'responses':responses,'missing_response_ids':sorted(set(queries)-responded),
        'served':any(r['served'] for r in responses),
        'served_pre_plan':any(r['served_pre_plan'] for r in responses),
        'exact_card_served':any(r['served'] and r['exact_expected_card'] for r in responses),
        'phase_refusals':sum(r['phase_refusal'] for r in responses)}

def inspect(history):
    calls=[];shell=[];prompts=[];first_user_seen=False
    for index,h in enumerate(history):
        if h.get('role')=='system' or (h.get('role')=='user' and not first_user_seen):
            prompts.append(h.get('content') or '')
            if h.get('role')=='user':first_user_seen=True
        if h.get('role')=='assistant':
            for call in h.get('tool_calls') or []:
                if call.get('function',{}).get('name')=='query_memory':calls.append(call.get('id'))
            action=h.get('action') or ''
            if isinstance(action,str) and re.search(r'(?<![\w/])query_memory(?:\s|$)',action):shell.append(index)
    text='\n'.join(x if isinstance(x,str) else json.dumps(x) for x in prompts)
    markers=[m for m in ('<reference_memory>','[GOLD PATCH src=','[REPO PLAYBOOK','[LIKELY FILES') if m in text]
    return {'query_memory_function_calls':calls,'query_memory_shell_action_indices':shell,
        'initial_prompt_marker_hits':markers,'first_user_present':first_user_seen,
        'no_direct_memory_observed':first_user_seen and not calls and not shell and not markers}
