# APP odontoClinic

odontoclinic/
├── main.py               # Punto de entrada principal de la aplicación.
├── database/             # Lógica relacionada con la base de datos.
│   ├── db_config.py      # Configuración inicial y conexión.
│   ├── models.py         # Modelos para manejar las tablas.
├── modules/              # Cada funcionalidad es un módulo independiente.
│   ├── login.py          # Módulo para el login.
│   ├── appointments.py   # Módulo para gestión de citas.
│   ├── patients.py       # Módulo para gestión de pacientes.
│   ├── billing.py        # Módulo para el estado de cuenta.
│   ├── history.py        # Módulo para la historia clínica.
├── assets/               # Archivos estáticos como imágenes, íconos, etc.
│   ├── radiografias/     # Carpeta para guardar radiografías.
├── utils/                # Utilidades compartidas.
│   ├── helpers.py        # Funciones comunes (e.g., validaciones).
├── requirements.txt      # Dependencias del proyecto.
└── README.md             # Documentación del proyecto.
