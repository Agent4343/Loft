#!/usr/bin/env python3
"""Checks that every Assessor Guide topic is still present in the study aid.

Run after any content edit:   python3 tools-coverage-check.py
Exits non-zero if a topic goes missing, so it can be wired into a check.

Each topic carries several alternate phrasings because the aid paraphrases the
source; matching on a single exact phrase produces false misses.
"""
import html
import re
import sys

TARGET = 'LOFT-Process-Safety.html'

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
 # Three CAS-route probes were dropped here - the IC procedure definition, the
 # globally recommended IC examples, and the Interim Directive scenario. Those
 # questions were removed once Hebron/Hibernia completed CVPE; none is assessable.
 ('2.3 Revalidation timeframe',        ['36 months','revalidat']),
 ('2.3 Deviation approvals',           ['deviation','work must stop']),
 ('2.3 Review/approval level',         ['technically verified','site validated','endorsed by']),
 ('2.3 Following procedures',          ['deviation requests','periodic observation']),
 ('2.3 Tools/triggers',                ['task analysis','difficulty, importance, frequency']),
 ('2.3 Procedures out of date',        ['out of date by six months','expedite review']),
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


def text_of(path):
    raw = open(path, encoding='utf8').read()
    raw = re.sub(r'<(script|style)\b.*?</\1>', ' ', raw, flags=re.S | re.I)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(raw)).lower()


def main():
    try:
        body = text_of(TARGET)
    except FileNotFoundError:
        print('cannot find %s' % TARGET)
        return 2
    missing = [name for name, probes in T if not any(p in body for p in probes)]
    for name, probes in T:
        ok = any(p in body for p in probes)
        print('%-42s %s' % (name, 'ok' if ok else 'MISSING'))
    print()
    print('%d topics checked, %d present, %d missing' % (len(T), len(T) - len(missing), len(missing)))
    if missing:
        print('\nMissing:')
        for m in missing:
            print('  - ' + m)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
