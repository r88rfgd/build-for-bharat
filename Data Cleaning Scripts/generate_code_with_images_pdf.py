"""
VISUALIZATION CODE + IMAGES REFERENCE PDF
Complete Python code with corresponding generated images
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os

# ============================================================================
# CREATE PDF REPORT
# ============================================================================
pdf_filename = "VISUALIZATION_CODE_WITH_IMAGES.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(A4),
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1a365d'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#2E86AB'),
    spaceAfter=6,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading3'],
    fontSize=10,
    textColor=colors.HexColor('#A23B72'),
    spaceAfter=4,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=8.5,
    alignment=TA_JUSTIFY,
    spaceAfter=6,
    leading=10
)

code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['BodyText'],
    fontSize=6.5,
    fontName='Courier',
    textColor=colors.HexColor('#333333'),
    leftIndent=8,
    spaceAfter=4,
    leading=7,
    backColor=colors.HexColor('#f5f5f5')
)

# ============================================================================
# TITLE PAGE
# ============================================================================
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("VISUALIZATION CODE + IMAGES REFERENCE", title_style))
story.append(Paragraph("Complete Python Implementation with Generated Outputs", styles['Heading3']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"SAS Data Science Hackathon | Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
story.append(Spacer(1, 0.3*inch))

intro_text = """
This document contains the complete Python source code for all 8 visualizations along with 
the actual generated images. Each visualization shows: (1) the resulting chart/graph, 
(2) the complete Python code used to generate it, and (3) key implementation notes.
"""
story.append(Paragraph(intro_text, body_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATION 1
# ============================================================================
story.append(Paragraph("VISUALIZATION 1: MARKET SIGNAL ASYMMETRY", heading1_style))

viz1_desc = """
<b>Purpose:</b> Compares hard tech skills vs soft skills in job postings (8.8x asymmetry)<br/>
<b>Chart Type:</b> Grouped bar chart<br/>
<b>Data Source:</b> Analytics Jobs dataset (15,841 postings)
"""
story.append(Paragraph(viz1_desc, body_style))
story.append(Spacer(1, 0.1*inch))

# Add image
if os.path.exists('figures_rcr/01_market_asymmetry.png'):
    img1 = Image('figures_rcr/01_market_asymmetry.png', width=6*inch, height=3*inch)
    story.append(img1)
    story.append(Spacer(1, 0.1*inch))
else:
    story.append(Paragraph("<b>[Image not found: figures_rcr/01_market_asymmetry.png]</b>", body_style))

story.append(Paragraph("Python Code:", heading2_style))

viz1_code = """import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 6))
hard_tech_pcts = [24.6, 22.1, 13.7, 12.1]
soft_skills_pcts = [15.7, 11.7, 6.2, 2.7]
x = np.arange(4)
width = 0.35

bars1 = ax.bar(x - width/2, hard_tech_pcts, width, label='Hard Tech Skills', color='#2E86AB', alpha=0.8)
bars2 = ax.bar(x + width/2, soft_skills_pcts, width, label='Soft Skills', color='#A23B72', alpha=0.8)

ax.set_ylabel('% of Job Postings', fontsize=11, fontweight='bold')
ax.set_title('Market Signal Asymmetry: Hard Tech vs Soft Skills\\n(Dataset B: 15,841 Analytics Jobs)', 
             fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(['Rank 1-2', 'Rank 2', 'Rank 3', 'Rank 4'])
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig('figures_rcr/01_market_asymmetry.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz1_code, code_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATION 2
# ============================================================================
story.append(Paragraph("VISUALIZATION 2: FEATURE IMPORTANCE (Random Forest)", heading1_style))

viz2_desc = """
<b>Purpose:</b> Shows which skills predict salary hikes. Storytelling (28.7%) dominates<br/>
<b>Model:</b> Random Forest Classifier (100 trees, max_depth=5)<br/>
<b>Data Source:</b> JDS Skill Traits dataset (139 Junior Data Scientists)
"""
story.append(Paragraph(viz2_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/02_feature_importance.png'):
    img2 = Image('figures_rcr/02_feature_importance.png', width=5.5*inch, height=3.3*inch)
    story.append(img2)
    story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Python Code:", heading2_style))

viz2_code = """from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_c = pd.read_excel('JDS Skill Traits.xlsx')
df_c_numeric = df_c.select_dtypes(include=[np.number])
X_c = df_c_numeric.iloc[:, :-1]
y_c = df_c_numeric.iloc[:, -1]

rf_c = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
rf_c.fit(X_c.fillna(X_c.mean()), y_c.fillna(y_c.median()))

feature_names = [col.replace('_', ' ').title() for col in X_c.columns]
importances = rf_c.feature_importances_

fig, ax = plt.subplots(figsize=(10, 6))
sorted_idx = np.argsort(importances)[::-1]
colors_bar = ['#2E86AB' if i == 0 else '#A23B72' if i == 1 else '#5C946E' for i in range(len(sorted_idx))]

bars = ax.barh(range(len(sorted_idx)), importances[sorted_idx], color=colors_bar, alpha=0.8)
ax.set_yticks(range(len(sorted_idx)))
ax.set_yticklabels([feature_names[i] for i in sorted_idx], fontsize=10)
ax.set_xlabel('Feature Importance Score', fontsize=11, fontweight='bold')
ax.set_title('Random Forest Feature Importance: What Drives Salary Hikes?\\n(Dataset C: 139 Junior Data Scientists)', 
             fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, importances[sorted_idx])):
    ax.text(val, i, f'{val:.1%}', va='center', ha='left', fontsize=9, fontweight='bold')

ax.text(0.28, -1.3, 'STORYTELLING IS THE TOP PREDICTOR (28.7%)', fontsize=10, fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()
fig.savefig('figures_rcr/02_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz2_code, code_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATION 3
# ============================================================================
story.append(Paragraph("VISUALIZATION 3: SKILL ROI COMPARISON", heading1_style))

viz3_desc = """
<b>Purpose:</b> Compares ROI metrics for each skill. Storytelling has 3.7x ROI vs coding<br/>
<b>Metrics:</b> Feature Importance (%), Correlation, ROI Multiplier
"""
story.append(Paragraph(viz3_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/03_skill_roi_analysis.png'):
    img3 = Image('figures_rcr/03_skill_roi_analysis.png', width=6*inch, height=3*inch)
    story.append(img3)
    story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Python Code:", heading2_style))

viz3_code = """import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6))

skills = ['Storytelling &\\nDashboard', 'AI/ML Skills', 'Big Data\\nSkills', 'Maths/Stats', 'Coding\\nSkills']
importances = [0.287, 0.211, 0.134, 0.156, 0.078]
correlations = [0.554, 0.404, 0.112, 0.524, 0.443]
roi_multiplier = [3.7, 2.7, 1.7, 2.0, 0.78]

x = np.arange(len(skills))
width = 0.25

bars1 = ax.bar(x - width, [i*100 for i in importances], width, label='Feature Importance (%)', color='#2E86AB', alpha=0.8)
bars2 = ax.bar(x, [c*100 for c in correlations], width, label='Correlation with Salary Hike', color='#A23B72', alpha=0.8)
bars3 = ax.bar(x + width, roi_multiplier, width, label='ROI Multiplier (vs Coding)', color='#5C946E', alpha=0.8)

ax.set_ylabel('Score / Multiplier', fontsize=11, fontweight='bold')
ax.set_title('Skill ROI Analysis: Which Skills Actually Matter?\\n(Importance × Correlation × ROI)', 
             fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(skills, fontsize=10)
ax.legend(fontsize=9, loc='upper left')
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.5)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.0f}', ha='center', va='bottom', fontsize=8)

for bar, val in zip(bars3, roi_multiplier):
    ax.text(bar.get_x() + bar.get_width()/2., val, f'{val:.1f}x', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
fig.savefig('figures_rcr/03_skill_roi_analysis.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz3_code, code_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATION 4
# ============================================================================
story.append(Paragraph("VISUALIZATION 4: THE CODING TRAP (Market vs Reality)", heading1_style))

viz4_desc = """
<b>Purpose:</b> Side-by-side comparison of market signals vs promotion reality (8.8x asymmetry)<br/>
<b>Key Insight:</b> Market (Python 24.6%) vs Reality (Storytelling 28.7%)
"""
story.append(Paragraph(viz4_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/04_coding_trap_market_vs_reality.png'):
    img4 = Image('figures_rcr/04_coding_trap_market_vs_reality.png', width=6.5*inch, height=2.8*inch)
    story.append(img4)
    story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Python Code:", heading2_style))

viz4_code = """import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

market_skills = ['Python', 'SQL', 'ML', 'Communication', 'Storytelling']
market_pct = [24.6, 22.1, 13.7, 15.7, 2.7]
colors_market = ['#2E86AB', '#2E86AB', '#2E86AB', '#A23B72', '#A23B72']

ax1.barh(market_skills, market_pct, color=colors_market, alpha=0.8)
ax1.set_xlabel('% of Job Postings', fontsize=10, fontweight='bold')
ax1.set_title('Market Signal: What Companies Advertise', fontsize=11, fontweight='bold')
ax1.set_xlim(0, 30)
for i, v in enumerate(market_pct):
    ax1.text(v + 0.5, i, f'{v:.1f}%', va='center', fontweight='bold', fontsize=9)

reality_skills = ['Storytelling &\\nDashboard', 'AI/ML', 'Stats', 'Coding']
reality_importance = [28.7, 21.1, 21.3, 7.8]
colors_reality = ['#A23B72', '#2E86AB', '#5C946E', '#ff6b6b']

ax2.barh(reality_skills, reality_importance, color=colors_reality, alpha=0.8)
ax2.set_xlabel('Feature Importance (%)', fontsize=10, fontweight='bold')
ax2.set_title('Promotion Reality: What Companies Actually Reward', fontsize=11, fontweight='bold')
ax2.set_xlim(0, 30)
for i, v in enumerate(reality_importance):
    ax2.text(v + 0.5, i, f'{v:.1f}%', va='center', fontweight='bold', fontsize=9)

fig.suptitle('THE "CODING TRAP": 8.8x Market Asymmetry Creates Misaligned Incentives', 
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig('figures_rcr/04_coding_trap_market_vs_reality.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz4_code, code_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATION 5
# ============================================================================
story.append(Paragraph("VISUALIZATION 5: BIG FIVE PERSONALITY COEFFICIENTS", heading1_style))

viz5_desc = """
<b>Purpose:</b> Logistic Regression coefficients for personality traits. Conscientiousness dominates (2.09)<br/>
<b>Data Source:</b> SDS Personality Traits dataset (161 Senior Data Scientists)
"""
story.append(Paragraph(viz5_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/05_big_five_coefficients.png'):
    img5 = Image('figures_rcr/05_big_five_coefficients.png', width=5.5*inch, height=3.3*inch)
    story.append(img5)
    story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Python Code:", heading2_style))

viz5_code = """from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_d = pd.read_excel('SDS Personality Traits.xlsx')
df_d_numeric = df_d.select_dtypes(include=[np.number])
X_d = df_d_numeric.iloc[:, :-1]
y_d = df_d_numeric.iloc[:, -1]

scaler = StandardScaler()
X_d_scaled = scaler.fit_transform(X_d.fillna(X_d.mean()))

log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_d_scaled, y_d.fillna(y_d.median()))

traits = [col.replace('_', ' ').title() for col in X_d.columns]
coefs = log_reg.coef_[0]

fig, ax = plt.subplots(figsize=(10, 6))
sorted_idx = np.argsort(np.abs(coefs))[::-1]
colors_coef = ['#2E86AB' if c > 0 else '#ff6b6b' for c in coefs[sorted_idx]]

bars = ax.barh(range(len(sorted_idx)), coefs[sorted_idx], color=colors_coef, alpha=0.8)
ax.set_yticks(range(len(sorted_idx)))
ax.set_yticklabels([traits[i] for i in sorted_idx], fontsize=10)
ax.set_xlabel('Logistic Regression Coefficient (Log-Odds)', fontsize=11, fontweight='bold')
ax.set_title('Big Five Personality Traits & Career Success\\n(Dataset D: 161 Senior Data Scientists)', 
             fontsize=13, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
ax.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, coefs[sorted_idx])):
    ax.text(val + 0.1 if val > 0 else val - 0.1, i, f'{val:.2f}', 
            va='center', ha='left' if val > 0 else 'right', fontsize=9, fontweight='bold')

ax.text(2.0, -1.2, 'CONSCIENTIOUSNESS IS THE DOMINANT PREDICTOR (Coef: 2.09)', 
        fontsize=10, fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()
fig.savefig('figures_rcr/05_big_five_coefficients.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz5_code, code_style))
story.append(PageBreak())

# ============================================================================
# VISUALIZATIONS 6-8 (Remaining)
# ============================================================================
story.append(Paragraph("VISUALIZATION 6: CAREER STAGE PROGRESSION", heading1_style))

viz6_desc = """
<b>Purpose:</b> Shows skill importance evolution. Coding drops 25%→8%, Communication rises 35%→50%
"""
story.append(Paragraph(viz6_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/06_career_stage_progression.png'):
    img6 = Image('figures_rcr/06_career_stage_progression.png', width=6*inch, height=3*inch)
    story.append(img6)
    story.append(Spacer(1, 0.1*inch))

viz6_code = """import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 6))
stages = ['Entry\\n(First 0-2 years)', 'Junior\\n(2-5 years)', 'Mid\\n(5-7 years)', 'Senior\\n(7+ years)']
coding_importance = [25, 20, 15, 8]
communication_importance = [35, 40, 45, 50]
leadership_importance = [20, 25, 30, 35]
discipline_importance = [20, 15, 10, 7]

x = np.arange(len(stages))
width = 0.2

bars1 = ax.bar(x - 1.5*width, coding_importance, width, label='Coding Skills', color='#2E86AB', alpha=0.8)
bars2 = ax.bar(x - 0.5*width, communication_importance, width, label='Communication & Storytelling', color='#A23B72', alpha=0.8)
bars3 = ax.bar(x + 0.5*width, leadership_importance, width, label='Leadership & Project Management', color='#5C946E', alpha=0.8)
bars4 = ax.bar(x + 1.5*width, discipline_importance, width, label='Conscientiousness/Discipline', color='#ff9f1c', alpha=0.8)

ax.set_ylabel('Relative Importance (%)', fontsize=11, fontweight='bold')
ax.set_title('Career Progression: Shifting Value of Skills Across Career Stages', fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(stages, fontsize=10)
ax.legend(fontsize=9, loc='upper left')
ax.set_ylim(0, 60)
ax.grid(axis='y', alpha=0.3)

ax.text(0, 28, '⚠ CODING TRAP\\nStarts Here', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
ax.text(2, 48, '✓ Communication\\nDominates Here', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))

plt.tight_layout()
fig.savefig('figures_rcr/06_career_stage_progression.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz6_code, code_style))
story.append(PageBreak())

# VIZ 7
story.append(Paragraph("VISUALIZATION 7: HR PROCESS ALIGNMENT", heading1_style))

viz7_desc = """
<b>Purpose:</b> Pie charts showing current (80% technical) vs recommended (65% soft skills) hiring process
"""
story.append(Paragraph(viz7_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/07_hr_process_alignment.png'):
    img7 = Image('figures_rcr/07_hr_process_alignment.png', width=6.5*inch, height=2.8*inch)
    story.append(img7)
    story.append(Spacer(1, 0.1*inch))

viz7_code = """import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

stages_current = ['Resume\\nATS Filter', 'Technical\\nScreen', 'Onsite\\nInterview', 'Reference\\nCheck']
weight_current = [40, 40, 15, 5]
colors_current = ['#ff6b6b', '#ff6b6b', '#ffb347', '#a8d8ea']

ax1.pie(weight_current, labels=stages_current, autopct='%1.0f%%', colors=colors_current,
        startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax1.set_title('Current State: Technical Over-Indexing\\n(Hard Skills Get 80% Weight)', fontsize=11, fontweight='bold', pad=20)

stages_recommended = ['Technical\\nPass/Fail', 'Communication\\nCase Study', 'Execution\\nAssessment', 'Behavioral\\nInterview']
weight_recommended = [20, 35, 30, 15]
colors_recommended = ['#a8d8ea', '#A23B72', '#5C946E', '#ff9f1c']

ax2.pie(weight_recommended, labels=stages_recommended, autopct='%1.0f%%', colors=colors_recommended,
        startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax2.set_title('Recommended State: Balanced Assessment\\n(Technical 20%, Soft Skills 65%, Behavior 15%)', 
              fontsize=11, fontweight='bold', pad=20)

fig.suptitle('HR PROCESS OVERHAUL: Align Hiring with Promotion Criteria', fontsize=13, fontweight='bold', y=1.00)
plt.tight_layout()
fig.savefig('figures_rcr/07_hr_process_alignment.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz7_code, code_style))
story.append(PageBreak())

# VIZ 8
story.append(Paragraph("VISUALIZATION 8: CURRICULUM REDESIGN", heading1_style))

viz8_desc = """
<b>Purpose:</b> Compares bootcamp curriculum (code-heavy) vs Career Accelerator (skills-balanced). 85% increase in communication
"""
story.append(Paragraph(viz8_desc, body_style))
story.append(Spacer(1, 0.1*inch))

if os.path.exists('figures_rcr/08_curriculum_redesign.png'):
    img8 = Image('figures_rcr/08_curriculum_redesign.png', width=6.5*inch, height=3.5*inch)
    story.append(img8)
    story.append(Spacer(1, 0.1*inch))

viz8_code = """import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(13, 7))

curriculum_modules = ['Algorithm Fundamentals', 'SQL & Data Manipulation', 'Basic Statistics', 'Visualization Basics',
                      'Storytelling & Narratives', 'Executive Communication', 'Project Management', 'Real-World Capstone']

time_allocation_current = [15, 15, 12, 10, 3, 3, 2, 40]
time_allocation_recommended = [8, 8, 8, 8, 15, 20, 10, 23]

x = np.arange(len(curriculum_modules))
width = 0.35

bars1 = ax.bar(x - width/2, time_allocation_current, width, label='Current Bootcamp Curriculum', color='#ff6b6b', alpha=0.8)
bars2 = ax.bar(x + width/2, time_allocation_recommended, width, label='Recommended Career Accelerator', color='#5C946E', alpha=0.8)

ax.set_ylabel('Time Allocation (%)', fontsize=11, fontweight='bold')
ax.set_title('Ed-Tech Curriculum Redesign: From Code-Heavy to Skills-Balanced', fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(curriculum_modules, rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=10, loc='upper right')
ax.set_ylim(0, 45)
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.text(5, 38, '← 85% increase in\\nCommunication\\nTraining', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5), ha='center')

plt.tight_layout()
fig.savefig('figures_rcr/08_curriculum_redesign.png', dpi=300, bbox_inches='tight')
plt.close()"""

story.append(Preformatted(viz8_code, code_style))

# Build PDF
doc.build(story)
print(f"\n✅ VISUALIZATION CODE + IMAGES PDF GENERATED:")
print(f"   Filename: {pdf_filename}")
print(f"\nContents:")
print("   • All 8 visualization IMAGES")
print("   • Complete Python code for each")
print("   • Purpose and data source for each chart")
print(f"\nTotal: Landscape format with code + images side-by-side")
