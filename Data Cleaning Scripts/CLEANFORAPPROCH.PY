#!/usr/bin/env python3
"""Builds the SkillLens data files from the 4 cleaned hackathon datasets.
Put this file next to the cleaned files and run:  python build_skilllens_data.py
Reads  (first match wins; raw files work too):
  A  cleaned_ds_jobs.csv          | DataScience Jobs.csv
  B  cleaned_analytics_jobs.csv   | Analytics Jobs.csv
  C  cleaned_jds_skills.csv       | JDS Skill Traits.xlsx
  D  cleaned_sds_personality.csv  | SDS Personality Traits.xlsx
Writes skill_connections_rich.csv (skill map + salaries) and paradox.json (promotion evidence)."""
import json, os, re, sys
from collections import Counter
from itertools import combinations
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
TOP_SKILLS, MIN_PAIR = 150, 5

HARD = {'python','r','java','sql','scala','javascript','c++','c#','php','machine learning','deep learning','nlp','computer vision','ai','artificial intelligence','tensorflow','pytorch','keras','scikit-learn','pandas','numpy','hadoop','spark','pyspark','hive','aws','azure','gcp','cloud','docker','kubernetes','git','mysql','postgresql','mongodb','tableau','power bi','excel','etl','data engineering','linux','api','rest api','statistics','mathematics','regression','classification','clustering','sas','data mining','data modeling','big data','data warehousing','data analysis','forecasting','predictive modeling','analytics','visualization','dashboards','reporting'}
SOFT = {'communication','presentation','storytelling','leadership','management','problem solving','critical thinking','collaboration','teamwork','time management','stakeholder management','decision making','strategic thinking','interpersonal','documentation','attention to detail','customer service','analytical'}
SYN = {'py':'python','python3':'python','machine-learning':'machine learning','ml':'machine learning','powerbi':'power bi','power-bi':'power bi','postgres':'postgresql','sklearn':'scikit-learn','artificial intelligence':'ai','communicative':'communication','verbal':'communication','problem-solving':'problem solving','team player':'teamwork','teamwork':'teamwork','statistical':'statistics','statistical analysis':'statistics','math':'mathematics','maths':'mathematics','data visualization':'visualization','data visualisation':'visualization','dashboard':'dashboards','story telling':'storytelling','data storytelling':'storytelling'}
# which promotion feature (dataset C) each skill belongs to
CAT = {'story': {'storytelling','communication','presentation','visualization','dashboards','tableau','power bi','reporting','stakeholder management'},
       'stats': {'statistics','mathematics','regression','classification','clustering','forecasting','predictive modeling'},
       'code': {'python','r','java','sql','scala','javascript','c++','c#','php','git','linux','api'},
       'ai': {'machine learning','deep learning','nlp','computer vision','ai','tensorflow','pytorch','keras','scikit-learn'},
       'bigdata': {'hadoop','spark','pyspark','hive','aws','azure','gcp','cloud','big data','etl','data engineering','data warehousing'}}
LABEL = {'story':'Storytelling and dashboards','stats':'Maths and stats','code':'Coding','ai':'AI and ML','bigdata':'Big data'}

ACR = {'sql','aws','gcp','nlp','ai','etl','api','sas','php','r','ml'}
SPECIAL = {'power bi':'Power BI','mysql':'MySQL','postgresql':'PostgreSQL','javascript':'JavaScript','pytorch':'PyTorch','tensorflow':'TensorFlow','pyspark':'PySpark','scikit-learn':'Scikit-learn','mongodb':'MongoDB','nlp':'NLP','ai':'AI','r':'R','c++':'C++','c#':'C#'}
def nice(s): return SPECIAL.get(s) or (s.upper() if s in ACR else s.title())

def find(*names):
    for n in names:
        p = os.path.join(HERE, n)
        if os.path.exists(p):
            return pd.read_excel(p) if n.endswith('xlsx') else pd.read_csv(p)
    sys.exit('Missing dataset. Looked for: ' + ' | '.join(names))

def lakhs(v):
    """'6-10 Lakhs', '12to15', 7.5 -> lakhs as float (midpoint of ranges); unknown -> nan"""
    if pd.isna(v): return np.nan
    if isinstance(v, (int, float)): return float(v) if v > 0 else np.nan
    n = re.findall(r'\d+\.?\d*', str(v))
    if not n or re.search(r'not\s*disclosed|negotiable', str(v), re.I): return np.nan
    x = float(np.mean([float(n[0]), float(n[1])])) if len(n) > 1 else float(n[0])
    return x if x > 0 else np.nan

def col(df, *keys, exclude=()):
    for k in keys:
        for c in df.columns:
            cl = c.lower().replace(' ', '')
            if k in cl and not any(e in cl for e in exclude): return c
    return None

def skills_of(v):
    if pd.isna(v): return []
    out = []
    for t in re.split(r'[,;/|]', str(v).lower()):
        t = re.sub(r'\s+', ' ', t).strip(' .-')
        t = SYN.get(t, t)
        if t in HARD or t in SOFT: out.append(t)
    return list(dict.fromkeys(out))

def role_of(v):
    return re.sub(r'\s+', ' ', str(v).strip().title())[:60] if pd.notna(v) else ''

# ---------- A + B: skill map ----------
A, B = find('cleaned_ds_jobs.csv','DataScience Jobs.csv'), find('cleaned_analytics_jobs.csv','Analytics Jobs.csv')
bs = col(B,'key_skills','skills_extracted'); br = col(B,'job_desig_norm','job_desig','designation'); bsal = col(B,'salary_annual','salary')
asal = col(A,'salary_annual','avg_salary'); at = col(A,'job_title_norm','job_title')
B['_sk'] = B[bs].apply(skills_of)
B['_role'] = B[br].apply(role_of) if br else ''
B['_sal'] = B[bsal].apply(lakhs) if bsal else np.nan
A['_sal'] = A[asal].apply(lakhs); A['_role'] = A[at].apply(role_of)
a_med = A.groupby('_role')['_sal'].median().dropna().to_dict()
cnt = Counter(s for l in B['_sk'] for s in l)
keep = {s for s, _ in cnt.most_common(TOP_SKILLS)}
pair = Counter()
for l in B['_sk']:
    for x, y in combinations(sorted(set(l) & keep), 2): pair[(x, y)] += 1
info = {}
for s in keep:
    m = B[B['_sk'].apply(lambda l: s in l)]
    roles = m['_role'][m['_role'] != ''].value_counts()
    role = roles.index[0] if len(roles) else ''
    sal = m['_sal'].median()
    if not sal > 0: sal = a_med.get(role, np.nan)          # fall back to Dataset A salary for that role
    info[s] = (role, round(float(sal), 1) if sal > 0 else '')  # blank, never 0
rows = []
for (x, y), c in pair.items():
    if c < MIN_PAIR: continue
    st = round(c / np.sqrt(cnt[x] * cnt[y]), 4)
    for a, b in ((x, y), (y, x)):
        rows.append((nice(a), nice(b), st, c, info[b][1], info[b][0], 'soft' if b in SOFT else 'hard'))
pd.DataFrame(rows, columns=['known_skill','study_next','connection_strength','co_occurrence_count','target_salary_lpa','target_role','category']).to_csv(os.path.join(HERE,'skill_connections_rich.csv'), index=False)
print(f'skill_connections_rich.csv: {len(rows)} links, {len(keep)} skills')

# ---------- market side of the paradox ----------
tot = sum(cnt.values()); hard_n = sum(v for k, v in cnt.items() if k in HARD); soft_n = sum(v for k, v in cnt.items() if k in SOFT)
post = {k: sum(1 for l in B['_sk'] if set(l) & CAT[k]) / max(len(B), 1) for k in CAT}

# ---------- C: what gets juniors a high hike ----------
C = find('cleaned_jds_skills.csv','JDS Skill Traits.xlsx')
tgt = col(C,'salary_hike'); feat = {k: col(C,*ks,exclude=('flag','imput','outlier')) for k, ks in
    {'story':('dashboard','storytell'),'stats':('stat','math'),'code':('coding',),'ai':('ai_','ml'),'bigdata':('big_data','bigdata')}.items()}
C = C[[tgt, *feat.values()]].apply(pd.to_numeric, errors='coerce').dropna()
X, y = C[list(feat.values())], C[tgt].astype(int)
rf = RandomForestClassifier(n_estimators=500, random_state=42).fit(X, y)
cv = StratifiedKFold(5, shuffle=True, random_state=42)
acc_c = cross_val_score(RandomForestClassifier(n_estimators=300, random_state=42), X, y, cv=cv).mean()
junior = [{'key': k, 'label': LABEL[k], 'importance': round(float(i), 4), 'corr': round(float(X[c].corr(y)), 3), 'market_share': round(post[k], 4),
           'lift': round(float(i) / max(post[k], .01), 2)} for (k, c), i in zip(feat.items(), rf.feature_importances_)]
junior.sort(key=lambda d: -d['importance'])

# ---------- D: what makes seniors successful ----------
D = find('cleaned_sds_personality.csv','SDS Personality Traits.xlsx'); D.columns = [c.strip() for c in D.columns]
tr = {t: col(D,t,exclude=('normal','zscore','flag')) for t in ('conscientiousness','openness','extraversion','agreeableness','neuroticism')}
dt = col(D,'success'); D = D[[dt, *tr.values()]].apply(pd.to_numeric, errors='coerce').dropna()
Xd, yd = D[list(tr.values())], D[dt].astype(int)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xd, yd)
acc_d = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), Xd, yd, cv=cv).mean()
senior = sorted([{'trait': t, 'r': round(float(Xd[c].corr(yd)), 3), 'odds_ratio': round(float(np.exp(b)), 2)} for (t, c), b in zip(tr.items(), pipe[-1].coef_[0])], key=lambda d: -d['r'])

out = {'market': {'postings': len(B), 'hard': hard_n, 'soft': soft_n, 'hard_share': round(hard_n / tot, 4), 'ratio': round(hard_n / max(soft_n, 1), 2),
                  'top_hard': [k for k, _ in cnt.most_common() if k in HARD][:6], 'top_soft': [k for k, _ in cnt.most_common() if k in SOFT][:6]},
       'junior': {'n': len(C), 'cv_accuracy': round(float(acc_c), 3), 'features': junior},
       'senior': {'n': len(D), 'cv_accuracy': round(float(acc_d), 3), 'traits': senior},
       'categories': {k: sorted(v) for k, v in CAT.items()}}
json.dump(out, open(os.path.join(HERE, 'paradox.json'), 'w'), indent=1)
print('paradox.json written. Junior top driver:', junior[0]['label'], junior[0]['importance'], '| Senior top trait:', senior[0]['trait'], senior[0]['r'])