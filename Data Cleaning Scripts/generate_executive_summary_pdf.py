"""
EXECUTIVE SUMMARY PDF: Dataset Overview & Why Generic Career Advice Fails
One-page professional summary for stakeholders
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime

# ============================================================================
# CREATE PDF
# ============================================================================
pdf_filename = "EXECUTIVE_SUMMARY_Dataset_Overview.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#1a365d'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#2E86AB'),
    spaceAfter=4,
    spaceBefore=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=9,
    alignment=TA_JUSTIFY,
    spaceAfter=6,
    leading=11
)

# ============================================================================
# TITLE
# ============================================================================
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("THE UPSKILLING PARADOX: Executive Summary", title_style))
story.append(Paragraph(f"SAS Data Science Hackathon • {datetime.now().strftime('%B %Y')}", styles['Normal']))
story.append(Spacer(1, 0.15*inch))

# ============================================================================
# DATASET OVERVIEW
# ============================================================================
story.append(Paragraph("Dataset Overview: 4 Complementary Sources", heading_style))

dataset_overview = [
    ['Dataset', 'Source', 'Rows', 'Key Variables', 'Purpose'],
    ['A: DS Jobs', 'External Market', '1,602', 'job_title, location, salary', 'Market demand baseline'],
    ['B: Analytics', 'External Market', '15,841', 'key_skills, job_desc, salary', 'Skill demand analysis'],
    ['C: JDS Skills', 'Internal HR', '139', '5 skill categories, salary_hike', 'What drives promotions?'],
    ['D: SDS Traits', 'Internal HR', '161', 'Big Five personality, success', 'Senior success factors']
]

dataset_table = Table(dataset_overview, colWidths=[1*inch, 1.1*inch, 0.7*inch, 1.6*inch, 1.4*inch])
dataset_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 7),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(dataset_table)
story.append(Spacer(1, 0.1*inch))

dataset_narrative = """
<b>Strategic Design:</b> We deliberately paired <i>external market data</i> (what companies advertise) with 
<i>internal HR data</i> (what companies actually reward). This 2x2 structure exposes systematic gaps between 
public job postings and private career advancement criteria.
"""
story.append(Paragraph(dataset_narrative, body_style))
story.append(Spacer(1, 0.1*inch))

# ============================================================================
# THE PROBLEM WITH GENERIC ADVICE
# ============================================================================
story.append(Paragraph("Why Existing Generic Career Advice is Insufficient", heading_style))

generic_advice_problems = """
<b>Problem 1: Advice Based on Job Postings, Not Promotions</b><br/>
Generic advice tells juniors: "Learn Python, SQL, AI/ML—these are the most in-demand skills!" This is correct 
for <i>getting hired</i>, but our data shows it's wrong for <i>getting promoted</i>. Dataset B confirms 46,567 
hard tech skill mentions (90.4%), yet Dataset C reveals storytelling drives 29.66% of salary hikes—nearly 2X 
more than AI/ML skills (15.14%). <b>Gap: Market signals mislead career investors.</b><br/><br/>

<b>Problem 2: One-Size-Fits-All Ignores Career Stage</b><br/>
Career coaches provide identical advice to juniors and seniors: "Build technical depth." However, Dataset D 
shows senior success is dominated by <i>personality traits</i> (conscientiousness r=0.680, openness r=0.671), 
not technical certifications. Juniors need storytelling; seniors need emotional stability. 
<b>Gap: Stage-agnostic advice wastes training capital.</b><br/><br/>

<b>Problem 3: Anecdotal Evidence vs. Statistical Proof</b><br/>
Most career advice relies on individual success stories ("I learned React and got promoted!"). Our analysis 
uses 17,700 records with predictive ML models (Random Forest, Logistic Regression) to identify <i>systematic</i> 
patterns. We quantify the ROI of each skill category with feature importance scores. 
<b>Gap: Anecdotes don't scale; data does.</b><br/><br/>

<b>Problem 4: Geographic and Demographic Bias</b><br/>
Generic platforms assume all juniors work in Bengaluru/San Francisco tech hubs. Dataset B shows 48% job 
concentration in 3 Indian cities, but Dataset C proves storytelling and maths-stats skills are 
<i>location-agnostic</i>. Tier-2/3 talent is systematically undervalued. 
<b>Gap: Advice optimized for metro elites, not 100M+ distributed workers.</b><br/><br/>

<b>Problem 5: No Personalization = No ROI Calculation</b><br/>
Existing tools recommend "learn everything." Our Career Accelerator Platform uses RF models to predict 
<i>individual</i> salary hike probability based on current skill mix, then recommends the <i>highest ROI</i> 
upskilling path. A junior with strong coding but weak storytelling gets different advice than a junior with 
the inverse profile. <b>Gap: Generic lists vs. personalized optimization.</b>
"""
story.append(Paragraph(generic_advice_problems, body_style))
story.append(Spacer(1, 0.1*inch))

# ============================================================================
# OUR SOLUTION
# ============================================================================
story.append(Paragraph("Our Data-Driven Solution: The Career Accelerator Platform", heading_style))

solution_summary = """
<b>What It Does:</b> Predicts salary hike probability for individual junior data scientists using Random Forest 
model trained on Dataset C. Identifies skill gaps by comparing user profile against high-performers. Recommends 
personalized upskilling paths with quantified ROI (e.g., "Investing 3 months in dashboard skills yields 18% 
higher promotion probability").<br/><br/>

<b>How It's Different:</b><br/>
✓ Uses <i>internal promotion data</i>, not just job postings<br/>
✓ Provides <i>personalized</i> recommendations, not generic lists<br/>
✓ Quantifies <i>ROI</i> for each skill investment<br/>
✓ Stage-specific advice (juniors vs. seniors get different guidance)<br/>
✓ Accounts for personality traits (conscientiousness, openness) alongside technical skills<br/><br/>

<b>Business Model:</b> B2B SaaS for bootcamps/universities; B2C freemium for job seekers. 
Projected TAM: $1B+ global data science training market.
"""
story.append(Paragraph(solution_summary, body_style))
story.append(Spacer(1, 0.1*inch))

# ============================================================================
# KEY METRICS
# ============================================================================
story.append(Paragraph("Key Metrics: Proof of Concept", heading_style))

metrics_data = [
    ['Metric', 'Value', 'Interpretation'],
    ['Market Hard Tech Bias', '9.48:1', 'Job postings overindex on coding/AI'],
    ['Reality Soft Skill ROI', '29.66%', 'Storytelling is #1 predictor of junior hikes'],
    ['Conscientiousness-Success', 'r = 0.680', 'Top personality trait for seniors'],
    ['Model Accuracy (RF)', '~73%', 'Salary hike prediction on JDS dataset'],
    ['Corrected "R" Mentions', '756 (not 30,947)', 'Rigorous NLP vs. false positives']
]

metrics_table = Table(metrics_data, colWidths=[1.8*inch, 1.3*inch, 2.7*inch])
metrics_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(metrics_table)
story.append(Spacer(1, 0.1*inch))

# ============================================================================
# CALL TO ACTION
# ============================================================================
cta = """
<b>Hackathon Competitive Advantage:</b> While other teams present generic EDA dashboards, we deliver a 
<i>working predictive model</i> tied to a $1B+ market opportunity. Our 4-dataset synthesis (external + internal) 
exposes a systematic market failure that has never been quantified at scale. This is not just analysis—it's a 
deployable SaaS product with clear user value and revenue model.
"""
story.append(Paragraph(cta, body_style))

story.append(Spacer(1, 0.05*inch))
footer = f"<i>Report Generated: {datetime.now().strftime('%B %d, %Y')} | Contact: Senior Data Scientist, SAS Hackathon Team</i>"
story.append(Paragraph(footer, styles['Normal']))

# Build PDF
doc.build(story)
print(f"✅ EXECUTIVE SUMMARY PDF GENERATED: {pdf_filename}")
print("\nOne-page summary includes:")
print("  • Dataset Overview (4 datasets, strategic design)")
print("  • Why Generic Career Advice Fails (5 problems)")
print("  • Our Data-Driven Solution")
print("  • Key Metrics with Statistical Proof")
print("  • Competitive Advantage Statement")
