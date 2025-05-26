import class_school_info

"""
Module to generate summaries comparing school metrics to the national average
"""

def interpret_delta_value(delta_value):
    """
    Interprets a delta value according to the scale:
    0: No difference from national average
    10: Slightly higher than national average
    20: Significantly higher than national average
    -10: Slightly lower than national average
    -20: Significantly lower than national average
    
    Args:
        delta_value: The delta value to interpret
        
    Returns:
        String interpretation of the delta value
    """
    # Debug log to help understand what values are received
    print(f"DEBUG: Interpreting delta value: {delta_value} of type {type(delta_value)}")
    
    # Check for None value first
    if delta_value is None:
        print("DEBUG: Delta value is None, returning default")
        return "לא ניתן לקבוע (נתון חסר)"
    
    try:
        # Try to convert to int if it's not already
        if not isinstance(delta_value, int):
            try:
                delta_value = int(float(delta_value))
                print(f"DEBUG: Converted delta value to {delta_value}")
            except (ValueError, TypeError) as e:
                print(f"DEBUG: Could not convert delta value: {e}")
        
        if delta_value == 0:
            return "בדומה לממוצע הארצי"
        elif delta_value == 10:
            return "גבוה במקצת מהממוצע הארצי"
        elif delta_value == 20:
            return "גבוה משמעותית מהממוצע הארצי"
        elif delta_value == 30:
            return "גבוה באופן יוצא דופן מהממוצע הארצי"
        elif delta_value == -10:
            return "נמוך במקצת מהממוצע הארצי"
        elif delta_value == -20:
            return "נמוך משמעותית מהממוצע הארצי"
        elif delta_value == -30:
            return "נמוך באופן יוצא דופן מהממוצע הארצי"
        else:
            # For any other value, give a more descriptive message
            print(f"DEBUG: Delta value {delta_value} did not match any standard case")
            if delta_value > 0:
                return f"גבוה מהממוצע הארצי (ערך {delta_value})"
            elif delta_value < 0:
                return f"נמוך מהממוצע הארצי (ערך {delta_value})"
            else:
                return "בדומה לממוצע הארצי"
    except (ValueError, TypeError) as e:
        print(f"ERROR interpreting delta value: {e}")
        return "לא ניתן לקבוע"

def get_improvement_questions(worst_metric, worst_statement):
    """
    Generates thought-provoking questions based on the school's weakest areas
    
    Args:
        worst_metric: The name of the school's weakest metric
        worst_statement: The worst statement/response from students
        
    Returns:
        List of thought-provoking questions
    """
    questions = []
    
    # Questions based on the weakest metric
    metric_questions = {
        "מיקוד שליטה פנימי": [
            "כיצד בית הספר יכול לעודד את התלמידים לקחת יותר אחריות אישית על הלמידה והתוצאות שלהם?",
            "אילו פעילויות או שינויים בסביבת הלמידה יכולים לחזק אצל התלמידים את האמונה ביכולתם להשפיע על העתיד שלהם?"
        ],
        "חוסן": [
            "כיצד בית הספר יכול לפתח אצל התלמידים כלים להתמודדות טובה יותר עם אתגרים וקשיים?",
            "אילו מנגנוני תמיכה נוספים ניתן להציע לתלמידים כדי לחזק את החוסן הנפשי שלהם?"
        ],
        "תפיסת עבר מעכבת": [
            "כיצד ניתן לעזור לתלמידים להתמודד עם חוויות עבר שליליות ולא לתת להן להשפיע על ההווה?",
            "אילו פעילויות יכולות לסייע לתלמידים לפתח נרטיב חיובי יותר לגבי העבר שלהם?"
        ],
        "עבר כתשתית חיובית": [
            "כיצד ניתן לעודד תלמידים לזהות חוויות חיוביות מהעבר כבסיס להתפתחות?",
            "איך אפשר לחזק אצל התלמידים את היכולת ללמוד מהעבר באופן בונה?"
        ],
        "דטרמינסטיות": [
            "כיצד ניתן לחזק בקרב התלמידים את התפיסה שהם יכולים להשפיע על העתיד שלהם?",
            "אילו פעילויות יכולות להפחית את התחושה שהעתיד כבר נקבע מראש?"
        ],
        "סיפוק מיידי": [
            "כיצד ניתן לפתח בקרב התלמידים יכולת דחיית סיפוקים וחשיבה לטווח ארוך?",
            "איך אפשר לחזק אצל התלמידים את ההבנה שהשקעה לטווח ארוך משתלמת יותר מסיפוק מיידי?"
        ],
        "תפיסת עתיד": [
            "כיצד ניתן לעזור לתלמידים לפתח תמונת עתיד חיובית וברורה יותר?",
            "אילו כלים ניתן להקנות לתלמידים כדי שיוכלו לתכנן ולהגשים את מטרותיהם העתידיות?"
        ]
    }
    
    # General questions in case the specific metric is not found
    general_questions = [
        "אילו תוכניות או פעילויות יכולות לחזק את הנקודות החלשות שזוהו בבית הספר?",
        "כיצד ניתן לרתום את הצוות החינוכי ואת התלמידים יחד למאמץ לשיפור המדדים הפסיכולוגיים שנמצאו נמוכים?"
    ]
    
    # Add metric-specific questions if available
    if worst_metric in metric_questions:
        questions.extend(metric_questions[worst_metric])
    else:
        questions.extend(general_questions)
    
    # If we don't have enough questions, add some based on the worst statement
    if len(questions) < 2 and worst_statement:
        questions.append(f"בהתייחס להיגד \"{worst_statement}\", אילו פעילויות יכולות לחזק את ההבנה והמודעות של התלמידים בנושא זה?")
    
    # Return only the first two questions
    return questions[:2]

def generate_school_summary(school_info):
    """
    Generates a comprehensive summary of school performance compared to national average
    
    Args:
        school_info: SchoolInfo object containing metrics and delta values
        
    Returns:
        String with formatted summary
    """
    # Create dictionary to store metrics and their interpretations
    metrics = {
        "מיקוד שליטה פנימי (ICI)": interpret_delta_value(school_info.ici_delta_present),
        "חוסן (RISC)": interpret_delta_value(school_info.risc_delta_present),
        "תפיסת עבר מעכבת": interpret_delta_value(school_info.future_negetive_past_delta_present),
        "עבר כתשתית חיובית": interpret_delta_value(school_info.future_positive_past_delta_present),
        "דטרמינסטיות": interpret_delta_value(school_info.future_fatalic_present_delta_present),
        "סיפוק מיידי": interpret_delta_value(school_info.future_hedonistic_present_delta_present),
        "תפיסת עתיד": interpret_delta_value(school_info.future_future_delta_present)
    }
    
    # Generate strength and weakness sections with color indicators
    strengths = []
    weaknesses = []
    
    # Function to get color based on interpretation
    def get_color_for_interpretation(interpretation):
        if "גבוה באופן יוצא דופן" in interpretation:
            return "#1b5e20"  # Dark green
        elif "גבוה משמעותית" in interpretation:
            return "#2e7d32"  # Medium green
        elif "גבוה במקצת" in interpretation:
            return "#43a047"  # Light green
        elif "נמוך באופן יוצא דופן" in interpretation:
            return "#b71c1c"  # Dark red
        elif "נמוך משמעותית" in interpretation:
            return "#d32f2f"  # Medium red
        elif "נמוך במקצת" in interpretation:
            return "#e53935"  # Light red
        else:
            return "#424242"  # Grey for neutral
    
    # Create colored metric items
    colored_metrics = []
    for metric, interpretation in metrics.items():
        color = get_color_for_interpretation(interpretation)
        colored_metrics.append(
            f'<li><strong>{metric}:</strong> <span style="color: {color}; font-weight: bold;">{interpretation}</span></li>'
        )
        
        if "גבוה" in interpretation:
            strengths.append(
                f'<li><strong>{metric}:</strong> <span style="color: {color}; font-weight: bold;">{interpretation}</span></li>'
            )
        elif "נמוך" in interpretation:
            weaknesses.append(
                f'<li><strong>{metric}:</strong> <span style="color: {color}; font-weight: bold;">{interpretation}</span></li>'
            )
    
    # Generate improvement questions
    questions = get_improvement_questions(school_info.worst_anigma_name, school_info.worst_heg1_text)
    
    # Format the summary with HTML styling
    summary = f"""
<div style="direction: rtl; text-align: right; font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
    <h1 style="color: #1565c0; text-align: center; border-bottom: 2px solid #1565c0; padding-bottom: 10px;">סיכום ביצועי בית הספר בהשוואה לממוצע הארצי</h1>

    <div style="background-color: white; padding: 15px; border-radius: 8px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h2 style="color: #1565c0; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px;">סקירה כללית</h2>
        <p style="margin-bottom: 10px;">בהשוואה לממוצע הארצי, בית הספר מציג את התוצאות הבאות:</p>
        <ul style="list-style-type: none; padding-right: 15px;">
            {"".join(colored_metrics)}
        </ul>
    </div>

    <div style="display: flex; gap: 20px; margin-top: 20px;">
        <div style="flex: 1; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #2e7d32; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px;">תחומי חוזק</h2>
            {f'<ul style="list-style-type: none; padding-right: 15px;">{"".join(strengths)}</ul>' if strengths else '<p style="color: #757575;">לא נמצאו תחומי חוזק משמעותיים בהשוואה לממוצע הארצי.</p>'}
        </div>

        <div style="flex: 1; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #c62828; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px;">תחומים לשיפור</h2>
            {f'<ul style="list-style-type: none; padding-right: 15px;">{"".join(weaknesses)}</ul>' if weaknesses else '<p style="color: #757575;">לא נמצאו תחומים לשיפור משמעותיים בהשוואה לממוצע הארצי.</p>'}
        </div>
    </div>

    <div style="background-color: #ffebee; padding: 15px; border-radius: 8px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 4px solid #c62828;">
        <h2 style="color: #c62828; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px;">בעיה מרכזית</h2>
        <p>בית הספר מתמודד עם קושי מיוחד בתחום <strong style="color: #c62828;">{school_info.worst_anigma_name}</strong>.</p>
        <p>ההיגד שקיבל את התוצאה החלשה ביותר הוא:</p>
        <div style="background-color: white; padding: 10px; border-radius: 5px; margin: 10px 0; border-right: 3px solid #c62828;">
            <p style="font-style: italic;">"{school_info.worst_heg1_text}"</p>
        </div>
    </div>

    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 4px solid #1565c0;">
        <h2 style="color: #1565c0; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px;">שאלות למחשבה ושיפור</h2>
        <ol style="padding-right: 20px;">
            <li style="margin-bottom: 10px;"><strong>{questions[0]}</strong></li>
            <li style="margin-bottom: 10px;"><strong>{questions[1]}</strong></li>
        </ol>
    </div>

    <div style="margin-top: 20px; font-size: 0.9em; color: #757575; text-align: center;">
        <p>* הערכים מוצגים בהשוואה לממוצע הארצי. ירוק מסמל תוצאות גבוהות מהממוצע, ואדום מסמל תוצאות נמוכות מהממוצע.</p>
    </div>
</div>
"""
    
    return summary

def generate_improved_school_summary(school_info):
    """
    Generates a comprehensive and visually appealing summary of school performance compared to national average
    
    Args:
        school_info: SchoolInfo object containing metrics and delta values
        
    Returns:
        String with formatted HTML summary with improved visual elements and explanations
    """
    # Create dictionary to store metrics and their interpretations
    metrics = {
        "מיקוד שליטה פנימי (ICI)": {
            "value": interpret_delta_value(school_info.ici_delta_present),
            "delta": school_info.ici_delta_present,
            "description": "מודד את המידה שבה תלמידים מאמינים שיש להם שליטה על חייהם ועל תוצאות מעשיהם.",
            "high_value": "תלמידים עם תחושת שליטה גבוהה על חייהם, לוקחים אחריות על מעשיהם והתוצאות שלהם.",
            "low_value": "תלמידים עם תחושה מופחתת של שליטה על חייהם, נוטים לייחס הצלחות וכישלונות לגורמים חיצוניים."
        },
        "חוסן (RISC)": {
            "value": interpret_delta_value(school_info.risc_delta_present),
            "delta": school_info.risc_delta_present,
            "description": "מודד את היכולת של תלמידים להתאושש מקשיים ולהסתגל לשינויים.",
            "high_value": "תלמידים עם יכולת גבוהה להתמודד עם אתגרים, קשיים ושינויים.",
            "low_value": "תלמידים עם קושי בהתמודדות עם שינויים ואתגרים, ויכולת התאוששות נמוכה יותר."
        },
        "תפיסת עבר מעכבת": {
            "value": interpret_delta_value(school_info.future_negetive_past_delta_present),
            "delta": school_info.future_negetive_past_delta_present,
            "description": "מודד את המידה שבה חוויות שליליות מהעבר משפיעות על ההווה והעתיד.",
            "high_value": "תפיסת עבר מעכבת גבוהה - תלמידים נוטים להתמקד בחוויות שליליות מהעבר שמשפיעות על התנהגותם בהווה.",
            "low_value": "תפיסת עבר מעכבת נמוכה - תלמידים פחות מושפעים מחוויות שליליות מהעבר."
        },
        "עבר כתשתית חיובית": {
            "value": interpret_delta_value(school_info.future_positive_past_delta_present),
            "delta": school_info.future_positive_past_delta_present,
            "description": "מודד את המידה שבה תלמידים רואים בעבר שלהם כבסיס חיובי להתפתחות.",
            "high_value": "תלמידים רואים בעבר שלהם מקור חיובי לצמיחה, למידה והתפתחות.",
            "low_value": "תלמידים מתקשים לראות בעבר שלהם כמקור חיובי להתפתחות."
        },
        "דטרמיניסטיות": {
            "value": interpret_delta_value(school_info.future_fatalic_present_delta_present),
            "delta": school_info.future_fatalic_present_delta_present,
            "description": "מודד את המידה שבה תלמידים מאמינים שהעתיד נקבע מראש ואין להם שליטה עליו.",
            "high_value": "תלמידים נוטים להאמין שהעתיד כבר נקבע מראש ולא ניתן לשנותו - אמונה שעלולה להוביל לפסיביות.",
            "low_value": "תלמידים מאמינים שיש להם השפעה על העתיד ויכולת לעצב אותו."
        },
        "סיפוק מיידי": {
            "value": interpret_delta_value(school_info.future_hedonistic_present_delta_present),
            "delta": school_info.future_hedonistic_present_delta_present,
            "description": "מודד את הנטייה להעדיף תגמולים מיידיים על פני תועלות עתידיות.",
            "high_value": "תלמידים נוטים להעדיף סיפוקים מיידיים על פני השקעה לטווח ארוך.",
            "low_value": "תלמידים מוכנים לדחות סיפוקים מיידיים לטובת תועלות משמעותיות יותר בעתיד."
        },
        "תפיסת עתיד": {
            "value": interpret_delta_value(school_info.future_future_delta_present),
            "delta": school_info.future_future_delta_present,
            "description": "מודד את המידה שבה תלמידים חושבים על העתיד ומתכננים אותו.",
            "high_value": "תלמידים מפתחים חשיבה עתידית, מציבים מטרות ופועלים להשגתן.",
            "low_value": "תלמידים פחות מתמקדים בתכנון העתיד ובחשיבה לטווח ארוך."
        }
    }
    
    # Generate strength and weakness sections with improved visualization
    strengths = []
    weaknesses = []
      # Function to get color and icon based on interpretation
    def get_display_elements(delta_value):
        # בדיקה אם הערך הוא None
        if delta_value is None:
            print("DEBUG: delta_value is None in get_display_elements")
            return "#757575", "&#8776;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #757575; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(117, 117, 117, 0.1);"
            
        if delta_value == 30:
            return "#1b5e20", "&#10004;&#10004;&#10004;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #1b5e20; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(27, 94, 32, 0.1);"
        elif delta_value == 20:
            return "#2e7d32", "&#10004;&#10004;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #2e7d32; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(46, 125, 50, 0.1);"
        elif delta_value == 10:
            return "#43a047", "&#10004;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #43a047; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(67, 160, 71, 0.1);"
        elif delta_value == -30:
            return "#b71c1c", "&#10060;&#10060;&#10060;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #b71c1c; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(183, 28, 28, 0.1);"
        elif delta_value == -20:
            return "#d32f2f", "&#10060;&#10060;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #d32f2f; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(211, 47, 47, 0.1);"
        elif delta_value == -10:
            return "#e53935", "&#10060;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #e53935; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(229, 57, 53, 0.1);"
        else:
            return "#757575", "&#8776;", "margin-top: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 2px solid #757575; border-radius: 10px; padding: 0.5rem 1rem; background-color: rgba(117, 117, 117, 0.1);"
    
    # Create improved metric cards for overview
    metric_cards = []
    for metric_name, metric_data in metrics.items():
        color, icon, badge_style = get_display_elements(metric_data["delta"])
        interpretation = metric_data["value"]
        
        metric_card = f"""
        <div class="metric-card" style="background-color: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 5px solid {color};">
            <h3 style="color: #333; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 8px;">{metric_name}</h3>
            <p style="margin-bottom: 5px;">{metric_data["description"]}</p>
            <div style="{badge_style}">
                <span style="font-size: 1.2rem; margin-left: 5px;">{icon}</span>
                <span style="color: {color}; font-weight: bold;">{interpretation}</span>
            </div>
            <div style="font-size: 0.9rem; margin-top: 10px; color: #555;">
                <p style="margin: 5px 0;"><strong>ציון גבוה:</strong> {metric_data["high_value"]}</p>
                <p style="margin: 5px 0;"><strong>ציון נמוך:</strong> {metric_data["low_value"]}</p>
            </div>
        </div>
        """
        metric_cards.append(metric_card)
          # Add to strengths or weaknesses based on delta value
        if metric_data["delta"] is not None and metric_data["delta"] > 0:
            strengths.append(f"""
            <div style="background-color: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 5px solid {color};">
                <h3 style="color: #333; margin-top: 0;">{metric_name}</h3>
                <div style="{badge_style}">
                    <span style="font-size: 1.2rem; margin-left: 5px;">{icon}</span>
                    <span style="color: {color}; font-weight: bold;">{interpretation}</span>
                </div>
                <p style="margin-top: 10px;">{metric_data["high_value"]}</p>
            </div>
            """)
        elif metric_data["delta"] is not None and metric_data["delta"] < 0:
            weaknesses.append(f"""
            <div style="background-color: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 5px solid {color};">
                <h3 style="color: #333; margin-top: 0;">{metric_name}</h3>
                <div style="{badge_style}">
                    <span style="font-size: 1.2rem; margin-left: 5px;">{icon}</span>
                    <span style="color: {color}; font-weight: bold;">{interpretation}</span>
                </div>
                <p style="margin-top: 10px;">{metric_data["low_value"]}</p>
            </div>
            """)
    
    # Generate improvement questions with better formatting
    questions = get_improvement_questions(school_info.worst_anigma_name, school_info.worst_heg1_text)
      # Format the summary with improved HTML styling
    summary = f"""
<div style="direction: rtl; text-align: right; font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5; border-radius: 10px; max-width: 1200px; margin: 0 auto;">
    <h1 style="color: #1565c0; text-align: center; border-bottom: 2px solid #1565c0; padding-bottom: 15px; margin-bottom: 30px;">סיכום ביצועי בית הספר בהשוואה לממוצע הארצי</h1>

    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h2 style="color: #2e7d32; border-bottom: 1px solid #c8e6c9; padding-bottom: 10px;">מה המשמעות של המדדים?</h2>
        <p style="margin-bottom: 15px;">הנתונים הבאים מציגים השוואה בין ביצועי בית הספר לבין הממוצע הארצי במספר מדדים פסיכולוגיים-חינוכיים חשובים:</p>
        <ul style="list-style-type: none; padding-right: 0;">
            <li style="margin-bottom: 10px;"><strong>מיקוד שליטה פנימי (ICI):</strong> המידה שבה תלמידים מאמינים שיש להם שליטה על חייהם.</li>
            <li style="margin-bottom: 10px;"><strong>חוסן (RISC):</strong> היכולת להתאושש מקשיים ולהסתגל לשינויים.</li>
            <li style="margin-bottom: 10px;"><strong>תפיסות זמן:</strong> הדרך שבה תלמידים תופסים את העבר, ההווה והעתיד שלהם.</li>
        </ul>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;">
        {"".join(metric_cards)}
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px;">
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #2e7d32; border-bottom: 1px solid #c8e6c9; padding-bottom: 10px;">תחומי חוזק</h2>
            {f'<div style="display: grid; grid-template-columns: 1fr; gap: 15px;">{"".join(strengths)}</div>' if strengths else '<p style="color: #757575; font-style: italic;">לא נמצאו תחומי חוזק משמעותיים בהשוואה לממוצע הארצי.</p>'}
        </div>

        <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #c62828; border-bottom: 1px solid #ffcdd2; padding-bottom: 10px;">תחומים לשיפור</h2>
            {f'<div style="display: grid; grid-template-columns: 1fr; gap: 15px;">{"".join(weaknesses)}</div>' if weaknesses else '<p style="color: #757575; font-style: italic;">לא נמצאו תחומים לשיפור משמעותיים בהשוואה לממוצע הארצי.</p>'}
        </div>
    </div>

    <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; margin-top: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 5px solid #c62828;">
        <h2 style="color: #c62828; border-bottom: 1px solid #ffcdd2; padding-bottom: 10px;">נקודת תורפה מרכזית</h2>
        <p>בית הספר מתמודד עם אתגר משמעותי בתחום <strong style="color: #c62828;">{school_info.worst_anigma_name}</strong>.</p>
        <p>ההיגד שקיבל את התוצאה החלשה ביותר הוא:</p>
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0; border-right: 4px solid #c62828;">
            <p style="font-style: italic; font-size: 1.1rem;">"{school_info.worst_heg1_text}"</p>
        </div>
    </div>

    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-top: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-right: 5px solid #1565c0;">
        <h2 style="color: #1565c0; border-bottom: 1px solid #bbdefb; padding-bottom: 10px;">שאלות למחשבה ושיפור</h2>
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <p style="font-size: 1.1rem; margin: 0;"><strong>1. {questions[0]}</strong></p>
        </div>
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <p style="font-size: 1.1rem; margin: 0;"><strong>2. {questions[1]}</strong></p>
        </div>
    </div>

    <div style="margin-top: 30px; background-color: #f5f5f5; padding: 15px; border-radius: 5px; border: 1px dashed #9e9e9e;">
        <h3 style="color: #424242; margin-top: 0;">כיצד לקרוא את התוצאות?</h3>
        <ul style="color: #616161;">
            <li><span style="color: #2e7d32;">&#10004;</span> ירוק מסמל תוצאות טובות יותר מהממוצע הארצי.</li>
            <li><span style="color: #e53935;">&#10060;</span> אדום מסמל תוצאות נמוכות יותר מהממוצע הארצי.</li>
            <li><span style="color: #757575;">&#8776;</span> אפור מסמל תוצאות הדומות לממוצע הארצי.</li>
            <li>עוצמת הצבע והסימון מעידים על גודל הפער מהממוצע הארצי.</li>
        </ul>
    </div>
</div>
"""
    
    return summary