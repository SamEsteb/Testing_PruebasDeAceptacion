Feature: Asignar estudiantes a grupos

    Como profesor
    Quiero asignar estudiantes a grupos existentes
    Para que puedan resolver series de ejercicios

    Scenario: Asignar estudiante correctamente a un grupo
        Given existe un estudiante con los datos "A001" , "Samuel", "Coña", "samuel.coña@email.com", "samuel123", "Ingeniería" y un grupo con nombre "Grupo 1" y curso "101"
        When asigno el estudiante al grupo
        Then debería ver un mensaje de éxito
