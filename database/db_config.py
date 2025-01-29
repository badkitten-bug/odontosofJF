import sqlite3

def connect_db():
    return sqlite3.connect("clinic.db", timeout=10)

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()

        # Tabla de Usuarios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        # Tabla de Doctores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT
        )
        ''')

        # Usuario predeterminado
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")

        # Tabla de Pacientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            phone TEXT,
            address TEXT,
            history_number TEXT UNIQUE,  -- Número de historia clínica único
            is_deleted INTEGER DEFAULT 0
        )
        ''')

        # Tabla de Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'Pending',
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Historia Clínica
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            procedure TEXT NOT NULL,
            notes TEXT,
            attachments TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Pagos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        conn.commit()
