"""
סקריפט לאתחול מזונות המערכת - גרסה עצמאית ללא תלות ב-Flask
"""

import sqlite3
import json

# רשימת מזונות בסיסית - מועתקת מהקוד המקורי
def get_default_foods():
    foods = [
        # חלבונים
        {"id": "1", "name": "ביצה", "protein": 6, "calories": 70, "carbs": 0.6, "fat": 5, "category": "חלבונים", "allowed_meals": "breakfast,lunch,dinner", "price": 1.5},
        {"id": "2", "name": "ביצים קשות", "protein": 12, "calories": 140, "carbs": 1.2, "fat": 10, "category": "חלבונים", "allowed_meals": "breakfast,lunch,dinner", "price": 2.0},
        {"id": "3", "name": "חזה עוף", "protein": 23, "calories": 110, "carbs": 0, "fat": 1.5, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 8.0},
        {"id": "4", "name": "שוק עוף", "protein": 20, "calories": 120, "carbs": 0, "fat": 3, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 6.0},
        {"id": "5", "name": "סלמון", "protein": 20, "calories": 150, "carbs": 0, "fat": 6, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 25.0},
        {"id": "6", "name": "טונה", "protein": 23, "calories": 130, "carbs": 0, "fat": 1, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 15.0},
        {"id": "7", "name": "גבינה צהובה 5%", "protein": 25, "calories": 100, "carbs": 1, "fat": 5, "category": "חלבונים", "allowed_meals": "breakfast,lunch", "price": 12.0},
        {"id": "8", "name": "קוטג' צהוב 9%", "protein": 18, "calories": 90, "carbs": 2, "fat": 3, "category": "חלבונים", "allowed_meals": "breakfast,lunch", "price": 8.0},
        {"id": "9", "name": "גבינה בולגרית 5%", "protein": 16, "calories": 70, "carbs": 1, "fat": 3, "category": "חלבונים", "allowed_meals": "breakfast,lunch", "price": 6.0},
        {"id": "10", "name": "טופו", "protein": 8, "calories": 80, "carbs": 2, "fat": 5, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 10.0},
        
        # פחמימות
        {"id": "11", "name": "אורז בן", "protein": 3, "calories": 130, "carbs": 28, "fat": 0.3, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 8.0},
        {"id": "12", "name": "פסטה", "protein": 5, "calories": 150, "carbs": 30, "fat": 0.5, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 6.0},
        {"id": "13", "name": "פיתה", "protein": 4, "calories": 100, "carbs": 20, "fat": 1, "category": "פחמימות", "allowed_meals": "breakfast,lunch", "price": 3.0},
        {"id": "14", "name": "לחם שיפון", "protein": 4, "calories": 80, "carbs": 15, "fat": 1, "category": "פחמימות", "allowed_meals": "breakfast,lunch", "price": 4.0},
        {"id": "15", "name": "שיבולת שועל", "protein": 5, "calories": 150, "carbs": 27, "fat": 2.5, "category": "פחמימות", "allowed_meals": "breakfast", "price": 5.0},
        {"id": "16", "name": "קינואה", "protein": 4, "calories": 120, "carbs": 21, "fat": 2, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 12.0},
        {"id": "17", "name": "תפוח אדמה", "protein": 2, "calories": 77, "carbs": 17, "fat": 0.1, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 3.0},
        {"id": "18", "name": "בטטה", "protein": 2, "calories": 86, "carbs": 20, "fat": 0.1, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 4.0},
        {"id": "19", "name": "אפונה", "protein": 5, "calories": 81, "carbs": 14, "fat": 0.4, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 6.0},
        {"id": "20", "name": "תירס", "protein": 3, "calories": 96, "carbs": 21, "fat": 1.5, "category": "פחמימות", "allowed_meals": "lunch,dinner", "price": 5.0},
        
        # ירקות
        {"id": "21", "name": "מלפפון", "protein": 0.6, "calories": 16, "carbs": 4, "fat": 0.1, "category": "ירקות", "allowed_meals": "breakfast,lunch,dinner", "price": 2.0},
        {"id": "22", "name": "עגבנייה", "protein": 0.9, "calories": 18, "carbs": 4, "fat": 0.2, "category": "ירקות", "allowed_meals": "breakfast,lunch,dinner", "price": 2.5},
        {"id": "23", "name": "גזר", "protein": 0.9, "calories": 41, "carbs": 10, "fat": 0.2, "category": "ירקות", "allowed_meals": "breakfast,lunch,dinner", "price": 3.0},
        {"id": "24", "name": "ברוקולי", "protein": 2.8, "calories": 34, "carbs": 7, "fat": 0.4, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 5.0},
        {"id": "25", "name": "כרוב", "protein": 1.3, "calories": 25, "carbs": 6, "fat": 0.1, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 4.0},
        {"id": "26", "name": "פלפל", "protein": 0.9, "calories": 20, "carbs": 5, "fat": 0.2, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 4.0},
        {"id": "27", "name": "סלק", "protein": 1.6, "calories": 43, "carbs": 10, "fat": 0.2, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 3.5},
        {"id": "28", "name": "זוקיני", "protein": 1.2, "calories": 17, "carbs": 3, "fat": 0.3, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 4.5},
        {"id": "29", "name": "חסה", "protein": 1.4, "calories": 15, "carbs": 3, "fat": 0.2, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 3.0},
        {"id": "30", "name": "כרובית", "protein": 2, "calories": 25, "carbs": 5, "fat": 0.3, "category": "ירקות", "allowed_meals": "lunch,dinner", "price": 5.0},
        
        # פירות
        {"id": "31", "name": "תפוח", "protein": 0.3, "calories": 52, "carbs": 14, "fat": 0.2, "category": "פירות", "allowed_meals": "snack", "price": 4.0},
        {"id": "32", "name": "בננה", "protein": 1.1, "calories": 89, "carbs": 23, "fat": 0.3, "category": "פירות", "allowed_meals": "snack,breakfast", "price": 3.5},
        {"id": "33", "name": "תפוז", "protein": 0.9, "calories": 47, "carbs": 12, "fat": 0.1, "category": "פירות", "allowed_meals": "snack", "price": 3.0},
        {"id": "34", "name": "אבוקדו", "protein": 2, "calories": 160, "carbs": 9, "fat": 15, "category": "פירות", "allowed_meals": "breakfast,snack", "price": 8.0},
        {"id": "35", "name": "אגס", "protein": 0.4, "calories": 57, "carbs": 15, "fat": 0.1, "category": "פירות", "allowed_meals": "snack", "price": 4.5},
        {"id": "36", "name": "ענבים", "protein": 0.6, "calories": 69, "carbs": 18, "fat": 0.2, "category": "פירות", "allowed_meals": "snack", "price": 6.0},
        {"id": "37", "name": "אוכמניות", "protein": 0.7, "calories": 57, "carbs": 14, "fat": 0.3, "category": "פירות", "allowed_meals": "snack", "price": 8.0},
        {"id": "38", "name": "תותים", "protein": 0.7, "calories": 33, "carbs": 8, "fat": 0.3, "category": "פירות", "allowed_meals": "snack", "price": 10.0},
        {"id": "39", "name": "מלון", "protein": 0.8, "calories": 34, "carbs": 8, "fat": 0.2, "category": "פירות", "allowed_meals": "snack", "price": 5.0},
        {"id": "40", "name": "אננס", "protein": 0.5, "calories": 50, "carbs": 13, "fat": 0.1, "category": "פירות", "allowed_meals": "snack", "price": 6.0},
        
        # שומנים בריאים
        {"id": "41", "name": "שמן זית", "protein": 0, "calories": 120, "carbs": 0, "fat": 14, "category": "שומנים בריאים", "allowed_meals": "lunch,dinner", "price": 15.0},
        {"id": "42", "name": "אגוזי מלך", "protein": 4, "calories": 190, "carbs": 4, "fat": 18, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 25.0},
        {"id": "43", "name": "שקדים", "protein": 6, "calories": 170, "carbs": 6, "fat": 15, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 20.0},
        {"id": "44", "name": "פקאן", "protein": 3, "calories": 200, "carbs": 4, "fat": 20, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 30.0},
        {"id": "45", "name": "זרעי פשתן", "protein": 2, "calories": 150, "carbs": 8, "fat": 12, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 15.0},
        {"id": "46", "name": "זרעי חמנייה", "protein": 3, "calories": 165, "carbs": 7, "fat": 14, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 12.0},
        {"id": "47", "name": "בוטנים", "protein": 7, "calories": 180, "carbs": 5, "fat": 16, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 15.0},
        {"id": "48", "name": "אגוז לוז", "protein": 4, "calories": 170, "carbs": 5, "fat": 15, "category": "שומנים בריאים", "allowed_meals": "snack", "price": 22.0},
        {"id": "49", "name": "שמן קוקוס", "protein": 0, "calories": 120, "carbs": 0, "fat": 14, "category": "שומנים בריאים", "allowed_meals": "breakfast", "price": 20.0},
        {"id": "50", "name": "חמאה", "protein": 0.1, "calories": 100, "carbs": 0, "fat": 11, "category": "שומנים בריאים", "allowed_meals": "breakfast", "price": 8.0},
        
        # מוצרי חלב
        {"id": "51", "name": "חלב 3%", "protein": 3, "calories": 60, "carbs": 5, "fat": 3, "category": "מוצרי חלב", "allowed_meals": "breakfast", "price": 6.0},
        {"id": "52", "name": "יוגורט טבעי", "protein": 10, "calories": 60, "carbs": 4, "fat": 0.4, "category": "מוצרי חלב", "allowed_meals": "breakfast,snack", "price": 4.0},
        {"id": "53", "name": "לבנה", "protein": 4, "calories": 35, "carbs": 1, "fat": 3, "category": "מוצרי חלב", "allowed_meals": "breakfast,snack", "price": 3.0},
        {"id": "54", "name": "חמאת בוטנים", "protein": 4, "calories": 190, "carbs": 6, "fat": 16, "category": "מוצרי חלב", "allowed_meals": "breakfast,snack", "price": 15.0},
        
        # קינוחים בריאים
        {"id": "55", "name": "דבש", "protein": 0.1, "calories": 304, "carbs": 82, "fat": 0, "category": "קינוחים בריאים", "allowed_meals": "breakfast", "price": 20.0},
        {"id": "56", "name": "שוקולד מריר 70%", "protein": 2, "calories": 170, "carbs": 13, "fat": 12, "category": "קינוחים בריאים", "allowed_meals": "snack", "price": 15.0},
        {"id": "57", "name": "גרנולה", "protein": 4, "calories": 150, "carbs": 20, "fat": 6, "category": "קינוחים בריאים", "allowed_meals": "breakfast", "price": 12.0},
        {"id": "58", "name": "דגים ללבן", "protein": 18, "calories": 100, "carbs": 0, "fat": 1, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 18.0},
        {"id": "59", "name": "כרישה", "protein": 20, "calories": 110, "carbs": 0, "fat": 2, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 20.0},
        {"id": "60", "name": "טונה בשמן", "protein": 26, "calories": 190, "carbs": 0, "fat": 8, "category": "חלבונים", "allowed_meals": "lunch,dinner", "price": 18.0},
    ]
    
    # הוספת מבנה prices לכל מזון
    for f in foods:
        f["prices"] = {
            "manual": f.pop("price", None),
            "shufersal": None,
            "rami_levy": None,
            "victory": None
        }
        f["active_price_source"] = "manual"
    
    return foods

def init_system_foods():
    conn = sqlite3.connect('nutrioptimal.db')
    cursor = conn.cursor()
    
    # יצירת הטבלאות החדשות אם לא קיימות
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_foods (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            protein REAL,
            calories REAL,
            carbs REAL,
            fat REAL,
            category TEXT,
            allowed_meals TEXT,
            price_manual REAL,
            price_shufersal REAL,
            price_rami_levy REAL,
            price_victory REAL,
            active_price_source TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_id TEXT NOT NULL,
            action TEXT NOT NULL,
            food_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # יצירת אינדקסים
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_foods_user_id ON user_foods(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_foods_food_id ON user_foods(food_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_foods_action ON user_foods(action)')
    
    # קבלת רשימת המזונות הבסיסית
    foods = get_default_foods()
    
    # מחיקת נתונים ישנים (אם יש)
    cursor.execute('DELETE FROM system_foods')
    
    # הכנסת המזונות לטבלה
    for food in foods:
        prices = food.get('prices', {})
        cursor.execute('''
            INSERT INTO system_foods (
                id, name, protein, calories, carbs, fat, category, allowed_meals,
                price_manual, price_shufersal, price_rami_levy, price_victory, active_price_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            food['id'],
            food['name'],
            food.get('protein'),
            food.get('calories'),
            food.get('carbs'),
            food.get('fat'),
            food.get('category'),
            food.get('allowed_meals'),
            prices.get('manual'),
            prices.get('shufersal'),
            prices.get('rami_levy'),
            prices.get('victory'),
            food.get('active_price_source', 'manual')
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ נטענו בהצלחה {len(foods)} מזונות לטבלת system_foods")

if __name__ == '__main__':
    init_system_foods()