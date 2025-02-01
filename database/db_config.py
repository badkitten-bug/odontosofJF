import sqlite3

def connect_db():
    """Establece y retorna una conexión a la base de datos."""
    return sqlite3.connect("clinic.db", timeout=10)

def create_tables():
    """Crea todas las tablas necesarias en la base de datos."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Tabla de Usuarios (para el login de cuenta)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            last_login TEXT
        )
        ''')

        # Tabla de Doctores (Odontólogos) con campos extendidos para Perú
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            tipo_documento TEXT,
            nro_documento TEXT,
            ruc TEXT,
            direccion TEXT,
            colegiatura TEXT,
            fecha_registro TEXT,
            fecha_nacimiento TEXT,
            telefono TEXT,
            celular TEXT,
            sexo TEXT,
            estado TEXT,
            correo TEXT,
            foto TEXT,
            usuario TEXT UNIQUE,
            password TEXT
        )
        ''')

        # Usuario predeterminado
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, role, email) VALUES ('admin', 'admin123', 'admin', 'admin@clinic.com')")

        # Tabla de Pacientes con campos ampliados para Perú
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_number TEXT, -- Número de historia clínica (se generará automáticamente)
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            edad INTEGER,
            documento TEXT,
            grado_instruccion TEXT,
            hospital_nacimiento TEXT,
            pais TEXT,
            departamento TEXT,
            provincia TEXT,
            distrito TEXT,
            direccion TEXT,
            telefono TEXT,
            fecha_nacimiento TEXT,
            estado_civil TEXT,
            afiliado TEXT,
            sexo TEXT,
            alergia TEXT,
            correo TEXT,
            observacion TEXT,
            fecha_registro TEXT,
            estado TEXT,
            is_deleted INTEGER DEFAULT 0
        )
        ''')

        # Crear trigger para asignar history_number automáticamente al insertar un paciente
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS set_history_number AFTER INSERT ON patients
        BEGIN
            UPDATE patients
            SET history_number = NEW.fecha_registro || '-' || NEW.id
            WHERE id = NEW.id;
        END;
        ''')

        # Tabla de Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            duration INTEGER,
            notes TEXT,
            status TEXT DEFAULT 'Pending',
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Tratamientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            cost REAL NOT NULL
        )
        ''')

        # Tabla de Tratamientos Aplicados (Relación entre Citas y Tratamientos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS applied_treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER NOT NULL,
            treatment_id INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY(appointment_id) REFERENCES appointments(id),
            FOREIGN KEY(treatment_id) REFERENCES treatments(id)
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
            treatment_plan TEXT,
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
            payment_method TEXT,
            status TEXT DEFAULT 'Pending',
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Inventario
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL
        )
        ''')

        # Tabla de Odontograma
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontogram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            tooth_number INTEGER NOT NULL,
            condition TEXT,
            notes TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Seguros Médicos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS insurance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            insurance_company TEXT NOT NULL,
            policy_number TEXT NOT NULL,
            coverage_details TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Prescripciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            medication TEXT NOT NULL,
            dosage TEXT NOT NULL,
            instructions TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Facturas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Comentarios y Calificaciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comments TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Horarios de Doctores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctor_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Recursos Humanos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            hire_date TEXT NOT NULL
        )
        ''')

        # Índices para mejorar el rendimiento de las consultas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id ON appointments(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_doctor_id ON appointments(doctor_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_history ON history(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_odontogram ON odontogram(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_payments ON payments(patient_id)')

        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Base de datos 'clinic.db' creada exitosamente con la estructura ampliada para Perú.")
