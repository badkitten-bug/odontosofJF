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
            especialidad_id INTEGER,
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
            password TEXT,
            FOREIGN KEY (especialidad_id) REFERENCES specialties(id)
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

        # Tabla de especialidades
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS specialties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            codigo INTEGER UNIQUE,  -- Se generará automáticamente
            descripcion TEXT,
            estado TEXT DEFAULT 'Activo'
        );
        ''')

        # Trigger para asignar el código automáticamente si no se proporciona
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS set_specialty_codigo AFTER INSERT ON specialties
        BEGIN
            UPDATE specialties
            SET codigo = (SELECT COALESCE(MAX(codigo), 0) + 1 FROM specialties)
            WHERE id = NEW.id AND NEW.codigo IS NULL;
        END;
        ''')

        # Tabla de Historias Clínicas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias_clinicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            numero_historia TEXT NOT NULL UNIQUE,
            fecha_creacion TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (paciente_id) REFERENCES patients(id)
        );
        ''')

        # Tabla de Exploración Física
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

        # Tabla de Funciones Vitales
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

        # Tabla de Alergias
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alergias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            alergia TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        # Tabla de Odontograma (detallado)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontograma_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diente TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        # Tabla de Diagnósticos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diagnostico TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        # Tabla de Tratamientos (detallado)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tratamientos_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            tratamiento TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
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