CREATE_CURRENCY_TABLE = '''CREATE TABLE IF NOT EXISTS currency(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    sign TEXT NOT NULL
                    )'''

CREATE_EXCHANGE_RATE_TABLE = '''CREATE TABLE IF NOT EXISTS exchange_rate(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    base_currency_id INTEGER NOT NULL,
                    target_currency_id INTEGER NOT NULL,
                    rate TEXT NOT NULL,
                    
                    UNIQUE(base_currency_id, target_currency_id),
                    
                    FOREIGN KEY (base_currency_id) REFERENCES currency(id),
                    FOREIGN KEY (target_currency_id) REFERENCES currency(id)
                    )'''
