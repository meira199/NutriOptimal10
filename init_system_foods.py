"""
סקריפט לאתחול מזונות המערכת במסד הנתונים
רץ פעם אחת בלבד כדי לאכלס את טבלת system_foods
"""

import sqlite3
from app import get_default_foods

def init_system_foods():
    conn = sqlite3.connect('nutrioptimal.db')
    cursor = conn.cursor()
    
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