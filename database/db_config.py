import sqlite3
from datetime import datetime

def connect_db():
    """Establece y retorna una conexión a la base de datos."""
    return sqlite3.connect("clinic.db", timeout=10)

def create_tables():
    """Crea todas las tablas necesarias en la base de datos."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Tabla de Usuarios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,  -- Roles: admin, doctor, recepcionista, etc.
            email TEXT,
            last_login TEXT,
            fecha_registro TEXT NOT NULL,  -- Fecha de registro del usuario
            ultima_actualizacion TEXT      -- Última actualización del usuario
        )
        ''')
        # Verificar si el usuario predeterminado ya existe
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            # Insertar el usuario predeterminado (admin)
            cursor.execute('''
            INSERT INTO users (username, password, role, email, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin123', 'admin', 'admin@clinic.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # Tabla de Doctores (Odontólogos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,  -- Especialidad del odontólogo
            tipo_documento TEXT,     -- Tipo de documento (DNI, CE, etc.)
            nro_doc TEXT UNIQUE,     -- Número de documento
            ruc TEXT,                -- RUC (opcional)
            colegiatura TEXT UNIQUE, -- Número de colegiatura
            fecha_nacimiento TEXT,   -- Fecha de nacimiento
            phone TEXT,              -- Teléfono fijo
            celular TEXT,            -- Celular
            gender TEXT,             -- Género
            estado TEXT DEFAULT 'Activo',  -- Estado: Activo, Inactivo
            email TEXT,
            foto TEXT,               -- URL o ruta de la foto
            usuario TEXT UNIQUE,     -- Nombre de usuario
            password TEXT,           -- Contraseña
            is_deleted INTEGER DEFAULT 0,  -- Soft delete
            fecha_registro TEXT NOT NULL,  -- Fecha de registro
            ultima_actualizacion TEXT      -- Última actualización
        )
        ''')
        # Tabla de Pacientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,              -- Edad del paciente
            phone TEXT,               -- Teléfono
            address TEXT,             -- Dirección
            email TEXT,
            gender TEXT,              -- Género
            blood_type TEXT,          -- Tipo de sangre
            history_number TEXT UNIQUE,  -- Número de historia clínica
            grado_instruccion TEXT,   -- Grado de instrucción
            hospital_nacimiento TEXT, -- Hospital de nacimiento
            pais TEXT,                -- País
            departamento TEXT,        -- Departamento
            provincia TEXT,           -- Provincia
            distrito TEXT,            -- Distrito
            estado_civil TEXT,        -- Estado civil
            afiliado TEXT,            -- Afiliado a algún seguro
            alergias TEXT,            -- Alergias (puede ser JSON o texto)
            observaciones TEXT,       -- Observaciones adicionales
            is_deleted INTEGER DEFAULT 0,  -- Soft delete
            fecha_registro TEXT NOT NULL,  -- Fecha de registro
            ultima_visita TEXT             -- Última visita
        )
        ''')

        # Tabla de Citas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,       -- Fecha de la cita
            time TEXT NOT NULL,       -- Hora de la cita
            duration INTEGER,         -- Duración en minutos
            notes TEXT,               -- Notas adicionales
            especialidad TEXT,        -- Especialidad requerida
            status TEXT DEFAULT 'Pendiente',  -- Estado: Pendiente, Atendido, Cancelado
            tipo_cita_id INTEGER,     -- Tipo de cita (relación con appointment_types)
            is_deleted INTEGER DEFAULT 0,  -- Soft delete
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id),
            FOREIGN KEY(tipo_cita_id) REFERENCES appointment_types(id)
        )
        ''')

        # Tabla de Tipos de Cita
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE  -- Ejemplo: Consulta, Limpieza, Ortodoncia, etc.
        )
        ''')

        # Tabla de Tratamientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,  -- Nombre del tratamiento
            description TEXT,           -- Descripción del tratamiento
            cost REAL NOT NULL          -- Costo del tratamiento
        )
        ''')

        # Tabla de Tratamientos Aplicados (Relación entre Citas y Tratamientos)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS applied_treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER NOT NULL,
            treatment_id INTEGER NOT NULL,
            notes TEXT,  -- Notas adicionales sobre el tratamiento aplicado
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
            date TEXT NOT NULL,        -- Fecha del registro
            diagnosis TEXT NOT NULL,   -- Diagnóstico
            procedure TEXT NOT NULL,   -- Procedimiento realizado
            treatment_plan TEXT,       -- Plan de tratamiento
            notes TEXT,                -- Notas adicionales
            attachments TEXT,          -- Archivos adjuntos (JSON o texto)
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Pagos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,        -- Fecha del pago
            amount REAL NOT NULL,      -- Monto del pago
            payment_method TEXT,       -- Método de pago (Efectivo, Tarjeta, etc.)
            status TEXT DEFAULT 'Pending',  -- Estado: Pendiente, Completado
            notes TEXT,                -- Notas adicionales
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Inventario
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,        -- Nombre del artículo
            description TEXT,          -- Descripción
            quantity INTEGER NOT NULL, -- Cantidad en stock
            cost REAL NOT NULL         -- Costo unitario
        )
        ''')

        # Tabla de Odontograma
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS odontogram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            tooth_number INTEGER NOT NULL,  -- Número del diente
            condition TEXT,                 -- Condición del diente
            notes TEXT,                     -- Notas adicionales
            date TEXT NOT NULL,             -- Fecha del registro
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Seguros Médicos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS insurance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            insurance_company TEXT NOT NULL,  -- Compañía de seguros
            policy_number TEXT NOT NULL,      -- Número de póliza
            coverage_details TEXT,            -- Detalles de la cobertura
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Prescripciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,        -- Fecha de la prescripción
            medication TEXT NOT NULL,  -- Medicamento
            dosage TEXT NOT NULL,      -- Dosificación
            instructions TEXT,         -- Instrucciones adicionales
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Facturas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,        -- Fecha de la factura
            total_amount REAL NOT NULL,  -- Monto total
            status TEXT DEFAULT 'Pending',  -- Estado: Pendiente, Pagado
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        ''')

        # Tabla de Comentarios y Calificaciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,        -- Fecha del comentario
            rating INTEGER NOT NULL,   -- Calificación (1-5)
            comments TEXT,             -- Comentarios
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Horarios de Doctores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctor_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL,  -- Día de la semana (Lunes, Martes, etc.)
            start_time TEXT NOT NULL,   -- Hora de inicio
            end_time TEXT NOT NULL,     -- Hora de fin
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
        ''')

        # Tabla de Procedimientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,        -- Nombre del procedimiento
            description TEXT,          -- Descripción
            cost REAL NOT NULL,        -- Costo
            categoria TEXT,            -- Categoría
            tipo_concepto TEXT,        -- Tipo de concepto
            fecha_registro TEXT,       -- Fecha de registro
            estado TEXT DEFAULT 'Activo'  -- Estado: Activo, Inactivo
        )
        ''')

        # Tabla de Configuración
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_pago TEXT,            -- Tipo de pago (Efectivo, Tarjeta, etc.)
            moneda TEXT,               -- Moneda (PEN, USD, etc.)
            banco TEXT,                -- Banco
            tipo_tarjeta TEXT          -- Tipo de tarjeta (Visa, MasterCard, etc.)
        )
        ''')

        # Índices para mejorar el rendimiento de las consultas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id ON appointments(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_doctor_id ON appointments(doctor_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_history ON history(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_odontogram ON odontogram(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patient_id_payments ON payments(patient_id)')

        conn.commit()

# Llamada a la función para crear las tablas al importar el módulo
create_tables()