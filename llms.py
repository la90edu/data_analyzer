import os
from openai import OpenAI
from dotenv import load_dotenv

# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# קבלת ה-API key מהמשתנים והגדרת הלקוח
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai_client = OpenAI(api_key=api_key)
else:
    openai_client = OpenAI()  # יתכן שיעבוד אם יש API key בסביבה

def get_openai_response(prompt, system_prompt, history, graph_data, stream=False):
    """
    קבלת תשובה ממודל השפה של OpenAI
    
    Args:
        prompt: השאלה של המשתמש
        system_prompt: הוראות המערכת למודל
        history: היסטוריית השיחה
        graph_data: נתוני הגרפים המוצגים
        stream: האם להשתמש בסטרימינג של התשובה
    
    Returns:
        תשובת המודל או אובייקט סטרימינג
    """
    # יצירת תקציר של נתוני הגרפים
    graph_summary = ""
    if graph_data["selected_school"]:
        graph_summary += f"הנתונים שלהלן מתייחסים לבית הספר: {graph_data['selected_school']}\n\n"
    
    if graph_data["risc"] is not None:
        graph_summary += f"נתוני גרף חוסן:\n"
        graph_summary += f"ערך נוכחי: {graph_data['risc']['value']:.2f}\n"
        graph_summary += f"ממוצע ארצי: {graph_data['risc']['global_avg']:.2f}\n"
        
    if graph_data["ici"] is not None:
        graph_summary += f"נתוני גרף מיקוד שליטה פנימי (ICI):\n"
        graph_summary += f"ערך נוכחי: {graph_data['ici']['value']:.2f}\n"
        graph_summary += f"ממוצע ארצי: {graph_data['ici']['global_avg']:.2f}\n"
        
    if graph_data["spider"] is not None:
        graph_summary += f"נתוני תפיסות זמן:\n"
        for category, values in graph_data["spider"].items():
            formatted_category = category.replace("future_", "").replace("_past", "").replace("_present", "")
            graph_summary += f"קטגוריה: {formatted_category}\n"
            graph_summary += f"  ערך נוכחי: {values['current']:.2f}\n"
            graph_summary += f"  ממוצע ארצי: {values['global']:.2f}\n"
    
    # הוספת תקציר הגרפים לפרומפט המשתמש
    user_prompt = f"""history: {history}

current prompt: {prompt}

נתוני הגרפים המוצגים בדאשבורד:
{graph_summary}
"""
    
    try:
        if stream:
            # החזר אובייקט סטרימינג שניתן לאיטרציה
            response_stream = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.05,
                stream=True
            )
            return response_stream
        else:
            # החזרת תשובה מלאה (ללא סטרימינג)
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.05
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"אירעה שגיאה בעת התקשורת עם OpenAI: {str(e)}"

def get_graph_explanation(graph_type, graph_data, school_info=None):
    """
    מקבלת הסבר על גרף ספציפי ממודל השפה בסטרימינג
    
    Args:
        graph_type: סוג הגרף (risc, ici, spider)
        graph_data: הנתונים של הגרף
        school_info: אובייקט SchoolInfo אם קיים
    
    Returns:
        הסבר טקסטואלי מפורט על הגרף ומשמעותו
    """
    if graph_type == "risc":
        prompt = f"""
        הסבר בבקשה את נתוני גרף החוסן הבאים:
        ערך נוכחי: {graph_data['value']:.2f}
        ממוצע ארצי: {graph_data['global_avg']:.2f}
        
        מה המשמעות של הנתונים האלה? האם הערך גבוה או נמוך ביחס לממוצע? מה זה אומר על בית הספר?
        התייחס להשלכות החינוכיות והחברתיות של התוצאות. תן המלצות להמשך בהתבסס על הנתונים.
        """
    elif graph_type == "ici":
        prompt = f"""
        הסבר בבקשה את נתוני גרף מיקוד שליטה פנימי (ICI) הבאים:
        ערך נוכחי: {graph_data['value']:.2f}
        ממוצע ארצי: {graph_data['global_avg']:.2f}
        
        מה המשמעות של הנתונים האלה? האם הערך גבוה או נמוך ביחס לממוצע? מה זה אומר על בית הספר?
        התייחס להשלכות החינוכיות והחברתיות של התוצאות. תן המלצות להמשך בהתבסס על הנתונים.
        """
    elif graph_type == "spider":
        prompt = """
        הסבר בבקשה את נתוני גרף תפיסות הזמן (גרף העכביש) המוצג.
        מהי המשמעות של כל אחד מהממדים? אילו ממדים בולטים לטובה ואילו לרעה?
        מהן ההשלכות החינוכיות והפסיכולוגיות של התוצאות?
        תן המלצות להמשך בהתבסס על הנתונים.
        """
        
        # הוספת פירוט על הקטגוריות בגרף העכביש אם יש נתונים
        if graph_data:
            prompt += "\n\nנתוני הקטגוריות השונות:\n"
            for category, values in graph_data.items():
                formatted_category = category.replace("future_", "").replace("_past", "").replace("_present", "")
                if "current" in values and "global" in values:
                    prompt += f"- {formatted_category}: ערך נוכחי {values['current']:.2f}, ממוצע ארצי {values['global']:.2f}\n"
    
    # הוספת מידע על בית הספר אם קיים
    if school_info and hasattr(school_info, 'school_name'):
        prompt += f"\nהנתונים מתייחסים לבית הספר: {school_info.school_name}"
    
    system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
    עליך להסביר את משמעות הנתונים בשפה פשוטה .
    ושאל שאות את המנהל שיכולות לעודד אותו לחשוב על שיפור המצב שלו כגון  'איך כיום בית הספר מעודד תלמידים להרגיש בעלות על המעשים שלהם?', 'האם יש מקומות נוספים שהיית משלב יכולת לקחת בעלות על הצלחות או כשלונות ומידת ההשפעה האישית של התלמיד עליהן?             .
    
    מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
    
    מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
    
    תפיסות זמן (גרף עכביש) - מציג חמישה ממדים:
    1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
    2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
    3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
    4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
    5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
    
    אל תתן המלצות או מסקנות. אלא רק תן שאלות חשיבה למנהל בית הספר שיכולות לעודד אותו לחשוב על שיפור המצב שלו.
    לדוגמה: 'איך כיום בית הספר מעודד תלמידים להרגיש בעלות על המעשים שלהם?', 'האם יש מקומות נוספים שהיית משלב יכולת לקחת בעלות על הצלחות או כשלונות ומידת ההשפעה האישית של התלמיד עליהן?'
    """
    
    try:
        # קריאה למודל השפה לקבלת הסבר מסכם
        response_stream = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            stream=True
        )
        
        # יצירת מקום להצגת ההסברים בזמן אמת
        full_explanation = ""
        
        # לולאה על חלקי התשובה בסטרימינג והצגה בזמן אמת
        for chunk in response_stream:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content
                if content:
                    full_explanation += content
        
        # החזרת ההסבר המלא
        return full_explanation
        
    except Exception as e:
        # במקרה של שגיאה, החזר הסבר כללי והודעת שגיאה
        error_msg = f"לא הצלחנו לייצר הסבר אוטומטי. שגיאה: {str(e)}"
        
        # הסבר ברירת מחדל לפי סוג הגרף
        if graph_type == "risc":
            return "חוסן (RISC): מודד את היכולת של התלמידים להתמודד עם אתגרים ומצבי לחץ. ציון גבוה מעיד על יכולת התמודדות טובה יותר."
        elif graph_type == "ici":
            return "מיקוד שליטה פנימי (ICI): מודד את האמונה של אדם שהוא שולט בחייו ולא גורמים חיצוניים. ציון גבוה מעיד על תחושת מסוגלות עצמית חזקה יותר."
        elif graph_type == "spider":
            return "גרף תפיסות זמן: מציג את החלוקה של תפיסות הזמן השונות (עבר שלילי/חיובי, הווה דטרמיניסטי/הדוניסטי, עתיד). איזון נכון בין התפיסות חשוב להתנהגות בריאה והצלחה לימודית."
        else:
            return "לא הצלחנו לייצר הסבר אוטומטי לגרף זה."