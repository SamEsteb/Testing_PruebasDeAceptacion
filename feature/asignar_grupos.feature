Feature: Asignar estudiantes a grupos

    Como profesor
    Quiero asignar estudiantes a grupos existentes
    Para que puedan resolver series de ejercicios

    Scenario: Asignar estudiante correctamente a un grupo
        Given existe un estudiante con los datos "A001" , "Samuel", "Coña", "samuel.coña@email.com", "samuel123", "Ingeniería" y un grupo con nombre "Grupo 1" y curso "101"
        When asigno el estudiante al grupo
        Then debería ver un mensaje de éxito

    Scenario: Intentar asignar a un estudiante que no existe
        Given existe un grupo con nombre "Grupo 1" y curso "101"
        When intento asignar al estudiante "A999" al grupo
        Then debería ver un mensaje de error indicando que el estudiante no existe

    Scenario: Remover estudiante de un grupo correctamente
        Given existe un estudiante "S003" asignado al grupo "Grupo C" del curso "102"
        When remuevo al estudiante "S003" del grupo "Grupo C" del curso "102"
        Then debería ver un mensaje de éxito por remoción