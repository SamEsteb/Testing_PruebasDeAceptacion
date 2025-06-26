Feature: Registro de un nuevo ususario den el sistema
    Como un usuario nuevo, quiero poder registrarme en el sistema para acceder
    a las funcionalidades correspondientes a mi rol. Esto es esencial
    porque es el punto de entrada al sistema.

    Scenario: Registro exitoso de un nuevo Estudiante
        Given que me encuentro en la página de registro
        When ingreso un nombre válido "Osvaldo"
        And ingreso un apellido válido "Norma Cabalga"
        And ingreso mi numero de matricula "2023-AB-001"
        And ingreso un correo electrónico unico "osvaldo.caba@uest.com"
        And ingreso una contraseña segura "password123"
        And ingreso una carrera válida "Ingeniería de Sistemas"
        And hago clic en el botón "Registrar Estudiante"
        Then soy redirigido a la página de inicio de sesión o mi sesión se inicia automáticamente
        And un nuevo registro de 'Estudiante' debe existir en la base de datos con el correo "osvaldo.caba@uest.com"
    