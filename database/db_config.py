import sqlite3

def connect_db():
    """Establece y retorna una conexión a la base de datos."""
    return sqlite3.connect("clinic.db", timeout=10)

def create_tables():
    """Crea todas las tablas necesarias en la base de datos."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # 📌 TABLA DE USUARIOS (LOGIN)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            last_login TEXT
        );
        ''')

        # 📌 TABLAS COMPLEMENTARIAS (TIPOS DE DOCUMENTO, EDUCACIÓN, ESTADO CIVIL)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        ''')

        cursor.execute("SELECT COUNT(*) FROM document_types")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO document_types (name) VALUES (?)",
                [('DNI',), ('Carné de Extranjería',), ('Pasaporte',), ('RUC',)]
            )
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS education_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL UNIQUE
        );
        ''')
        cursor.execute("SELECT COUNT(*) FROM education_levels")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO education_levels(level) VALUES (?)",
                [('INICIAL',), ('PRIMARIA',), ('SECUNDARIA',), ('UNIVERSITARIA',), ('SUPERIOR',)]
            )

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS marital_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL UNIQUE
        );
        ''')
        cursor.execute("SELECT COUNT(*) FROM marital_status")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO marital_status(status) VALUES (?)",
                [('Soltero(a)',), ('Casado(a)',), ('Divorciado(a)',), ('Viudo(a)',)]
            )

        # 📌 TABLA DE ESPECIALIDADES
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS specialties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            estado TEXT DEFAULT 'Activo'
        );
        ''')

        #INSERTAR 1 ESPECIALIDADE DE PRUEBA
        cursor.execute("SELECT * FROM specialties WHERE nombre = 'Odontología'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO specialties (nombre, descripcion) VALUES ('Odontología', 'Especialidad en odontología general')")

            
        # 📌 TABLA DE DOCTORES (ODONTÓLOGOS)
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
            FOREIGN KEY (especialidad_id) REFERENCES specialties(id) ON DELETE SET NULL,
            FOREIGN KEY (tipo_documento_id) REFERENCES document_types(id) ON DELETE SET NULL
        );
        ''')

        #INSERTAR UN DOCTOR DE PRUEBA
        cursor.execute("SELECT * FROM doctors WHERE nro_documento = '87654321'")
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO doctors (nombres, apellidos, especialidad_id, tipo_documento_id, nro_documento, ruc, direccion, colegiatura, fecha_registro, fecha_nacimiento, celular, sexo, estado, correo)
            VALUES ('Juan', 'Pérez', 1, 1, '87654321', '12345678901', 'Av. Los Pinos 123', '123456', '2021-05-12', '1996-05-12', '987654321', 'M', 'Activo', 'juan.perez@example.com')
            ''')
    
        # Usuario predeterminado
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, role, email) VALUES ('admin', 'admin123', 'admin', 'admin@clinic.com')")

        # 📌 TABLA DE PACIENTES (CON `history_number`)
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
            FOREIGN KEY(tipo_documento_id) REFERENCES document_types(id) ON DELETE SET NULL,
            FOREIGN KEY(grado_instruccion_id) REFERENCES education_levels(id) ON DELETE SET NULL,
            FOREIGN KEY(estado_civil_id) REFERENCES marital_status(id) ON DELETE SET NULL
        );
        ''')

        #INSERTAR UN PACIENTE DE PRUEBA
        cursor.execute("SELECT * FROM patients WHERE nro_documento = '12345678'")
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO patients (nombres, apellidos, edad, tipo_documento_id, nro_documento, history_number, grado_instruccion_id, hospital_nacimiento, pais, departamento, provincia, distrito, direccion, telefono, fecha_nacimiento, estado_civil_id, afiliado, sexo, alergia, correo, observacion, estado)
            VALUES ('Juan', 'Pérez', 25, 1, '12345678', 'P0001', 3, 'Hospital Nacional', 'Perú', 'Lima', 'Lima', 'Lima', 'Av. Los Pinos 123', '987654321', '1996-05-12', 2, 'SIS', 'M', 'Ninguna', 'juan.perez@example.com', 'Observaciones', 'Activo')
            ''')

        # 📌 TABLA DE HISTORIAS CLÍNICAS (RELACIONADA A `patients`)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias_clinicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            fecha_creacion TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (paciente_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        ''')

        # 📌 TABLA DE ODONTOGRAMA (AHORA RELACIONADA A `historias_clinicas`)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontogram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            tooth_number INTEGER NOT NULL,
            condition TEXT,
            notes TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id) ON DELETE CASCADE
        );
        ''')

        # 📌 TABLA DE ODONTOGRAMA DETALLE (Dientes específicos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontograma_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diente TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id) ON DELETE CASCADE
        );
        ''')

        # 📌 TABLAS DE EXPLORACIÓN FÍSICA Y FUNCIONES VITALES
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
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id) ON DELETE CASCADE
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
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id) ON DELETE CASCADE
        );
        ''')

        # 📌 TABLAS DE DIAGNÓSTICOS Y TRATAMIENTOS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            diagnostico TEXT,
            observaciones TEXT,
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id) ON DELETE CASCADE
        );
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
            appointment_id INTEGER,
            treatment_id INTEGER NOT NULL,
            historia_id INTEGER,
            notes TEXT,
            FOREIGN KEY(appointment_id) REFERENCES appointments(id),
            FOREIGN KEY(treatment_id) REFERENCES treatments(id),
            FOREIGN key(historia_id) references historias_clinicas(id)
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
            category_id INTEGER,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0),
            supplier_id INTEGER,
            status TEXT DEFAULT 'Disponible' CHECK(status IN ('Disponible', 'Agotado', 'Dañado')),
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES inventory_categories(id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        );
        ''')


        # Tabla de Categorías de Inventario
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        ''')

        # Insertar datos iniciales en Categorías
        cursor.execute("SELECT COUNT(*) FROM inventory_categories")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany(
                "INSERT INTO inventory_categories (name) VALUES (?)",
                [('Equipos',), ('Materiales',), ('Medicamentos',), ('Otros',)]
            )

        # Tabla de Proveedores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT
        );
        ''')

        # Tabla de Movimientos de Inventario
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventory_id INTEGER NOT NULL,
            movement_type TEXT NOT NULL CHECK(movement_type IN ('Entrada', 'Salida')),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (inventory_id) REFERENCES inventory(id)
        );
        ''')

        # Tabla de Materiales Usados en Tratamientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatment_materials_used (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treatment_id INTEGER NOT NULL,
            inventory_id INTEGER NOT NULL,
            quantity_used INTEGER NOT NULL CHECK(quantity_used > 0),
            FOREIGN KEY (treatment_id) REFERENCES applied_treatments(id),
            FOREIGN KEY (inventory_id) REFERENCES inventory(id)
        );
''')

        # Tabla de Uso de Inventario en Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment_inventory_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER NOT NULL,
            inventory_id INTEGER NOT NULL,
            quantity_used INTEGER NOT NULL CHECK(quantity_used > 0),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id),
            FOREIGN KEY (inventory_id) REFERENCES inventory(id)
        );
        ''')
        # Tabla de Odontograma
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontogram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            tooth_number INTEGER NOT NULL,
            condition TEXT,
            notes TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY(historia_id) REFERENCES historias_clinicas(id)
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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alergias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id INTEGER NOT NULL,
            alergia TEXT,
            observaciones TEXT,
            FOREIGN KEY (historia_id) REFERENCES historias_clinicas(id)
        );
        ''')

        # 📌 ÍNDICES PARA MEJORAR EL RENDIMIENTO
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historia_id_odontogram ON odontogram(historia_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historia_id_odontograma_detalle ON odontograma_detalle(historia_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historia_id_exploracion ON exploracion_fisica(historia_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historia_id_funciones_vitales ON funciones_vitales(historia_id)')

        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Base de datos 'clinic.db' creada exitosamente con la estructura corregida.")
