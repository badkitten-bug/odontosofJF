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

        # Tabla de Tipos de Documento
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')
        cursor.execute("SELECT COUNT(*) FROM document_types")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO document_types (name) VALUES (?)",
                [('DNI',), ('Carné de Extranjería',), ('Pasaporte',), ('RUC',)]
            )

        # Tabla de Niveles de Educación
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS education_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL UNIQUE
        )
        ''')
        cursor.execute("SELECT COUNT(*) FROM education_levels")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO education_levels(level) VALUES (?)",
                [('INICIAL',), ('PRIMARIA',), ('SECUNDARIA',), ('UNIVERSITARIA',), ('SUPERIOR',)]
            )

        # Tabla de Estados Civiles
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS marital_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL UNIQUE
        )
        ''')
        cursor.execute("SELECT COUNT(*) FROM marital_status")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO marital_status(status) VALUES (?)",
                [('SOLTERO',), ('CASADO',), ('VIUDO',), ('DIVORCIADO',)]
            )

        # Tabla de Especialidades
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS specialties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            estado TEXT DEFAULT 'Activo'
        );
        ''')

        # Tabla de Doctores (Odontólogos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            especialidad_id INTEGER,
            tipo_documento_id INTEGER,
            nro_documento TEXT NOT NULL,
            ruc TEXT,
            direccion TEXT,
            colegiatura TEXT,
            fecha_registro TEXT,
            fecha_nacimiento TEXT NOT NULL,
            celular TEXT,
            sexo TEXT,
            estado TEXT,
            correo TEXT,
            foto TEXT,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY (especialidad_id) REFERENCES specialties(id),
            FOREIGN KEY (tipo_documento_id) REFERENCES document_types(id)
        )
        ''')

        # Usuario predeterminado
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, role, email) VALUES ('admin', 'admin123', 'admin', 'admin@clinic.com')")

        # Tabla de Pacientes – aquí guardamos el número de historia (history_number)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            edad INTEGER,
            tipo_documento_id INTEGER,
            nro_documento TEXT NOT NULL UNIQUE,
            history_number TEXT UNIQUE,
            grado_instruccion_id INTEGER,
            hospital_nacimiento TEXT,
            pais TEXT,
            departamento TEXT,
            provincia TEXT,
            distrito TEXT,
            direccion TEXT,
            telefono TEXT,
            fecha_nacimiento TEXT NOT NULL,
            estado_civil_id INTEGER,
            afiliado TEXT,
            sexo TEXT,
            alergia TEXT,
            correo TEXT,
            observacion TEXT,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            estado TEXT,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(tipo_documento_id) REFERENCES document_types(id),
            FOREIGN KEY(grado_instruccion_id) REFERENCES education_levels(id),
            FOREIGN KEY(estado_civil_id) REFERENCES marital_status(id)
        )
        ''')

        # Tabla de Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            first_time TEXT NOT NULL,
            end_time TEXT,
            duration INTEGER,
            notes TEXT,
            status_id INTEGER DEFAULT 1,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(status_id) REFERENCES appointment_status(id),
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Estado de las Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        ''')
        cursor.execute("SELECT COUNT(*) FROM appointment_status WHERE name IN ('Pending', 'Completed', 'Cancelled')")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO appointment_status (name) VALUES ('Pending'), ('Completed'), ('Cancelled')")

        # Tabla de Tratamientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            cost REAL NOT NULL
        )
        ''')

        # Tabla de Tratamientos Aplicados
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

        # Tabla de Historias Clínicas (almacena datos adicionales de la historia)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias_clinicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            fecha_creacion TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (paciente_id) REFERENCES patients(id)
        );
        ''')

        # Tablas complementarias de la Historia Clínica
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exploracion_fisica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            enfermedad_actual TEXT,
            tiempo_enfermedad TEXT,
            motivo_consulta TEXT,
            signos_sintomas TEXT,
            antecedentes_personales TEXT,
            antecedentes_familiares TEXT,
            medicamento_actual TEXT,
            motivo_uso_medicamento TEXT,
            dosis_medicamento TEXT,
            tratamiento_ortodoncia TEXT,
            alergico_medicamento TEXT,
            hospitalizado TEXT,
            transtorno_nervioso TEXT,
            enfermedades_padecidas TEXT,
            cepilla_dientes TEXT,
            presion_arterial TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS funciones_vitales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            presion_arterial TEXT,
            pulso TEXT,
            temperatura TEXT,
            frecuencia_cardiaca TEXT,
            frecuencia_respiratoria TEXT,
            peso TEXT,
            talla TEXT,
            imc TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alergias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            alergia TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontograma_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diente TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diagnostico TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tratamientos_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            tratamiento TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        # Índices para mejorar el rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id ON appointments(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_doctor_id ON appointments(doctor_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_history ON historias_clinicas(paciente_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_odontogram ON odontogram(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_payments ON payments(patient_id)')

        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Base de datos 'clinic.db' creada exitosamente con la estructura ampliada para Perú.")
