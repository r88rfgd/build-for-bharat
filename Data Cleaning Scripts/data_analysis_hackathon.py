"""
Data Science Hackathon Analysis
Tasks:
1. Clean and merge datasets
2. NLP analysis on skills
3. Create visualizations
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# TASK 1: CLEAN THE MESS (Data Engineering)
# ============================================================================

print("=" * 80)
print("TASK 1: DATA CLEANING & ENGINEERING")
print("=" * 80)

# Load datasets
print("\nLoading datasets...")
ds_jobs = pd.read_csv('DataScience Jobs.csv')
analytics_jobs = pd.read_csv('Analytics Jobs.csv')

print(f"Original shapes: DS Jobs: {ds_jobs.shape}, Analytics Jobs: {analytics_jobs.shape}")

# ============================================================================
# 1.1 SALARY STANDARDIZATION
# ============================================================================
print("\n--- Standardizing Salaries ---")

def convert_salary_to_annual(salary_str):
    """Convert salary string to annual salary in lakhs"""
    if pd.isna(salary_str) or salary_str == '':
        return np.nan
    
    salary_str = str(salary_str).strip().upper()
    
    # Handle range format (e.g., "6to10", "6-10")
    if 'TO' in salary_str or '-' in salary_str:
        nums = re.findall(r'[\d.]+', salary_str)
        if len(nums) >= 2:
            return float((float(nums[0]) + float(nums[1])) / 2)
        elif len(nums) == 1:
            return float(nums[0])
    
    # Handle single values with L suffix (Lakhs)
    if 'L' in salary_str:
        nums = re.findall(r'[\d.]+', salary_str)
        if nums:
            return float(nums[0])
    
    # Handle numeric strings
    try:
        return float(re.findall(r'[\d.]+', salary_str)[0])
    except:
        return np.nan

# Standardize DS Jobs salaries
ds_jobs['salary_annual'] = ds_jobs['avg_salary'].apply(convert_salary_to_annual)
analytics_jobs['salary_annual'] = analytics_jobs['salary'].apply(convert_salary_to_annual)

print(f"DS Jobs salary stats:\n{ds_jobs['salary_annual'].describe()}")
print(f"\nAnalytics Jobs salary stats:\n{analytics_jobs['salary_annual'].describe()}")

# ============================================================================
# 1.2 JOB TITLE NORMALIZATION
# ============================================================================
print("\n--- Normalizing Job Titles ---")

def normalize_job_title(title):
    """Normalize job titles"""
    if pd.isna(title):
        return None
    
    title = str(title).strip().lower()
    
    replacements = {
        r'\bdata\s+scientist\b': 'data scientist',
        r'\bdata\s+analyst\b': 'data analyst',
        r'\bdata\s+engineer\b': 'data engineer',
        r'\bmachine\s+learning\b': 'machine learning',
        r'\bml\s+engineer\b': 'ml engineer',
        r'\bsenior\b': 'senior',
        r'\bjunior\b': 'junior',
        r'\blead\b': 'lead',
    }
    
    for pattern, replacement in replacements.items():
        title = re.sub(pattern, replacement, title)
    
    return title.strip()

ds_jobs['job_title_norm'] = ds_jobs['job_title'].apply(normalize_job_title)
analytics_jobs['job_desig_norm'] = analytics_jobs['job_desig'].apply(normalize_job_title)

print(f"Sample normalized titles:\n{ds_jobs[['job_title', 'job_title_norm']].drop_duplicates().head(10)}")

# ============================================================================
# 1.3 LOCATION NORMALIZATION
# ============================================================================
print("\n--- Normalizing Locations ---")

def normalize_location(loc_str):
    """Normalize location names"""
    if pd.isna(loc_str):
        return None
    
    loc = str(loc_str).strip().upper()
    
    # Take first location if multiple
    if ',' in loc:
        loc = loc.split(',')[0].strip()
    
    # Standardize common city names
    replacements = {
        'BANGALORE': 'BENGALURU',
        'BENGALORE': 'BENGALURU',
        'BOMBAY': 'MUMBAI',
        'DELHI': 'NEW DELHI',
        'KOLKATTA': 'KOLKATA',
    }
    
    for old, new in replacements.items():
        if old in loc:
            loc = loc.replace(old, new)
    
    return loc.strip()

analytics_jobs['location_norm'] = analytics_jobs['location'].apply(normalize_location)

print(f"Top 10 locations:\n{analytics_jobs['location_norm'].value_counts().head(10)}")

# Save cleaned datasets
ds_jobs.to_csv('cleaned_ds_jobs.csv', index=False)
analytics_jobs.to_csv('cleaned_analytics_jobs.csv', index=False)
print("\n✓ Saved cleaned_ds_jobs.csv and cleaned_analytics_jobs.csv")

# ============================================================================
# TASK 2: TEXT MINING (NLP)
# ============================================================================

print("\n" + "=" * 80)
print("TASK 2: TEXT MINING & NLP ANALYSIS")
print("=" * 80)

# Define skill categories
HARD_TECH_SKILLS = {
    'python', 'r', 'java', 'sql', 'scala', 'javascript', 'typescript', 'golang', 'rust',
    'c++', 'c#', 'php', 'ruby', 'kotlin', 'swift',
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'ai', 'artificial intelligence',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas', 'numpy', 'scipy',
    'hadoop', 'spark', 'pyspark', 'hive', 'impala', 'presto',
    'aws', 'azure', 'gcp', 'google cloud', 'cloud', 'lambda', 's3',
    'docker', 'kubernetes', 'jenkins', 'git', 'gitlab', 'github',
    'mysql', 'postgresql', 'mongodb', 'cassandra', 'dynamodb', 'redis', 'elasticsearch',
    'tableau', 'power bi', 'powerbi', 'looker', 'qlik', 'excel', 'vba',
    'etl', 'elt', 'data pipeline', 'data engineering',
    'linux', 'windows', 'unix', 'bash', 'shell',
    'rest api', 'graphql', 'soap', 'microservices',
    'agile', 'scrum', 'statistics', 'statistical', 'mathematics', 'math',
    'api', 'rest', 'json', 'xml', 'regression', 'classification', 'clustering'
}

SOFT_SKILLS = {
    'communication', 'communicative', 'verbal', 'presentation', 'storytelling',
    'leadership', 'leader', 'team lead', 'management',
    'problem solving', 'critical thinking', 'analytical', 'analysis',
    'collaboration', 'collaborative', 'teamwork', 'team player',
    'time management', 'organization', 'organized',
    'adaptability', 'adaptable', 'flexible', 'flexibility',
    'attention to detail', 'detail-oriented',
    'customer service', 'customer focus', 'stakeholder management',
    'decision making', 'strategic thinking',
    'interpersonal', 'relationship building', 'networking',
    'learning', 'quick learner', 'continuous learning',
    'documentation', 'reporting',
}

# Extract skills from Analytics Jobs
print("\n--- Extracting Skills from Analytics Jobs ---")

def extract_skills(skills_str):
    """Extract individual skills from comma-separated string"""
    if pd.isna(skills_str):
        return []
    
    skills = str(skills_str).lower().split(',')
    return [s.strip() for s in skills if s.strip()]

analytics_jobs['skills_list'] = analytics_jobs['key_skills'].apply(extract_skills)

# Flatten all skills
all_skills_flat = []
for skills_list in analytics_jobs['skills_list']:
    all_skills_flat.extend(skills_list)

print(f"Total skill mentions: {len(all_skills_flat)}")
print(f"Unique skills: {len(set(all_skills_flat))}")

# Categorize skills
hard_skills_count = Counter()
soft_skills_count = Counter()

for skill in all_skills_flat:
    skill_clean = skill.strip().lower()
    
    # Check if skill matches hard tech skills
    matched = False
    for hard_skill in HARD_TECH_SKILLS:
        if hard_skill in skill_clean or skill_clean in hard_skill:
            hard_skills_count[hard_skill] += 1
            matched = True
            break
    
    if not matched:
        # Check if skill matches soft skills
        for soft_skill in SOFT_SKILLS:
            if soft_skill in skill_clean or skill_clean in soft_skill:
                soft_skills_count[soft_skill] += 1
                break

print(f"\nHard Tech Skills found: {len(hard_skills_count)}")
print(f"Soft Skills found: {len(soft_skills_count)}")

# Top skills
print("\n--- Top 15 Hard Tech Skills ---")
for skill, count in hard_skills_count.most_common(15):
    print(f"  {skill}: {count}")

print("\n--- Top 15 Soft Skills ---")
for skill, count in soft_skills_count.most_common(15):
    print(f"  {skill}: {count}")

# Aggregate by category
hard_skills_total = sum(hard_skills_count.values())
soft_skills_total = sum(soft_skills_count.values())

print(f"\n=== SKILL DEMAND SUMMARY ===")
print(f"Hard Tech Skills Total: {hard_skills_total}")
print(f"Soft Skills Total: {soft_skills_total}")
print(f"Ratio (Hard:Soft): {hard_skills_total / soft_skills_total if soft_skills_total > 0 else 'N/A':.2f}:1")

# Save skill data
skill_summary = pd.DataFrame({
    'skill': list(hard_skills_count.keys()) + list(soft_skills_count.keys()),
    'count': list(hard_skills_count.values()) + list(soft_skills_count.values()),
    'category': ['Hard Tech'] * len(hard_skills_count) + ['Soft Skills'] * len(soft_skills_count)
})
skill_summary = skill_summary.sort_values('count', ascending=False)
skill_summary.to_csv('skill_analysis.csv', index=False)
print("\n✓ Saved skill_analysis.csv")

# ============================================================================
# TASK 3: VISUAL OUTPUTS
# ============================================================================

print("\n" + "=" * 80)
print("TASK 3: VISUALIZATIONS")
print("=" * 80)

# ============================================================================
# 3.1 GEOGRAPHIC HEAT MAP / BAR CHART
# ============================================================================
print("\n--- Creating Location Hotspot Visualization ---")

location_counts = analytics_jobs['location_norm'].value_counts().head(15)

plt.figure(figsize=(14, 8))
colors = sns.color_palette("viridis", len(location_counts))
bars = plt.barh(range(len(location_counts)), location_counts.values, color=colors)
plt.yticks(range(len(location_counts)), location_counts.index)
plt.xlabel('Number of Job Postings', fontsize=12, fontweight='bold')
plt.ylabel('Location', fontsize=12, fontweight='bold')
plt.title('Top 15 Job Hotspots by Location\n(Analytics Jobs Dataset)', 
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, location_counts.values)):
    plt.text(value + 50, i, f'{int(value):,}', 
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('location_hotspots.png', dpi=300, bbox_inches='tight')
print("✓ Saved location_hotspots.png")
plt.close()

# ============================================================================
# 3.2 HARD TECH vs SOFT SKILLS BAR CHART
# ============================================================================
print("\n--- Creating Skills Demand Comparison ---")

# Aggregate totals
skill_totals = {
    'Hard Tech Skills': hard_skills_total,
    'Soft Skills': soft_skills_total
}

plt.figure(figsize=(12, 8))
categories = list(skill_totals.keys())
values = list(skill_totals.values())
colors = ['#2E86AB', '#A23B72']

bars = plt.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
plt.ylabel('Total Mentions in Job Postings', fontsize=12, fontweight='bold')
plt.title('Market Demand: Hard Tech Skills vs Soft Skills\n(Based on Analytics Jobs Dataset)', 
          fontsize=14, fontweight='bold', pad=20)

# Add value labels on bars
for bar, value in zip(bars, values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(value):,}\n({value/sum(values)*100:.1f}%)',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylim(0, max(values) * 1.15)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('skills_demand_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved skills_demand_comparison.png")
plt.close()

# ============================================================================
# 3.3 TOP SKILLS BREAKDOWN
# ============================================================================
print("\n--- Creating Detailed Skills Breakdown ---")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Top Hard Tech Skills
top_hard = hard_skills_count.most_common(10)
hard_names = [skill for skill, _ in top_hard]
hard_counts = [count for _, count in top_hard]

ax1.barh(range(len(hard_names)), hard_counts, color='#2E86AB', edgecolor='black', linewidth=1)
ax1.set_yticks(range(len(hard_names)))
ax1.set_yticklabels(hard_names)
ax1.set_xlabel('Mentions', fontsize=11, fontweight='bold')
ax1.set_title('Top 10 Hard Tech Skills', fontsize=12, fontweight='bold')
ax1.invert_yaxis()
for i, v in enumerate(hard_counts):
    ax1.text(v + 50, i, f'{v:,}', va='center', fontsize=9, fontweight='bold')

# Top Soft Skills
top_soft = soft_skills_count.most_common(10)
soft_names = [skill for skill, _ in top_soft]
soft_counts = [count for _, count in top_soft]

ax2.barh(range(len(soft_names)), soft_counts, color='#A23B72', edgecolor='black', linewidth=1)
ax2.set_yticks(range(len(soft_names)))
ax2.set_yticklabels(soft_names)
ax2.set_xlabel('Mentions', fontsize=11, fontweight='bold')
ax2.set_title('Top 10 Soft Skills', fontsize=12, fontweight='bold')
ax2.invert_yaxis()
for i, v in enumerate(soft_counts):
    ax2.text(v + 50, i, f'{v:,}', va='center', fontsize=9, fontweight='bold')

plt.suptitle('Detailed Skills Breakdown', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('detailed_skills_breakdown.png', dpi=300, bbox_inches='tight')
print("✓ Saved detailed_skills_breakdown.png")
plt.close()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated Files:")
print("  1. cleaned_ds_jobs.csv - Cleaned DataScience Jobs dataset")
print("  2. cleaned_analytics_jobs.csv - Cleaned Analytics Jobs dataset")
print("  3. skill_analysis.csv - Detailed skill frequency analysis")
print("  4. location_hotspots.png - Geographic job distribution")
print("  5. skills_demand_comparison.png - Hard vs Soft skills comparison")
print("  6. detailed_skills_breakdown.png - Top 10 skills in each category")
print("\nKey Findings:")
print(f"  • Total jobs analyzed: {len(ds_jobs) + len(analytics_jobs):,}")
print(f"  • Hard Tech Skills demand: {hard_skills_total:,} mentions")
print(f"  • Soft Skills demand: {soft_skills_total:,} mentions")
print(f"  • Demand ratio (Hard:Soft): {hard_skills_total / soft_skills_total if soft_skills_total > 0 else 0:.2f}:1")
print(f"  • Top location: {location_counts.index[0]} ({location_counts.values[0]:,} jobs)")
print(f"  • Top hard skill: {hard_skills_count.most_common(1)[0][0]} ({hard_skills_count.most_common(1)[0][1]:,} mentions)")
if soft_skills_count:
    print(f"  • Top soft skill: {soft_skills_count.most_common(1)[0][0]} ({soft_skills_count.most_common(1)[0][1]:,} mentions)")

print("\n" + "=" * 80)
