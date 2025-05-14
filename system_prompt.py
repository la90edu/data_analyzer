import class_school_info
import os
# def get_system_prompt(school_info):
def return_highlighted_text(school_info):
    return f"""
תן היילייט למנהל בית ספר בסגנון  "המדד שנמוך מהממוצע הוא{school_info.worst_anigma_name} _ , המדד נמוך ב___ אחוז מהממוצע הארצי . ההיגד המרכזי שבגללו המדד נמוך הוא ____":        
המדד שנמצא מתחת לממוצע {school_info.worst_anigma_name}
הפער מהממוצע הארצי: {school_info.worst_anigma_value*100} אחוזים
ההיגד שנמצא מתחת לממוצע: {school_info.worst_heg1_text}
  """
# ההיגד השני שנמצא מתחת לממוצע: {school_info.worst_heg2_text if hasattr(school_info, 'worst_heg2_text') else 'לא זמין'}
  
    
def return_prompt(school_info):#worst_anigma_name,worst_anigma_percent, worst_heg1_text,worst_heg2_text,best_anigma_name,best_anigma_percent):
#     knowledge_files=["knowledge-base/CD1.md","knowledge-base/ICI1.md","knowledge-base/CD2.pdf","knowledge-base/ICI2.pdf"]
#     # הכנת מידע על קבצי ידע אם קיימים
#     knowledge_base_info = ""
#     if knowledge_files and isinstance(knowledge_files, list) and len(knowledge_files) > 0:
#         knowledge_base_info = """
# ### קבצי מידע נוספים ###
# יש לך גישה למידע נוסף מהקבצים הבאים:

# return f"""
#         for file_path in knowledge_files:
#             file_name = os.path.basename(file_path)
#             file_ext = os.path.splitext(file_name)[1].lower()
#             file_type = "לא ידוע"
            
#             if file_ext == ".md":
#                 file_type = "Markdown"
#             elif file_ext == ".pdf":
#                 file_type = "PDF"
#             elif file_ext in [".csv", ".xlsx", ".xls"]:
#                 file_type = "נתונים טבלאיים"
#             elif file_ext == ".json":
#                 file_type = "JSON"
#             elif file_ext in [".txt", ".doc", ".docx"]:
#                 file_type = "מסמך טקסט"
                
#             knowledge_base_info += f"- {file_name}: קובץ {file_type} שמכיל מידע רלוונטי. התייחס אליו בתשובתך.\n"
        
#         knowledge_base_info += """
# כאשר משתמש שואל שאלה שקשורה למידע בקבצים אלה, השתמש במידע זה להעשרת תשובתך.

    return f"""
    ### הנחיות כלליות ###
אתה עוזר מומחה המיועד לענות על שאלות הקשורות לנתוני חוסן ותפיסות זמן של בתי ספר בתוכנית "הציר המנטלי".


### סיווג שאלות ###
כאשר אתה מקבל שאלה, עליך ראשית לסווג אותה לאחת מהקטגוריות הבאות:
1. שאלות על גרפים ונתונים
2. בקשה לדוח למנהל בית ספר
3. שאלות על חוזקות וחולשות של בית הספר
4. שאלות כלליות על התוכנית
5. שאלות הקשורות לקבצי מידע נוספים

### הנחיות לפי סוג השאלה ###

## 1. שאלות על גרפים ונתונים ##
אם השאלה עוסקת בניתוח גרפים, התייחס למידע הבא:

סוגי הגרפים המוצגים למשתמש:
- גרף חוסן (RISC) - מראה את רמת החוסן הנפשי של בית הספר בהשוואה לממוצע ארצי וממוצע מחקרי.
- גרף מיקוד שליטה פנימי (ICI) - מראה את רמת מיקוד השליטה הפנימי של בית הספר בהשוואה לממוצע ארצי ומחקרי.
- גרף רדאר (Spider) - מראה את תפיסות הזמן השונות של בית הספר (עבר חיובי, עבר שלילי, הווה הדוניסטי, הווה פאטאלי, עתיד).

בניתוח הגרפים, התייחס ל:
- השוואה בין הערך הנוכחי לממוצעים
- מגמות בולטות
- קשרים בין המדדים השונים
- המלצות מעשיות להתערבות

## 2. דוח למנהל בית ספר ##
אם מבקשים דוח למנהל, הכן טקסט מותאם הכולל:

1. פתיחה המציגה את תכנית "הציר המנטלי" והשאלון
2. התייחסות למדדים התיאורטיים עם אזכור המאמרים המפורטים:
    - מיקוד שליטה פנימי (Nowicki & Strickland, 1973)
    - חוסן (Connor & Davidson, 2003)
    - תפיסת זמן (Zimbardo & Boyd, 1999)
3. ניתוח תוצאות בית הספר ביחס לממוצע הארצי לפי הסקאלה:
    * 0-9% מעל/מתחת = "מעט מעל/מתחת לממוצע"
    * 10-19% מעל/מתחת = "מעל/מתחת לממוצע במידה מסוימת"
    * 20%+ מעל/מתחת = "מעל/מתחת לממוצע באופן משמעותי"
4.    התייחסות חיובית למדד הגבוה ביותר
5. שאלות לחשיבה בהתאם למדד החלש ביותר
6. סיום המזמין להתבוננות ופעולה

## 3. שאלות על איפה אני ביחס לממוצע ##
אם השאלה עוסקת בחוזקות וחולשות של בית הספר, התייחס למידע הבא:

המדד שנמצא מתחת לממוצע {school_info.worst_anigma_name}
הפער מהממוצע הארצי: {school_info.worst_anigma_value*100} אחוזים
ההיגד שנמצא מתחת לממוצע: {school_info.worst_heg1_text}
ההיגד השני שנמצא מתחת לממוצע: {school_info.worst_heg2_text if hasattr(school_info, 'worst_heg2_text') else 'לא זמין'}

ספק:
- תיאור המצב הנוכחי
- דרכי טיפול והתערבות אפשריות לשיפור ההיגד החלש
- ציון לשבח של המדד החזק ביותר: {school_info.best_anigma_name}

## 4. מידע כללי על התוכנית ##
אם מבקשים מידע כללי על התוכנית, התייחס למידע הבא:

תוכנית "הציר המנטלי" מיועדת לפתח דפוס חשיבה מתפתח בקרב תלמידי חטיבות ביניים ותיכונים מהפריפריה (מדד טיפוח 6-10) לקידום קריירות היי-טק בישראל. התוכנית כוללת הכשרת אנשי חינוך, מעורבות של הנהלת בית הספר, סדנאות לפיתוח חשיבה מתפתחת וחוויות יזמיות מעשיות. התוכנית מלווה על ידי חברות טכנולוגיה מובילות.

חזון התוכנית: יצירת תמונת עתיד של הזדמנויות בהייטק ופיתוח גישות חיוביות כלפי למידה והתפתחות אישית.

קהל היעד: תלמידים בכיתות ח' ו-י' ב-93 בתי ספר במדדי טיפוח 6-10.

## 5. שאלות הקשורות לקבצי מידע נוספים ##
אם השאלה קשורה למידע המופיע בקבצים הנוספים שצוינו, השתמש במידע הרלוונטי מהקבצים האלו כדי לספק תשובה מקיפה ומדויקת. שלב את המידע מהקבצים יחד עם הידע הכללי שלך על התוכנית.



### פורמט תשובות ###
פרמט את כל תשובותיך ב-Markdown. השתמש בכותרות, רשימות, הדגשות וטבלאות כדי להפוך את התשובה לברורה ומאורגנת.

DEPRESSION AND ANXIETY 18:76 82 (2003)

Research Article![](Aspose.Words.5cef5754-8589-4286-87a9-ff460351bed3.001.png)

DEVELOPMENT OF A NEW RESILIENCE SCALE:
THE CONNOR-DAVIDSON RESILIENCE SCALE (CD-RISC)

n

Kathryn M. Connor, M.D., and Jonathan R.T. Davidson, M.D.![](Aspose.Words.5cef5754-8589-4286-87a9-ff460351bed3.002.png)

Resilience may be viewed as a measure of stress coping ability and, as such, could be an important target of treatment in anxiety, depression, and stress reactions. We describe a new rating scale to assess resilience. The Connor-Davidson Resilience scale (CD-RISC) comprises of 25 items, each rated on a 5-point scale (0 4), with higher scores reflecting greater resilience. The scale was administered to subjects in the following groups: community sample, primary care outpatients, general psychiatric outpatients, clinical trial of generalized anxiety disorder, and two clinical trials of PTSD. The reliability, validity, and factor analytic structure of the scale were evaluated, and reference scores for study samples were calculated. Sensitivity to treatment effects was examined in subjects from the PTSD clinical trials. The scale demonstrated good psychometric properties and factor analysis yielded five factors. A repeated measures ANOVA showed that an increase in CD-RISC score was associated with greater improvement during treatment. Improvement in CD-RISC score was noted in proportion to overall clinical global improvement, with greatest increase noted in subjects with the highest global improvement and deterioration in CD-RISC score in those with minimal or no global improvement. The CD- RISC has sound psychometric properties and distinguishes between those with greater and lesser resilience. The scale demonstrates that resilience is modifiable and can improve with treatment, with greater improvement corresponding to higher levels of global improvement. Depression and Anxiety 18:76 82, 2003.

- 2003 Wiley-Liss, Inc.![](Aspose.Words.5cef5754-8589-4286-87a9-ff460351bed3.003.png)

Key words: resilience; stress coping; wellbeing; posttraumatic stress disorder; anxiety; depression

INTRODUCTION

Resilience embodies the personal qualities that enable one to thrive in the face of adversity. Research over the

last 20 years has demonstrated that resilience is a multidimensional characteristic that varies with con- text, time, age, gender, and cultural origin, as well as within an individual subjected to different life circum- stances [e.g., Garmezy, 1985; Garmezy and Rutter, 1985; Rutter et al., 1985; Seligman and Csikszentmi- halyi, 2000; Werner and Smith, 1992]. One theory for this variability was developed by Richardson and colleagues, who proposed the following resiliency model [Richardson et al., 1990; Richardson, 2002]. Beginning at a point of biopsychospiritual balance (  homeostasis  ), one adapts body, mind, and spirit to current life circumstances. Internal and external stressors are ever-present and one s ability to cope

- 2003 WILEY-LISS, INC.

with these events is influenced by both successful and unsuccessful adaptations to previous disruptions. In some situations, such adaptations, or protective

Department of Psychiatry and Behavioral Sciences, Duke University![](Aspose.Words.5cef5754-8589-4286-87a9-ff460351bed3.004.png) Medical Center, Durham, North Carolina

Contract grant sponsor: Smith Kline Beecham; Contract grant sponsor: Pfizer Pharmaceuticals; Contract grant sponsor: Pure World Botanicals, Inc.; Contract grant sponsor: Organon; Con- tract grant sponsor: NIH; Contract grant number: R01 MH56656- 01A1

nCorrespondence to: Dr. Connor, Box 3812, DUMC, Durham, NC 27710. E-mail: kathryn.connor@duke.edu

Received for publication 15 September 2002; Accepted 1 April 2003

DOI: 10.1002/da.10113

Published online in Wiley InterScience (www.interscience.wiley.com).

77 Connor and Davidson

factors, are ineffective, resulting in disruption of the biopsychospiritual homeostasis. In time, response to this disruption is a reintegrative process, leading to one of four outcomes: (1) the disruption represents an oppor- tunity for growth and increased resilience, whereby adaptation to the disruption leads to a new, higher level of homeostasis; (2) a return to baseline homeostasis, in an effort to just get past or beyond the disruption; (3) recovery with loss, establishing a lower level of home- ostasis; or 4) a dysfunctional state in which maladaptive strategies (e.g., self-destructive behaviors) are used to cope with stressors. Resilience may thus also be viewed as measure of successful stress-coping ability.

The clinical relevance of resilience and related constructs has been noted previously. Maddi and Khoshaba theorized that hardiness was an index of mental health [Maddi and Khoshaba, 1994] and recent data has supported this hypothesis [Ramanaiah et al., 1999]. Tsuang [2000] has emphasized the substantial clinical implications that follow a better understanding of the forces that mould resilience. With regard to trauma and posttraumatic stress disorder (PTSD), it has been shown that hardiness contributes to protec- tion against developing chronic PTSD after combat [King et al., 1998; Waysman et al., 2001].

The growing focus on health promotion and well- being, shifting emphasis away from pathology and problem-orientation, provides an opportunity to revisit the role of resilience in health. Yet there is relatively little awareness about resilience or its importance in clinical therapeutics. Conventionally, therapeutic trials have focused more heavily on measuring morbidity, although quality of life elements are now included in many trials. A number of scales have been developed to measure resilience [Bartone et al., 1989; Wagnild and Young, 1993] or aspects of resilience [e.g., hardiness: Hull et al., 1987, Kobasa, 1979; perceived stress, Cohen et al., 1983]. However, these measures have neither been widely used nor applied to specific populations [Carlson, 2001; Mosack, 2002] and thereby lack generalizability. Of striking note, a textbook of psy- chiatric measures recently published by the American Psychiatric Association contains not a single resilience measure [American Psychiatric Association, 2000].

The need for well-validated measures of resilience that are simple to use is thus evident. While several scales have been developed, they have not gained wide acceptance and no one scale has established primacy. With these considerations in mind, the Connor- Davidson Resilience Scale (CD-RISC) was developed as a brief self-rated assessment to help quantify resilience and as a clinical measure to assess treatment response.

METHODS

SCALE DEVELOPMENT

We recently became interested in the concept of resilience as being relevant to treatment outcome in

anxiety, depression, and stress reactions. This interest arose in part from a finding that fluoxetine produced greater therapeutic benefit on stress coping than placebo in PTSD [Connor et al., 1999]. Furthermore, in reviewing the account of Sir Edward Shackleton s heroic expedition in the Antarctic in 1912 [Alexander, 1998], it was noted that the expedition s leader possessed many personal characteristics compatible with resilience and that this may perhaps have contributed to the successful survival of each member of the expedition in the face of overwhelming odds. Together, these observations prompted the authors to undertake the development of a short self-rated resilience measure.

The content of the scale was drawn from a number of sources. From Kobasa s work with the construct of hardiness [Kobasa, 1979], items reflecting control, commitment, and change viewed as challenge were included. The following features were drawn from Rutter s work [Rutter, 1985]: developing strategy with a clear goal or aim, action orientation, strong self- esteem/confidence, adaptability when coping with change, social problem solving skills, humor in the face of stress, strengthening effect of stress, taking on responsibilities for dealing with stress, secure/stable affectional bonds, and previous experiences of success and achievement (these last two features may reflect the underpinnings of resilience). From Lyons [1991], items assessing patience and the ability to endure stress or pain were included. Lastly, from Shackleton s experi- ences, it was noted that the role of faith and a belief in benevolent intervention (  good luck  ) were likely important factors in the survival of the expedition, suggesting a spiritual component to resilience. Table 1 summarizes the salient features of resilience.

With the above considerations, the CD-RISC was constructed, with the following goals in mind: to develop a valid and reliable measure to quantify

TABLE 1: Characteristics of resilient people



|Reference|Characteristic|
| - | - |
|Kobasa, 1979|View change or stress as a challenge/opportunity|
|Kobasa, 1979|Commitment|
|Kobasa, 1979|Recognition of limits to control|
|Rutter, 1985|Engaging the support of others|
|Rutter, 1985|Close, secure attachment to others|
|Rutter, 1985|Personal or collective goals|
|Rutter, 1985|Self-efficacy|
|Rutter, 1985|Strengthening effect of stress|
|Rutter, 1985|Past successes|
|Rutter, 1985|Realistic sense of control/having choices|
|Rutter, 1985|Sense of humor|
|Rutter, 1985|Action oriented approach|
|Lyons, 1991|Patience|
|Lyons, 1991|Tolerance of negative affect|
|Rutter, 1985|Adaptability to change|
|Current|Optimism|
|Current|Faith|

79 Connor and Davidson

TABLE 2: Content of the Connor-Davidson Resilience Scale



|Item no.|Description|
| - | - |
|1|Able to adapt to change|
|2|Close and secure relationships|
|3|Sometimes fate or God can help|
|4|Can deal with whatever comes|
|5|Past success gives confidence for new challenge|
|6|See the humorous side of things|
|7|Coping with stress strengthens|
|8|Tend to bounce back after illness or hardship|
|9|Things happen for a reason|
|10|Best effort no matter what|
|11|You can achieve your goals|
|12|When things look hopeless, I don t give up|
|13|Know where to turn for help|
|14|Under pressure, focus and think clearly|
|15|Prefer to take the lead in problem solving|
|16|Not easily discouraged by failure|
|17|Think of self as strong person|
|18|Make unpopular or difficult decisions|
|19|Can handle unpleasant feelings|
|20|Have to act on a hunch|
|21|Strong sense of purpose|
|22|In control of your life|
|23|I like challenges|
|24|You work to attain your goals|
|25|Pride in your achievements|

resilience, to establish reference values for resilience in the general population and in clinical samples, and to assess the modifiability of resilience in response to pharmacologic treatment in a clinical population.

The CD-RISC contains 25 items, all of which carry a 5-point range of responses, as follows: not true at all (0), rarely true (1), sometimes true (2), often true (3), and true nearly all of the time (4). The scale is rated based on how the subject has felt over the past month. The total score ranges from 0 100, with higher scores reflecting greater resilience. The individual items comprising the scale are listed in Table 2.

STUDY SAMPLE

Subjects were drawn from the following study samples: a random-digit dial based general population sample [i.e., non help-seeking (Group 1, n¼577; included subjects with complete data only); primary care outpatients (Group 2, n¼139); psychiatric out- patients in private practice (Group 3, n¼43); subjects in a study of generalized anxiety disorder (GAD; Group 4, n¼25); and subjects in two clinical trials of PTSD (Group 5, n¼22; Group 6, n¼22)]. Of note, subjects in Group 6 are included only for between- group diagnostic comparisons and in the assessment of pre- to post-treatment change. Each study protocol was approved by the Duke University Medical Center

Institutional Review Board and all subjects provided informed consent.

Demographic characteristics of Groups 1 5 (n¼ 806) were as follows: female 65% (n¼510), male 35% (n¼274); white 77% (n¼588), non-white 23% (n¼181); and mean (sd) age 43.8 (15.3) years (n¼763). Some missing data occurred for all of these compar- isons, which explains why the figures do not total 806 in the various comparisons (e.g., data were not always available for gender, ethnic status, etc.).

DATA ANALYSIS

The data were analyzed with the following objec- tives: (1) to establish reference scores for the CD-RISC and to assess whether scores were affected by clinical category or demographic factors, (2) to assess the reliability and validity of the scale, (3) to assess the factor composition of the CD-RISC in the general population, and (4) to assess the extent to which CD- RISC scores can change with clinical improvement with treatment and over time.

Given that several of the samples were not normally distributed, median CD-RISC scores were calculated for each group and pairwise comparisons were per- formed using the Wilcoxon Rank Sum test, with Po.05 being regarded as significant. A Bonferroni correction was used for multiple comparisons to derive the z score. Of note, mean CD-RISC scores are also presented for clinical reference. A Kruskal-Wallis test was used for multiple group comparisons, with the expectation that degrees of resilience would be lower in psychiatric outpatients than in the general population or primary care patients.

Descriptive statistics were used to characterize CD-RISC scores in the full sample by gender, ethnicity, and age. Analysis of variance was used to analyze categorical variables (e.g., gender and ethnicity) and correlation with the continuous measure of age.

The reliability and validity of the scale were assessed as follows. Test retest reliability was examined in subjects from Groups 4 and 5 in whom no clinical change was noted between two consecutive visits. Internal consistency was evaluated by using Cronbach s alpha for the total and item-total scores in subjects from Group 1. Convergent validity was assessed in various groups by correlating the CD-RISC with measures of hardiness [Kobasa Hardiness Scale; Koba- sa et al., 1979], perceived stress [Perceived Stress Scale (PSS-10); Cohen et al., 1983], and stress vulnerability [Stress Vulnerability Scale (SVS); Sheehan et al., 1990], as well as measures of disability [Sheehan Disability Scale(SDS); Sheehan et al., 1983] and social support [Sheehan Social Support Scale (SSSS); Sheehan, 1990]. Divergent validity was assessed by correlating CD- RISC scores with the Arizona Sexual Experience Scale [ASEX; McGahuey et al., 2000] in subjects from Group 4.

81 Connor and Davidson

An exploratory factor analysis using an ORTHO- MAX rotation was conducted by using data from the general population sample (Group 1).

The effects of time and treatment on resilience were assessed by comparing pre- and post-treatment CD- RISC scores in treatment responders and non-respon- ders in the clinical trial samples (Groups 4, 5, and 6) by using a repeated measures analysis of variance (ANO- VA), with response as the grouping variable and time as the repeated measure. Response was defined by a Clinical Global Improvement (CGI-I; Guy; 1976) score of 1 (very much improved) or 2 (much improved).

RESULTS

CD-RISC SCORES BY CLINICAL CATEGORY AND DEMOGRAPHIC GROUP

Mean (sd) and median (1st, 4th quartile) CD-RISC scores were calculated for the full sample (Groups 1 5) and for the individual study groups (Table 3). Results of pairwise comparisons are listed in Table 4 and significant differences were found for the following groups: general population (Group 1) vs. each of the other groups, primary care (Group 2) vs. GAD (Group 4), and primary care vs. PTSD (Groups 5 and 6). Statistical significance was obtained in the

overall multiple comparison model (w2 ¼142.80, df¼5, Po.0001).

Mean (sd) scores were also calculated by demo- graphic grouping, and no differences were observed in the characteristics evaluated. A gender comparison revealed a mean score of 77.1 (16.3) for women and 77.2 (14.2) for men (P¼.63). Mean CD-RISC scores by racial group were as follows: white subjects, 77.4 (14.8) and non-white subjects, 76.7 (18.1) (P ¼ .83). The mean (sd) age of the full sample was 43.8 (15.4) years, and no correlation was found between age and CD- RISC score (Pearson r ¼.06, n.s.).

RELIABILITY AND VALIDITY

Internal consistency. Cronbach s a for the full scale was 0.89 for Group 1 (n¼577) and item-total correlations ranged from 0.30 to 0.70 (Table 5).

TABLE 3: Connor-Davidson Resilience Scale scores by study group



||Group|||Median|
| :- | - | :- | :- | - |
|Study group|no.|N|Mean (sd)|(1st, 4th Q)|
|General population|1|577|80\.4 (12.8)|82(73, 90)|
|Primary care|2|139|71\.8 (18.4)|75 (60, 86)|
|Psychiatric outpatients|3|43|68\.0 (15.3)|69(57, 79)|
|GAD patients|4|24|62\.4 (10.7)|64\.5 (53, 71)|
|PTSD patients|5|22|47\.8 (19.5)|47(31, 61)|
||6|22|52\.8 (20.4)|56 (39, 61)|

GAD ¼ generalized anxiety disorder; PTSD ¼ posttraumatic stress disorder.

TABLE 4: Pairwise comparisons of Connor-Davidson Resilience Scale scores



||||Statistically|
| :- | :- | :- | - |
|Groupn|Mean rank difference|Critical rank difference|significant differencenn|
|Group1 vs.||||
|Group2|114\.70|66\.36|Yes|
|Group3|193\.80|111\.02|Yes|
|Group4|290\.50|146\.31|Yes|
|Group5|362\.80|152\.56|Yes|
|Group6|329\.70|152\.56|Yes|
|Group2 vs.||||
|Group3|79\.10|122\.55|No|
|Group4|175\.80|155\.24|Yes|
|Group5|248\.10|161\.15|Yes|
|Group6|215\.00|161\.15|Yes|
|Group3 vs.||||
|Group4|96\.70|178\.95|No|
|Group5|169\.00|184\.09|No|
|Group6|135\.90|184\.09|No|
|Group4 vs.||||
|Group5|72\.30|207\.29|No|
|Group6|39\.20|207\.29|No|
|Group5 vs|||.|
|Group6|33\.10|211\.75|No|

nGroup 1¼general population; Group 2¼primary care; Group 3¼psychiatric outpatients; Group 4¼GAD clinical trial subjects; Groups 5 and 6¼PTSD clinical trial subjects.

nn ao.05; Bonferonni correction used to derive z score; z¼2.94 GAD ¼ generalized anxiety disorder; PTSD ¼ posttraumatic stress disorder.

Test retest reliability. Test retest reliability was assessed in 24 subjects from the clinical trials of GAD (Group 4) and PTSD (Group 5) in whom little or no clinical change was observed from time 1 to time 2. The mean (sd) CD-RISC scores at time 1 [52.7 (17.9)] and time 2 [52.8 (19.9)] demonstrated a high level of agreement, with an intraclass correlation coefficient of 0.87.

Convergent validity. CD-RISC scores were posi- tively correlated with the Kobasa hardiness measure in psychiatric outpatients (Group 3, n ¼ 30; Pearson r ¼ 0.83, Po.0001). Compared to the Perceived Stress Scale (PSS-10), the CD-RISC showed a significant negative correlation (Group 3, n ¼ 24; Pearson r ¼ 0.76, Po.001), indicating that higher levels

of resilience corresponded with less perceived stress. The Sheehan Stress Vulnerability Scale (SVS) was similarly negatively correlated with the CD-RISC (Spearman r ¼ 0.32, Po.0001) in 591 subjects from the combined sample. This result also indicates that higher levels of resilience correspond to lower levels of perceived stress vulnerability. As a measure of disability, the CD-RISC demonstrated a

` `Connor and Davidson

TABLE 5: Item-total correlations and rotated factor pattern for the Connor-Davidson Resilience Scale

Factor (Eigenvalue)

Item Item-total correlation[^1] 1 (7.436) 2 (1.563) 3 (1.376) 4 (1.128) 5 (1.073)![](Aspose.Words.5cef5754-8589-4286-87a9-ff460351bed3.005.png)

83 Connor and Davidson

24 0.61 0.70870 0.14250 12 0.62 0.63998 0.22255 11 0.62 0.62497 0.11656 25 0.56 0.60385 0.04385 10 0.52 0.59601 0.17001 23 0.59 0.55800 0.32628 17 0.70 0.40381 0.35512 16 0.62 0.39651 0.37804 20 0.40 0.08774 0.67393 18 0.58 0.29395 0.57585 15 0.57 0.29967 0.53047

6 0.58 0.11507 0.52564

7 0.55 0.14586 0.46703 19 0.64 0.17227 0.43428 14 0.64 0.25215 0.42942

1 0.55 0.07334 0.08512

4 0.64 0.07074 0.19156

5 0.69 0.26961 0.37932

2 0.36 0.23482 0.08203

8 0.67 0.34423 0.34073 22 0.63 0.21396 0.12493 13 0.62 0.15177 0.03725 21 0.64 0.36495 0.15438

3 0.30 0.01386 0.01460

9 0.40 0.12061 0.24612

0.04339 0.19253 0.01779 0.20851 0.05018 0.11083 0.13206 0.21732 0.06408 0.14600 0.22531 0.11798 0.16642 0.03336 0.10776 0.00758 0.12202 0.04681 0.12714 0.35236 0.00409 0.26274 0.18958 0.03547 0.05234 0.06238 0.23265

` `0.01006 0.19034 0.08147 0.04440 0.23134 0.01552

0\.40443 0.12267 0.03711 0.30584 0.01699 0.27429 0.27115 0.39728 0.01199 0.26572 0.36228 0.10734

0\.75885 0.10762 0.03223 0.61921 0.40002 0.02811 0.55332 0.09561 0.08239

0\.53775 0.14060 0.31552 0.43996 0.16462 0.04038 0.09219 0.77469 0.02935 0.20513 0.54772 0.40077

` `0.02278 0.53186 0.32889 0.15972 0.15786 0.77820

` `0.00029 0.05145 0.73662

` `Connor and Davidson

time  CGI group effect (F ¼ 7.70; df 2, 29; P¼.002) were noted.

DISCUSSION

The CD-RISC has been tested in the general population, as well as in clinical samples, and demonstrates sound psychometric properties, with good internal consistency and test retest reliability. The scale exhibits validity relative to other measures of stress and hardiness, and reflects different levels of resilience in populations that are thought to be differentiated, among other ways, by their degree of resilience (e.g., general population vs. patients with anxiety disorders). Clinical improvement with even short-term pharmacotherapy in patients with PTSD, a condition with a propensity toward heightened vulner- ability to the effects of stress, is accompanied by up to 25% or greater increase in resilience, depending upon level of global improvement. Furthermore, subjects with PTSD who showed very much improvement attained CD-RISC scores close to the mean of the general population. To the authors  knowledge, this is the first demonstration that increased resilience, as operationally defined, can be associated with a pharmacologic intervention.

Three areas can be identified where the CD-RISC might be usefully applied. A number of investigators have considered possible biologic aspects of resilience. For example, resilience is characterized by a response profile to major stress in which low baseline catecho- laminergic activity is transformed into high catechola- mine production, along with increased tissue-specific response (e.g., glucose levels) and an attenuated cortisol response [Dienstbier, 1991]. Gormley [2000] has opined that SSRI drugs may facilitate this process in depressive, obsessive-compulsive, and panic disorders but provides no actual evidence in support of his assertion. The authors have shown previously that fluoxetine has such an effect in PTSD [Connor et al., 1999]. It is also possible that relationships exist between resilience and central serotonergic function [Andrews et al., 1988; Healey and Healey, 1996]. Thus, the CD-RISC might prove useful in studies of the biology of resilience.

A second application of the scale could be in clinical practice with contemporary resiliency interventions. Such interventions explore resilience qualities with individuals, identify them, and nurture them [Rak, 2002]. In focusing on strengths and positive attributes, an individual tends to become engaged in more adaptive pursuits, and their problems tend to diminish. The CD-RISC is compatible with such interventions, as an aid to identifying resilient characteristics but also in assessing response to the intervention.

A third potential application of the scale might be in studies designed to investigate adaptive and maladap- tive strategies for coping with stress, and as a tool to assist in screening individuals for high-risk, high-stress

activities or occupations. For example, resilience (hardiness) was identified as a strong predictor of protection from PTSD in a cohort of Vietnam veterans [King et al., 2000]. Lyons [1991] noted a strengthening effect of extreme trauma in many trauma survivors and a scale such as the CD-RISC might be useful in studying such individuals.

The authors note several limitations of this report. The CD-RISC is a wave two resilience measure, using the scheme outlined by Richardson [Richardson, 2002], assessing characteristics of resi- lience, and does not assess the resiliency process or provide information about the theory of resilience. While divergent validity was demonstrated, the mea- sure used to assess divergence (ASEX, a measure of sexual functioning) was weakly, albeit nonsignificantly, correlated with CD-RISC and this finding most likely reflects the heterogeneity of the resilience construct. The CD-RISC has not been validated against an objective (i.e., behavioral or third party) measure, or against biological measures of resilience, such as neuropeptide Y responses to extreme stress [Morgan et al., 1999]. The authors also recognize that it is possible to perform well in one area in the face of adversity (e.g., work) but to function poorly in another (i.e., interpersonal relationships). Would such a person be considered resilient? Furthermore, resilience may either be a determinant of response or an effect of exposure to stress. Assessment of such directional factors was not undertaken in this report. A prospective study would be able to inform whether resilience pre- dated exposure to trauma, protected against post- trauma problems, or, if through circumstances, some survivors developed further resilience post-trauma.

CONCLUSIONS

The CD-RISC is a brief, self-rated measure of resilience that has sound psychometric properties. By using the CD-RISC, the findings of this study demonstrate the following: resilience is quantifiable and influenced by health status (i.e., individuals with mental illness have lower levels of resilience than the general population); resilience is modifiable and can improve with treatment; and greater improvement in resilience corresponds to higher levels of global improvement. The CD-RISC could have potential utility in both clinical practice and research.

Acknowledgements We thank Larry Tupler and Erik Churchill for their statistical support and Dr. George Parkerson for facilitating access to primary care subjects.

REFERENCES

Alexander C. 1998. The Endurance: Shackleton s legendary antarctic

expedition. New York: Alfred A. Knopf.

American Psychiatric Association. 2000. Handbook of psychiatric measures. Washington, DC: American Psychiatric Association.

85 Connor and Davidson

Andrews W, Parker G, Barrett E. 1998. The SSRI antidepressants:

exploring their  other   possible properties. J Affect Disorder 49:141 144.

Bartone PT, Ursano R, Wright K, Ingraham L. 1989. The impact of

military air disaster on the health of assistance workers. J Nerv Mental Dis 177:317 328.

Carlson DJ. 2001. Development and validation of a College

Resilience Questionnaire. Dissertation Abstracts International, A

(Humanities and Social Sciences). vol 62, Jan 2001, 20025. Cohen S, Kamarck T, Mermelstein R. 1983. A global measure of

perceived stress. J Health Soc Behav 24:386 396.

Connor KM, Sutherland SM, Tupler LA, Churchill LE,

Malik ML, Davidson JRT. 1999. Fluoxetine in posttraumatic stress disorder: a randomized, placebo-controlled trial. Br J Psych 175:17 22.

Dienstbier RA. 1991. Behavioral correlates of sympathoadrenal

reactivity: the toughness model. Med Sci Sports Med 23:846 852. Garmezy N. 1985. Stress resistant children: the search for protective

factors. In: Recent research in developmental psychopathology,

book suppl number 4 to J Child Psychol Psych. Oxford: Pergamon

Press.

Garmezy N, Rutter M. 1985. Acute stress reactions. In: M Rutter, L

Hersob, editors. Child and adolescent psych: modern approaches. Oxford: Blackwell.

Gormley N. 2000. Is neuroticism a modifiable risk factor for

depression? Ir J Psych Med 17:41 42.

Healey D, Healey H. 1998. The clinical pharmacologic profile of

reboxetine: does it involve the putative neurobiological substrates of wellbeing? J Affect Disord 51:313 322.

Hull JG, Van Treuren RR, Virnelli S. 1987. Hardiness and health: a

critique and alternative approach. J Personality Soc Psychol 53:518 530.

King LA, King DW, Fairbank JA, Keane TM, Adams GA. 1998.

Resilience-recovery factors in post-traumatic stress disorder among female and male Vietnam veterans: hardiness, postwar social support, and additional stressful life events. J Personality Soc Psychol 74:420 434.

Kobasa SC. 1979. Stressful life events, personality, and health: an

inquiry into hardiness. J Personality Soc Psychol 37:1 11.

Lyons J. 1991. Strategies for assessing the potential for positive

adjustment following trauma. J Traumatic Stress 4:93 111.

Maddi SR, Khoshaba DM. 1994. Hardiness and mental health. J Pers

Assess 63:265 274.

McGahuey CA, Gelenberg AJ, Laukes CA, Moreno FA, Delgado PL.

2000\. The Arizona Sexual Experience Scale (ASEX): reliability and validity. J Sex Marital Therapy 26:25 40.

Morgan CA III, Wang S, Southwick SM, Rasmusson A, Hazlett G,

Hauger RL, Charney DS. 2000. Plasma neuropeptide-Y concen- trations in humans exposed to military survival training. Biol Psychiatry 47:902 909.

Mosack KE. 2002. The development and validation of the R-PLA: a

resiliency measure for people living with HIV/AIDS (immune deficiency). Dissertation Abstracts International: Section B: the Sciences and Engineering. vol 62, Mar 2002, 3844.

Rak CF. 2002. Heroes in the nursery: three case studies in resilience.

J Clin Psychol 58:247 260.

Ramanaiah NV, Sharpe JP, Byravan A. 1999. Hardiness and major

personality factors. Psychol Rep 84:497 500.

Richardson GE. 2002. The metatheory of resilience and resiliency.

J Clin Psychol 58:307 321.

Richardson GE, Neiger B, Jensen S, Kumpfer K. 1990. The

resiliency model. Health Education 21:33 39.

Rutter M. 1985. Resilience in the face of adversity: protective factors

and resistance to psychiatric disorders. Br J Psych 147:598 611. Seligman MEP, Csikszentmihalyi M. 2000. Positive psychology. Am

Psychologist 55:5 14.

Sheehan DV. 1983. The Anxiety Disease. New York: Bantam Books. Sheehan DV, Raj AB, Harnett Sheehan K. 1990. Is buspirone

effective for panic disorder? J Clin Psychopharmacol 10:3 11. Tsuang MT. 2000. Genes, environment and mental health wellness.

Am J Psychiatry 157:489 491.

Wagnild GM, Young HM. 1993. Development and psychometric

validation of the Resilience Scale. J Nurs Meas 1:165 178. Waysman M, Schwarzwald J, Solomon Z. 2001. Hardiness: an

examination of its relationship with positive and negative long-

term changes following trauma. J Traumatic Stress 14:531 548. Werner E, Smith R. 1992. Overcoming odds: high risk children from

birth to adulthood. Ithaca, NY: Cornell University Press.

[^1]: Calculated from standardized variables; Chronbach s a¼0.93.

    significant negative correlation with the Sheehan Disability Scale (SDS) (Pearson r ¼ 0.62, Po.0001) in psychiatric patients (Groups 3 and 4, n ¼ 40). Lastly, the Sheehan Social Support Scale (SSS) correlated significantly with the CD-RISC in 589 subjects (Spearman r ¼ ;0.36, Po.0001). Thus, greater resilience, as expected, is associated with less disability and greater social support.

    influences. The factor pattern for the scale is presented in Table 5.

    SENSITIVITY TO THE EFFECTS OF TREATMENT

    In subjects with PTSD (Groups 5 and 6), non- responders (n ¼ 30) had mean (sd) pre and post treatment scores of 54.0 (16.5) and 54.9 (18.8), respectively. Among responders (n ¼ 19), mean pre- and post-treatment scores were 56.8 (18.4) and

    Discriminant validity. The CD-RISC was not significantly correlated with the ASEX at baseline (Group 4, n ¼ 23; r ¼ 0.34, P ¼.11) or at endpoint (n ¼ 19; r ¼ 0.30, P ¼ .21).

    68\.9 (19.8), respectively. Significant effects were

    observed for time (F ¼ 17.36; df 1, 47; Po.0001) and for time  response category (F ¼ 12.87; df 2, 47; P o 001), indicating that CD-RISC scores increased significantly with overall clinical improvement.

    FACTOR ANALYSIS

    Analysis of data from subjects in the general population sample yielded five factors whose eigenva- lues were, respectively, 7.47, 1.56, 1.38, 1.13, and

    Greater improvement was noted in CD-RISC score in proportion to the degree of global clinical improvement. For example, in subjects with a CGI-I score of 1 (n ¼ 7), there was a mean increase of 19.9 (26.6%) in the CD-RISC score, compared to an increase of 7.9 (16.2%) for those with a CGI-I score of 2 (n ¼ 7), and a deterioration of 0.8 (1.3%) in those with a CGI-I of 3 or more (minimal or no improve- ment; n ¼ 18) (F ¼ 3.42, df 2, Po.05). Significant effects for time (F ¼ 14.82; df2, 29; P ¼ .006) and for

    1\.07. These factors could be broadly interpreted in

    the following manner. Factor 1 reflects the notion of personal competence, high standards, and tenacity. Factor 2 corresponds to trust in one s instincts, tolerance of negative affect, and strengthening effects of stress. Factor 3 relates to the positive accept- ance of change, and secure relationships. Factor 4 was related to control and Factor 5 to spiritual
    
    
    
    *Journal  oj  Consulting  and Clinical  Psychology ![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.001.jpeg)*1973,  Vol.  40,  No.  1,  148-154

A  LOCUS  OF  CONTROL  SCALE  FOR  CHILDREN1

STEPHEN NOWICKI, JR.,2  AND  BONNIE  R. STRICKLAND *Emory  University*

The  present  study  presents reliability  and  validity  evidence concerning a  new measure of a generalized locus of  control  for  children. Construction procedures leading  to  the  final  40-item  scale  are  described.  Preliminary  work  showed that  scores  were  not  related  to  social  desirability  or  intelligence  test  scores but  were  related  to  achievement.  Continued  research  with  the  instrument conducted  over  a  wide  range  of  subject  populations has  provided  additional construct  validation  across  variables  such  as  popularity,  ability  to  delay gratification,  and prejudice.

Reinforcement  has  long  been  recognized as a major determinant of behavior; however, as  Rotter  (1966)  noted,  the  effect  of  rein- forcement  is not a simple stamping in process but  "depends  on whether  or  not  the  person perceives  a  causal  relationship  between  his own  behavior  and  the  reward  [p.  1]." This perception  may  vary  in  degree  from  indi- vidual to individual and even within the same individual  over time  and  situations.  The  de- velopment  of  a  belief  of behavior-reinforce- ment  contingencies  is  likely  a  particularly important  influence  as a growing child  learns appropriate  social  and  personal  behavior. Within  a  social  learning  theory,  Rotter (1966)  has described  a dimension of locus of control  of  reinforcement.  He  remarked  that

When  a  reinforcement is  perceived  by  the  subject as  following  some action  of  his  own  but  not  being entirely  contingent  upon  his  action,  then,  in  our culture,  it  is  typically  perceived  as  the  result  of luck,  chance, fate,  as  under the  control of  powerful others,  or  as  unpredictable  because  of  the  great complexity  of  the  forces  surrounding  him.  When the  event  is  interpreted  in  this  way  by  an  indi- vidual,  we  have  labeled  this  a  belief  in  external control.  If  the  person  perceives  that  the  event  is contingent  upon  his  own  behavior or  his  own  rela- tively  permanent  characteristics,  we  have  termed this  a belief  in internal  control  [p.  1].

Considerable  research  on  this  dimension has  been  accomplished  with  adults  (Joe,

1 Extended  reports of this  research were presented at  the  annual meeting  of  the  American Psychologi- cal Association in Washington, D.C., September 1971. Also,  some  parts  of  the  reported  research  were supported  by  funds  available  from  the  Emory  Uni- versity  Research Committee.

2 Requests  for  reprints  should  be  sent  to  Stephen Nowicki,  Jr.,  Department  of  Psychology,  Emory University,  Atlanta,  Georgia 30322.

1971;  Lefcourt,  1966,  1971;  Rotter,  1966). The  major  adult  measure of locus  of  control is a  modification of  the  early  instruments of Phares  (1957)  and  James  (1957)  and  was constructed by Rotter and his associates  (see Rotter,  1966). A complete description  of this scale  with  reliability  and  validation  data  is presented  by  Rotter  (1966).  Although  the Rotter  scale  has  been  criticized with  regard to  its  appropriateness  for  blacks  (Gurin, Gurin,  Lao,  &  Beattie,  1969),  nonetheless, this scale with a few other measures has been used  in  well  over  100 studies  over  the  last IS  years.

Considering  the  extensive body of research with  adults,  it  seems  appropriate  to  extend an  investigation of the locus of control  vari- able  to  children.  There  is  ample  reason  to believe  that  this  variable  is of significant in- fluence on  children's  behavior.  For  instance, Coleman,  Campbell,  Hobson,  McPartland, Mood, Weinfeld, and York (1966), in a study of  almost  half  a  million  youngsters  across the  United  States,  found  that  a  belief  in destiny  was  a  major  determinant  in  school achievement. They  concluded that  this  pupil attitude  factor had a  stronger relationship to achievement  than  all  other  school  factors together.

Of  course, research  in  this  area  is  depen- dent  on  a  reliable  and  valid  measure,  and there  have  been  a  number  of  attempts  to measure  the locus of control  of  reinforcement dimension  in  children.  Bialer  (1961)  devel- oped  a  paper-and-pencil  measure  consisting of  23 items answered yes or  no, while  Battle and  Rotter  (1963)  constructed  a  projective

device  called  the  Children's  Picture  Test of

148

Locus OF CONTROL SCALE FOR CHILDREN 149

internal-External  Control.  Research  with![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.002.jpeg)

these measures  suggests that locus  of control

becomes  more  internal  with  age  and  that

internality  is  associated  with  higher  social

class  and  white  culture  placement  as  op-

posed  to Negro  and  lower socioeconomic sta-

tus. From these suggestive findings with mea-

sures of a generalized locus of control measure,

Crandall,  Crandall  and  Katkovsky  (1965)

attempted  to  develop  a  more  specific  mea- sure  aimed  at  assessing  children's  beliefs

in  reinforcement  in  intellectual-academic-

achievement  situations.  With  the  Intellec-

tual  Achievement  Responsibility  Question-

naire,  they  found  internal  beliefs  to  be

moderately related  to intelligence, ordinal po-

sition,  and  size  of  family  but  inconsistently

related  to social class. The scale was predic- tive of younger girls' and older boys'  achieve- ment  scores.

In  all,  however,  each  of the  measures  of a child's locus of  control  of reinforcement falls short in one way or another.  Bialer's  (1961) scale suffers from reliability and format short- comings.  For  example, the  scale  had  a  split- half  reliability  of  .49 in a  study by  Schaffer, Strickland,  and  Uhl  (1969).  Moreover,  the basic  format  of  the  Bialer  scale  has  almost half  of  the  items consecutively keyed  in  one direction—an  open  invitation  for  response style to significantly affect  scores.  Battle  and Rotter's  (1963)  measure  is  difficult  to  ad- minister to large  groups,  and  there is incom- plete  reliability  information  available.  The Crandall  et  al.  (1965)  scale  is  specifically constructed  for the academic  rather than  the general situation, and its forced-choice format may be  difficult  for younger and  duller Ss.

Consequently,  there  is  a  clear  need  for  a reliable  instrument  for  researchers  to  use  to study  the  effects  of  a  generalized  locus  of control  orientation  of  a  child's  behavior.  A

lidity  as  measured  by  relationships  with achievement,  intelligence,  socioeconomic class, and parental  education level is also presented.

The  following  relationships  were hypothe- sized  as  necessary  for  a  measure  to  be  con- sidered  an  appropriate  assessment  of  locus of  control,  *(a)*  Scores  will  become  more internal with  increasing age;  *(b)*  scores will be  related  to  achievement  with  internals achieving more than externals; and  *(c)*  scores will not be significantly related to measures of social  desirability  or  intelligence.

METHOD

The  Nowicki-Strickland  Locus  of Control scale is a paper-and-pencil measure consisting of 40 questions that  are  answered  either  yes  or  no  by  placing  a mark  next  to  the  question. This  form  of  the mea- sure  derives  from  work  which  began  with  a  large number of items *(N =* 102), constructed on the basis of  Rotter's  definition  of  the  internal-external con- trol  of  reinforcement dimension. The  items  describe reinforcement  situations  across  interpersonal  and motivational  areas  such  as  affiliation,  achievement, and  dependency.  School  teachers  were  consulted  in the construction  of items. The goal was to make  the items readable  at  the fifth-grade level, yet appropri- ate  for  older  students.  These  items  along  with Rotter's  description  of  the  locus  of  control dimen- sion  were then given  to  a  group  of  clinical psychol- ogy  staff  members  *(N —* 9),  who  were  asked  to answer  the  items in  an  external  direction. Items  on which there was not  complete agreement among the judges were dropped. This left  59 items, which made up  the  preliminary  form  of  the  test.  The  59-item form  of  the  test  was  then  given  to  a  sample of

TABLE 1

MEANS  AND  STANDARD  DEVIATIONS  OP  NOWICKI- STRICKLAND Locus or  CONTROL SCORES IOR MALES     AND  FEMALES  IN  EXPERIMENTAL  SAMPLE:

GRADES  3  THROUGH  12

Males Females

*M SD S* no. *M SD* 5 no.

Locus OF CONTROL SCALE FOR CHILDREN 

methodologically sound  measure  would  allow

researchers  to  describe better the  nomothetic

network  of relationships  surrounding this  di-

mension.  Thus,  the  major  purpose  of  the .present  study  was  to  produce  a  reliable,

methodologically  precise  measure  of  general-

ized  locus  of  control  of  reinforcement  that

could  be  group  administered  to  a  wide  age

range  of  children.  Evidence  of  construct  va-

3  17.97 4.67
3  18.44 3.58
3  18.32 4.38
3  13.73 5.16
3  13.15 4.87
3  14.73 4.35
3  13.81 4.06
3  13.05 5.34
3  12.48 4.81
3  11.38 4.74

44 17.38 3.06 55

59 18,80 3.63 55

40 17.00 4.03 41

45 13.32 4.58 43

65 13.94 4.23 52

75 12.29 3.58 34

43 12.25 3.75 44

68 12.98 5.31 57

37 12,01 5.15 53

39 12.37 5.05 48

151 STEPHEN  NOWICKI, JR., AND BONNIE  R.  STRICKLAND

TABLE  2![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.003.jpeg)

NOWICKI-STRICKLAND  SCALE  AND ITEM-TOTAL  CORRELATIONS  WITH  THAT ITEM  MlSSING FOR 5 IN  THE THIRD,  SEVENTH,  AND ELEVENTH  GRADES OP THE SAMPLE

` `STEPHEN  NOWICKI, JR., AND BONNIE  R.  STRICKLAND

Item

1. Do you believe that most problems will solve themselves if you just don't fool with them? (Yes)»'b
1. Do you believe that you can stop yourself from catching a cold ? (No)
1. Are some kids just born lucky?
1. Most of the time do you feel that getting good grades means a great deal to you? (No)
1. Are you often blamed for things that just aren't your fault? (Yes)b
1. Do you believe that if somebody studies hard enough he or she can pass any subject?  (No)
1. Do you feel that most of the time it doesn't pay to try hard because things never turn out right anyway?  (Yes)a>b
1. Do you feel that if things start out well in the morning that it's going to be a good day no matter what you do? (Yes)
1. Do you feel that most of the time parents listen to what their chil- ren have to say? (No)"'b
1. Do you believe that wishing can make good things happen ? (Yes)a

1 1 . When you get punsihed does it usually seem its for no good reason at

all? (Yes)b

12. Most of the time do you find it hard to change a friend's (mind) opin- ion? (Yes)b
12. Do you think that cheering more than luck helps a team to win ? (No)
12. Do you feel that it's nearly impossible to change your parent's mind about anything? (Yes)a'b

IS. Do you believe that your parents should allow you to make most of

your own decisions? (No)

16. Do you feel that when you do something wrong there's very little you can do to make it right? (Yes)"'b
16. Do you believe that most kids are just born good at sports? (Yes)"'b
16. Are most of the other kids your age stronger than you are? (Yes)8
16. Do you feel that one of the best ways to handle most problems is just not to think about them?  (Yes)»'b
16. Do you feel that you have a lot of choice in deciding who your friends are? (No)
16. If you find a four leaf clover do you believe that it might bring you good luck?  (Yes)
16. Do you often feel that whether you do your homework has much to do with what kind of grades you get? (No)
16. Do you feel that when a kid your age decides to hit you, there's little you can do to stop him or her? (Yes)"'b
16. Have you ever had a good luck charm?  (Yes)
16. Do you believe that whether or not people like you depends on how you act?  (No)
16. Will your parents usually help you if you ask them to? (No)
16. Have you felt that when people were mean to you it was usually for no reason at all? (Yes)"'b
16. Most of the time, do you feel that you can change what might hap- pen tomorrow by what you do today? (No)b
16. Do you believe that when bad things are going to happen they just are going to happen no matter what you try  to do to stop them? (Yes)«'b

30,  Do you think that kids can get their own way if they just keep try-

ing?  (No)

31. Most of the time do you find it useless to try to get your own way at home?  (Yes)'-b

Male Female

3 7 11 3 7 11

.153 *.219* .107 .323 .165 .140 .140 *.219* .065 *.398* .176 .154 .281 *A97* .224 .431 .244 .501

.146 .101 .244 *.019* .171 .270 .204 .167 .225 .007 *A091* .617

.385 .026 .520 .263 .075 .205 .165 *.390 A09* .343 .328 .402 .ISO .077 .307 .215 .040 .095

.222 .330 .240 .484 .056 *.192* .126 *.059* .083 .236 .285 *.032*

.366 .324 .456 .244 .263 .225

.113 *.229* .208 *.039* .272 *.396* .348 .362 *.298* .017 *.397* .352

.456 .161 .417 .175 *.396* .436 .004 .234 *.298* .172 *.329* -.012

.078 *.490* .306 .415 .568 .243 .284 .322 .136 .347 .130 .170 .227 .337 .381 .175 .480 .151

.368 .262 .506 *.329* .367 *.239* .086 .256 .143 .356 .385 *.192 .139* .172 .300 .186 .285 .342 *.U9* .003 .034 .065 *.009* .156

.273 *.049* .150 .177 *,294* .464 .086 .163 .047 .075 .077 .037

.028 .016 .150 .148 .113 .252 .230 .140 .366 .218 .000 .166

.314 .144 .306 .500 .178 .165 .116 .152 .100 .283 .302 .415

.367 .322 .455 .443 .608 .564 .154 .208 *.129* .203 .005 *A29* .164 .446 .530 .211 .342 .448

Locus  OF  CONTROL  SCALE  FOR  CHILDREN* 

Table  *2—(Continued)![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.004.jpeg)*

Locus  OF  CONTROL  SCALE  FOR  CHILDREN* 

Item

32. Do you feel that when good things happen  they happen because of hard work? (No)
32. Do you feel that when somebody your age wants to be your enemy there's little you can do to change matters? (Yes)»'b

34, Do you feel that it's  easy to get friends to do what you want them

to? (No)

35. Do you usually feel that you have little to say about what you get to eat at home? (Yes)»'b
35. Do you feel that when someone doesn't like you there's little you can do about it?  (Yes)"'b
35. Do you usually feel that it's almost useless to try in school because most other children are just plain smarter than you are? (Yes)\*'b
35. Are you the kind of person who believes that planning ahead makes things turn out better? (Yes)a'b
35. Most of the time, do you feel that you have little to say about what your family decides to do? (Yes)a'b
35. Do you think it's  better  to be smart than  to be lucky?  (No)

Male Female

3 7 11 3 7 11

.423 .318 .281 .290 .263 .245 .052 .336 .559 .310 .517 .226 .101 .099 .181 .276 .462 .600 .143 .353 .344 .289 .384 .275 .122 .295 .416 .132 .473 .360 .456 .205 .625 .341 .308 .157 .158 .343 .096 .531 .264 .458

.203 .269 .405 .343 .648 .365 .039 .273 .349 .435 .333 .316

Locus  OF  CONTROL  SCALE  FOR  CHILDREN* 

6 Items selected for abbreviated scale for Grades  1-6. b Items selected for abbreviated  scale for grades  7-12.

Locus  OF  CONTROL  SCALE  FOR  CHILDREN* 

children  (#=152)  ranging  from  the  third  through ninth grades. Means for this testing  ranged from  19.1 *(SD =* 3,86)  at  the third  grade to  11.65  *(SD =* 4.26) at ninth  grade,  with higher  scores associated with  an external  orientation.  Controlling  for  IQ,  internals performed  significantly  better  than  externals  on achievement  test  scores  (i = 3.78,  d/ = 48).  Test- retest  reliabilities  for  a  6-week  period  are  .67  for the 8-11-year-old group  *(N =* 98)  and  .75 for  those in  the  12-15-year-old  group  (JV = 54).

Item  analysis  was computed  to  make a  somewhat more  homogeneous  scale  and  to  examine  the  dis- criminative  performance of  the  items.  The  results of this analysis, as well as comments from  teachers  and pupils  in  the  sample  led  to  the  present  form  of  the scale  consisting  of  40 items.

*Administration*

The  40-item  scale  was  then  administered  to  a large  number  of  children  ranging  from  the  third through  the  twelfth  grade  to  obtain  reliability  esti- mates,  demographic  measures,  and  construct  valid- ity  information.  The  sample  consisted  of  1,017 mostly  Caucasian  elementary  and  high  school  stu- dents  in  four  different  communities. All schools were in  a  county  bordering  a  large  metropolitan  school system.

Socioeconomic data  were  obtained  from  the school records,  and  Hollingshead  (1957)  Index  of  Social Position  rankings indicated  that  although  the  lower level  occupations  were  somewhat  overrepresented, all  levels,  except  the  very  highest  one,  were  well represented.  Intelligence  test  scores  for  males  and females  in  Grades  3-10  ranged  from  means  of  101 td  106 as measured  by  Otis-Lennon  scales,  with  no

Significant  differences  across  groups.

Initial  research  showed  that  first  and  second graders  had  some  difficulty  with  the  preliminary instrument, so it  was  decided  to  concentrate  on  the third  through  twelfth  grades  in  this  investigation. This  is  not  to  say  that  the  test  is  not  appropriate for  first  and  second  graders,  but  rather  the  present study emphasizes  the  performance  of somewhat  older students.  The  5s  were  told  that  the  examiner  was gathering information concerning attitudes  and  opin- ions  of  different  aged  students  to  see how  they  dif- fered  depending  on  the  age  of  the  students,  and they were assured that  their responses would be kept confidential.  Testing  took  place midway  through  the spring  quarter  of  1969 at  the  schools.  The  examiner read  each  item  aloud  twice,  asking  5s  to  check  yes or  no  on  the  test  sheet. This  oral  presentation  was chosen  to  make  the  items  more  understandable  and easier  to  follow.

RESULTS  AND DISCUSSION

Table  1 presents  the  means and  standard deviations  of  the  Nowick-Strickland  scale scores  for  males  and  females  at  each  grade level;  it  shows  that  students'  responses became more internal with  age.

The  Nowicki-Strickland  scale  items  are presented  in  Table  2.  Biserial  item  correla- tions  are presented  for males and  females  at the third, seventh, and eleventh  grades. It  is evident  from  this  table  that  the  item-total relationships are  moderate but  consistent for

all ages.

153 STEPHEN  NOWICKI,  JR.,  AND BONNIE  R.  STRICKLAND

Estimates  of  internal  consistency  via  the split-half method, corrected by the Spearman- Brown  ![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.005.jpeg)formula  are  *r —* .63  (for Grades 3,  4, 5);  r=.68  (for  Grades  6,  7,  8);  *r = .U* (for  Grades  9,  10,  11);  and  *r = M*  (for Grade  12). These reliabilities  are satisfactory in  light  of  the  fact  that  the  items  are  not arranged according to difficulty.  Since the test is additive and  the items are  not comparable, the  split-half  reliabilities  tend  to  underesti- mate the true internal consistency of the scale.

Test-retest  reliabilities  sampled  at  three grade levels, 6 weeks apart,  were  .63 for  the third  grade,  .66 for  the  seventh  grade,  and .71  for  the  tenth  grade.

Correlations  with  an  abbreviated  form  of the  Children's  Social  Desirability  Scale (Crandall  et  al.,  1965)  were  computed  for male and  female  subjects within each  grade, and  locus of  control  scores were not  signifi- cantly  related  to social  desirability.

The  relationships between locus of control, socioeconomic  level,  and  achievement  are presented in Tables 3 and  4.

With  regard  to  socioeconomic  level  (see Table  3),  all  correlations are  negative, with 6 of the  16 correlations reaching the  .10 level of significance. Most of the significant correla- tions  are  present  in  the  male  group.  It  is tentatively  concluded  that  internality  is  re- lated  significantly  to  higher  occupational

level, especially  for males.

In  Table  4,  a  clear  relationship  between locus  of  control  and  achievement  scores emerges. All of the correlations are negative—

TABLE 3

CORRELATIONS BETWEEN  NOWICKI-STRICKLAND Locus or  CONTROL SCORES AND OCCUPATIONAL

LEVEL FOR GEADES 3 THROUGH 10

Num- Female Num- Grade Male ber ber

3  -.141 27 -.072 22
3  -.277\* 27 -.044 31
3  -.389\*\* 36 -.052 35
3  -.059 30 -.464\*\* 26 7 -.327\*\* 35 -.229 41
8  -.195 25 -.068 48
8  -.206 33 -.247\* 39

10 -.163 27 -.301\* 33

**. .**

**\*\* *p  <* .05.**

**TABLE  4**

CORRELATIONS BETWEEN NOWICKI-STRICKLAND Locus or CONTROL AND ACHIEVEMENT TEST SCORES

FOR 5s  IN ELEMENTARY AND SECONDARY GRADES

Grade Male Num- Female Num-

ber ber

3  -.284\* 34 -.178 27
3  -.118 50 -.195 31
3  -.398\*\*\* 42 -.254\* 45
3  -.272\* 33 -.112 32 7 -.335\*\* 35 -.306\* 34

10 -.442\*\*\* 49 -.034 38 12 -.451\*\*\* 38 -.004 48

**\*\* *t  < .05.* \*\*\* *j>  <*  .01.**

again with most of the significant correlations present  in  the  male groups.  Female  achieve- ment  does  not  seem  to  be  predictable  from scores on the  Nowicki-Strickland scale.  Only fifth-  and  seventh-grade  females  show  a trend  toward  a  significant  relationship  with achievement  scores.

The  correlations  were  also  computed  for parental level  of education  and  locus of con- trol.  Although all  correlations were negative, only  2 of  the  12 correlations  reached  signifi- cance,  and  both  of  these  are  in  the  male group.  The  lack  of  significant  findings  may be  the  result  of  using  the  highest  level  of education  for  the  analysis,  regardless  of whether  it  was the  mother's  or  the  father's. This  procedure  may  add  a  source  of  error for locus of control scores that may be  related to  the  father's  but  not  to  the  mother's educational  level.

On  the  basis  of  the  item-total  correlations and  item  variance  estimates  for  each  item of  the  Nowicki-Strickland  scale,  those  items working the  best were identified.  The  analy- ses computed for each  grade were then com- bined  into  primary  and  secondary  groups. The  primary group consisted  of 5s  from  the third  through  the  sixth  grades,  while  the secondary  group  consisted  of  5s  from  the seventh  through  the  twelfth  grades. The  re- sults of these analyses were used  to  construct shorter  yet  reliable  versions  of  the  40-item scale.  The  two  revised  scales  consist  of  20

and  21  items,  respectively,  using  the  items

155 STEPHEN  NOWICKI, JR.,  AND BONNIE  R.  STRICKLAND

that  discriminate  the  best  for  the  two  age groups. ![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.006.jpeg) These  new  revision  should  be  used with caution until more reliability  and valid- ity  information can  be  gathered.  However, there is every reason to believe from the item analysis  (on over  1,000 students)  that  these revisions  should  be  a  usable,  reliable,  and quick  measure  of  a  generalized  locus  of control  of  reinforcement  for  different-aged children. -  In  addition,  the  Nowicki-Strickland  scale

; has been  revised  and adopted  for use with -college  and  adult  subjects  by  changing  the

word  "kids" to  "people" and  deleting  items about  parents.  This  was  done  to  allow  for direct  comparison  between  the  responses  of adults and children. The low level of reading skill  required  and  the  lack  of  politically tinged  items  make it  appropriate  for use in a wide number  of populations.

Last,  to  investigate  the  construct  valida- tion of the Nowicki-Strickland scale, its  rela- tion  to  other  measures  of  locus  of  control

i were  examined.  It  was expected  that  there would be significant but not high correlations between  the  measures.  The  relation  to  the

"Intellectual Achievement Responsibility scale was examined first. In a sample of black third $T= 182)  and seventh graders  *(N =*  171),

there  were  significant  correlations  with  the IH- but not with the I— scores  (for the third

•grade,  r = .31,  £<.01;  for  the  seventh /grade, *r=* .51, *p <* .01). Next, the correlation

.with  the  Bialer-Cromwell score  (see  Bialer, 1961) was also significant *(r* =  .41, *p <* .05) in  a  sample  of  white  children  *(N =* 29) aged 9-11. Finally, the relation  between the Rotter  and  the  Nowicki-Strickland  adult

scales  was  also  significant  in  two  studies with  college  students  *(N* =  76,  *r* =  .61, *p <* .01;  *N -*  46, *r -*  .38,  *p <* .01).  These relations suggest added  support  for  the con- struct  validation  of  the  Nowicki-Strickland scale.

Since the construction of the scale, a num- ber  of studies across a diverse range of sub- ject  populations  have  been  completed.  Gen- erally,  the  results  are  clearly  supportive of the utility and validity of the new instrument, which  appears  to be related  to  a variety of behaviors. Nowicki  (1971)  and Nowicki and Roundtree  (1971)  found  significant  relation-

ships  between internal locus of  control  and higher  grade point  averages  but  not  intelli- gence for twelfth graders and college students. For  seventh  graders,  Roberts  (1971)  found significant correlations between internal  locus of  control and  reading achievement for both sexes  and  a  significant  relationship  with mathematics  achievement  for  males but  not for  females.  With  third-grade  students,  he found  no  significant  relationships  between the  school  achievement  measures  and  locus of  control,  but  he  did  find  significant  rela- tionships  between  internal  scores  and  self- esteem as measured by  the Coopersmith and Piers-Harris  instruments for both males and females.

Ludwigsen  and  Rollins  (1971)  manipu- lated  two  cue  conditions  and  found  among white sixth graders that internals, as assessed by  the  Nowicki-Strickland scale,  performed better  than  externals  on a visual recognition task and a self-initiated cue group did better than a group for whom verbal cues were sup- plied.  For  high  socioeconomic  Ss,  only  cue suorce  differentiated  performance.  In  the lower  socioeconomic  group,  however,  cue source, locus of control, and  their interaction were all determining factors. They also found the Ss of low socioeconomic status to be more external  than  high  socioeconomic Ss. Aside from school-related variables, other behavioral correlates  of  internality  on  the  Nowicki- Strickland scale include delay of gratification for  white elementary school subjects  (Strick- land,  1971,  1972),  involvement  in  extracur- ricular  activities  for  twelfth-grade  females, and popularity  (as  determined by number of votes for class president)  for both elementary and  secondary school males (Nowicki, 1971; Nowicki & Barnes,  1971; Nowicki & Round- tree,  1971). Additionally, Duke and Nowicki

(1971) have completed research that suggests that  a belief in external control of  reinforce- ment, as assessed  by  the  Nowicki-Strickland scale,  among  white  children  is  related  to prejudice against blacks, at least in a  South- ern population.  Broadly, these  research find- ings suggest  that, particularly  for males,  an internal  score  on  the  Nowicki-Strickland scales  is  significantly  related  to  academic competence,  to  social  maturity,  and  appears

157 STEPHEN  NOWICKI, JR.,  AND BONNIE  R.  STRICKLAND

to  be  a  correlate  of  independent,  striving, self-motivated ![](Aspose.Words.d813df02-2726-49c6-9ef7-fe6d771ace65.007.jpeg) behavior.

If  a  generalized  belief  in  internal  control of  reinforcement is  related  to  a  number of achievement and competence behaviors as well as tolerance toward other races, then an obvi- ous  question  arises  as  to  whether  internal- external beliefs can be modified. Nowicki and Barnes  (1971)  administered  the  Nowicld- Strickland scale to 291 seventh-, eighth-, and ninth-grade males, predominantly black,  from inner-city  ghetto  schools  as  they  entered  a structured  camp situation in which the  coun- selors  sought  to  make  clear  the connection between  the  camper's  behavior  and  resultant rewards. As hypothesized, campers were  sig- nificantly more internal  on a  readministration of the Nowicki-Strickland scale at  the  end of their camp session,  usually  1 week.

Obviously,  there  are  a  number of compli- cating  variables  to  consider,  including  age, sex, race,  and socioeconomic status,  when in- vestigating  a generalized  expectancy  of  rein- forecement  with  children.  Nonetheless,  the locus  of  control  dimension  appears  to  be  a variable  of  significant  impact  in  relation  to children's  behaviors,  and  the  Nowicki- Strickland scale appears to be an  appropriate instrument  for  assessing  this  variable.  Con- tinued  research,  particularly  as regards ante- cedent conditions, such as parental  character- istics  and  child-rearing  practices  that  lead to  the  development of  a  generalized expect- ancy of locus of control, is clearly  warranted.

REFERENCES

BATTLE, E.  S., & ROTTER, J.  B. Children's  feelings of

personal  control  as  related  to  social  class  ethnic

group. *Journal  of  Personality,*  1963, 3,  482-490. BIALER,  I.  Conceptualization  of  success  and  failure

in mentally  retarded and  normal  children.  *Journal*

*of  Personality,* 1961, 29, 303-320.

COLEMAN,  J.  S.,  CAMPBELL,  E.  Q.,  HOBSON,  C.  J.,

McPARTLAND, J.,  MOOD, A.  M.,  WEINFIEID,  F.  D.,

&  YORK,  R.  T.  *Equality  of  educational  opportu- nity.*  (Superintendent  of  Documents,  Catalog  No. FS5.238:38001)  Washington,  D.C.:  United  States Office  of Education,  1966.

CRANDALL, V. C.,  CRANDALL, V. J., & KATKOVSKY, W.

A  children's  social  desirability  questionnaire.  *Jour-*

*nal  of  Consulting Psychology,*  1965, 29,  27-36. DUKE, M.  P.,  & NOWICKI, S. Perceived  interpersonal

distance  as  a  function  of  the  subjects'  locus  of

control  and  the  race  and  sex  of  stimuli  in  ele-

mentary and high school children. Paper  presented

at  the annual  meeting of the Southeastern  Psycho- logical  Association,  Miami  Beach,  Florida,  April- May  1971.

GURIN,  P.,  GURIN,  G.,  LAO, R.,  &  BEATTIE,  M.

Internal-external  control  of  the  motivational  dy- namics  of  Negro  youth.  *Journal  of  Social  Issues,* 1969, 25,  29-S3.

HOLLINGSHEAD,  A.  Two-factor  index  of  social  posi-

tion.  New Haven,  Conn.:  Author,  1957.  (Mimeo) JAMES,  W.  H.  Internal  versus  external  control  of

reinforcement  as  a  basic  variable  in  learning

theory.  Unpublished  doctoral  dissertation,  Ohio

State  University, 1957.

JOE,  V.  A.  Review  of  the  internal-external  control

construct  as  a  personality  variable.  *Psychological Reports,*  1971, 28, 619-640.

LEFCOURT, H.  M.  Internal versus external control of

reinforcement:  A  review.  *Psychological  Bulletin,* 1966, 65,  206-220.

LEPCOURT, H.  M.  *Internal  versus external control  of*

*reinforcement  revisited.*  (Research  Rep.  No.  27)

Ontario,  Canada:  University  of  Waterloo, 1971. LUDWIGSEN,  K.,  & ROLLINS,  H.  Recognition  of  ran-

dom  forms  as  a  function  of  cue,  perceived  locus

of  control,  and  socio-economic level.  Paper  pre-

sented  at  the  annual meeting  of  the  Southeastern

Psychological  Association, Miami  Beach,  Florida, -

April-May,  1971.

NOWICKI,  S. Achievement  and  popularity  as  related

to  locus  of  control  across  different  age  groups.

Unpublished  manuscript, Emory  University,  1971. NOWICKI,  S.,  &  BARNES,  J.  Effects  of  a  structured

camp  experience  on  locus  of  control  in  children.

*Journal  of  Genetic Psychology,*  1973, in  press. NOWICKI,  S.,  JR.,  &  ROUNDTREE,  J.  Correlates  of

locus  of  control in  a  secondary school  population.

*Developmental  Psychology,*  1971,  4, 477-478. PHARES,  E.  J.  Expectancy  changes  in  skill  and

change situations. *Journal  of  Abnormal  and Social*

*Psychology,*  1967, 54, 339-342.

ROBERTS,  A.  The  self-esteem  of  disadvantaged  third

and  seventh  graders.  Unpublished  doctoral  dis- sertation,  Emory  University,  1971.

ROTTER,  J.  B.  *Social  learning  and  clinical  psychol-*

*ogy.* New York:  Prentice-Hall,  1954.

ROTTER,  J.  B.  Generalized  expectancies  for  internal

versus  external  control  of  reinforcement.  *Psycho-*

*logical Monographs,*  1966, 80  (1, Whole No.  609). SCHAFFER,  S.,  STRICKLAND,  B.,  & UHL, N.  The  rela-

tionship  of individual  difference  measures  to  socio-

economic  level  and  to  discrimination  learning.

Paper  presented  at  the  annual  meeting  of  the

Southeastern  Psychological  Association,  New  Or-

leans,  February-March  1969.

STRICKLAND,  B.  R.  Delay  of  gratification and  inter-

nal  locus  of  control  in  children. *Journal  of  Con- sulting  and  Clinical Psychology,*  in  press.

STRICKLAND, B.  R.  Delay  of gratification  as  a  func-

tion  of  race  of  the  experimenter.-  *Journal  of Personality  and  Social  Psychology,*  1972,  22, 108-112.

(Received  September  30,  1971)



"""
