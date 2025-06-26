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

    Scenario: Registro exitoso de un nuevo Supervisor
        Given que me encuentro en la página de registro
        When ingreso un nombre válido "Ana"
        And ingreso un apellido válido "Gómez de la Vega"
        And ingreso un correo electrónico único "ana.govega@usuper.com"
        And ingreso una contraseña segura "securePass456"
        And hago clic en el botón "Registrar Supervisor"
        Then soy redirigido a la página de inicio de sesión o mi sesión se inicia automáticamente
        And un nuevo registro de 'Supervisor' debe existir en la base de datos con el correo "ana.govega@usuper.com"

     Scenario: Intento de registro con correo electrónico ya existente
        Given que ya existe un 'Estudiante' con el correo electrónico "pablo.neruda@uest.com"
        And me encuentro en la página de registro
        When intento registrar un 'Supervisor' con el correo electrónico "pablo.neruda@uest.com"
        Then el sistema debe mostrar un mensaje de error indicando que el correo electrónico ya está en uso
        And no se debe crear un nuevo registro de 'Supervisor' en la base de datos
    