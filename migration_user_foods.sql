-- ====================================
-- Migration: הוספת טבלאות לניהול מזונות אישיים למשתמש
-- ====================================

-- טבלת מזונות המערכת (רשימה בסיסית)
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
);

-- טבלת מזונות אישיים של משתמשים
CREATE TABLE IF NOT EXISTS user_foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_id TEXT NOT NULL,
    action TEXT NOT NULL,  -- 'add', 'edit', 'delete'
    food_data TEXT,  -- נתוני המזון בפורמט JSON
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- אינדקסים לשיפור הביצועים
CREATE INDEX IF NOT EXISTS idx_user_foods_user_id ON user_foods(user_id);
CREATE INDEX IF NOT EXISTS idx_user_foods_food_id ON user_foods(food_id);
CREATE INDEX IF NOT EXISTS idx_user_foods_action ON user_foods(action);