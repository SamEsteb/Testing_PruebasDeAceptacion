Feature: Asignar estudiantes a grupos

  Como profesor
  Quiero asignar estudiantes a grupos existentes
  Para que puedan resolver series de ejercicios

  Scenario: Asignar estudiante correctamente a un grupo
    Given existe un estudiante con id "1" y un grupo con id "10"
    When asigno el estudiante al grupo
    Then debería ver un mensaje de éxito
