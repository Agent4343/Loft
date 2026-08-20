import re
# Curated topic probes: several alternate phrasings each, so paraphrase does not cause false misses.
T = [
 ('2.1 RAM intent',                    ['common framework for identifying','intent of the ram']),
 ('2.1 Communicating RAM outcomes',    ['directly affected by identified risks','nature of the risk']),
 ('2.1 SLS / TLS role in RAM',         ['role of the sls','sls role in the ram','promote and encourage risk discovery']),
 ('2.1 ALARP',                         ['as low as','alarp']),
 ('2.1 Residual risk',                 ['residual risk']),
 ('2.1 Approving a risk assessment',   ['risk manager','aggregate risk of the asset','decision analysis']),
 ('2.1 Critical safeguard fails',      ['break-in work','safeguard owner informs']),
 ('2.1 CUI piping scenario',           ['retirement thickness','cui']),
 ('2.2 Training UBP / CVPE objective', ['training and competency ubp','cvpe']),
 ('2.2 Competency roles',              ['o&m technician']),
 ('2.2 Training tied to safeguard',    ['h2s response','process safety and you']),
 ('2.2 Validate/track competency',     ['webcat','personal placement checklist','ppc']),
 ('2.2 PSKV',                          ['pskv','operator knowledge verification']),
 ('2.3 IC procedure definition',       ['integrity critical procedure']),
 ('2.3 Revalidation timeframe',        ['36 months','revalidat']),
 ('2.3 Global IC examples',            ['pigging','escape capsule']),
 ('2.3 Deviation approvals',           ['deviation','work must stop']),
 ('2.3 Review/approval level',         ['technically verified','site validated','endorsed by']),
 ('2.3 Following procedures',          ['deviation requests','periodic observation']),
 ('2.3 Tools/triggers',                ['task analysis','difficulty, importance, frequency']),
 ('2.3 Procedures out of date',        ['out of date by six months','expedite review']),
 ('2.3 IC error at night',             ['interim directive']),
 ('2.4 FIMS criticality A-D',          ['criticality a','tmee330']),
 ('2.4 Sustained casing pressure',     ['sustained production casing','scssv','casing pressure']),
 ('2.4 Long Term Temporary Defeat',    ['long term temporary defeat','after 1 shift']),
 ('2.4 Gas detector TD scenario',      ['gas detector is faulty','faulty gas detector']),
 ('2.4 HLSD TD at day 6',              ['level control valve','high-level shutdown','hlsd']),
 ('2.5 Two elements alarm system',     ['readily address them without becoming overloaded','without becoming overloaded']),
 ('2.5 30 alarms/hour scenario',       ['30 alarms per hour','reactive']),
 ('2.6 WMS objective / PTW scope',     ['confined space entry','permit to work','work management system']),
 ('2.6 Life Saving Rules & Actions',   ['life saving']),
 ('2.6 PIC / AA / AO / PH roles',      ['person-in-charge','area authority','permit holder']),
 ('2.6 Non-permitted work list',       ['non-permitted work','oims 6-4']),
 ('2.6 SVI / ICC endorsement',         ['isolation control certificate','single valve isolation','icc']),
 ('2.6 LTI review & escalation',       ['6-month interval','quarterly field assessment']),
 ('2.6 DWCM purpose & attendees',      ['daily work coordination']),
 ('2.6 Temporary defeat purpose',      ['not solely time based','defeating and reinstatement']),
 ('2.6 Max permit validity',           ['no ability to extend','maximum permit validity','maximum validity']),
 ('2.6 SIMOPS',                        ['simops']),
 ('2.6 Breaking containment SVI',      ['flange class','witness the demonstration']),
 ('2.6 Control valve, no bleeder',     ['zero energy verification','bleeder','no zero energy']),
 ('2.7 MOC principles',                ['multi-functional','changes are evaluated']),
 ('2.7 When to consider MOC',          ['operating envelope','in kind']),
 ('2.7 Replacement in Kind',           ['replacement in kind','ansi ball valve']),
 ('2.7 Temporary change',              ['temporary change','authorized duration']),
 ('2.7 MOC requires PSSR',             ['pssr']),
 ('2.7 CS valve weekend scenario',     ['carbon steel','corrosion allowance']),
 ('2.7 Missing paperwork scenario',    ['paperwork','one-line drawing','p&id']),
 ('2.8 Notification vs investigation', ['notification is letting others know','irat']),
 ('2.8 Verify FLS/SLS understanding',  ['internal notification matrix','communication']),
 ('2.8 IRAT 100 scenario',             ['irat score','barriers remaining']),
 ('2.9 Env scenario offshore',         ['marine life','exclusion zone']),
 ('2.9 Env scenario onshore',          ['inland waterway','floating roof','30,000']),
 ('3.0 ER expectations by role',       ['emergency alerting','on-scene commander']),
 ('3.0 Tactical Response Plan',        ['tactical response plan']),
 ('3.0 TRP phase objectives',          ['initial discovery','proactive response']),
 ('3.0 PEAR / IMT scenario',           ['pear','holding statement','imt']),
]
files={'Loft':'rendered_lo.txt','Flip':'rendered_fc.txt','Study':'rendered_sg.txt'}
txt={k:open(v,encoding='utf8').read() for k,v in files.items()}
print('%-36s %-6s %-6s %-6s' % ('topic','Loft','Flip','Study'))
print('-'*60)
gaps=[]
for name,ps in T:
    row={k:any(p in txt[k] for p in ps) for k in files}
    mark=lambda b:'yes' if b else 'NO'
    line='%-36s %-6s %-6s %-6s' % (name,mark(row['Loft']),mark(row['Flip']),mark(row['Study']))
    if not all(row.values()): gaps.append((name,row)); line+='  <--'
    print(line)
print()
print('topics probed: %d | present in all three: %d | partial: %d' % (len(T),len(T)-len(gaps),len(gaps)))
