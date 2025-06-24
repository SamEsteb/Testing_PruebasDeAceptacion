Feature: Crear series de ejercicios
  Como profesor
  Quiero crear series de ejercicios
  Para asignarlas posteriormente a mis estudiantes

  Scenario: Crear una serie exitosamente
    Given soy un profesor autenticado
    When ingreso el nombre "Serie de Algebra" y activo la serie
    And presiono el botón de crear serie
    Then la serie debe guardarse en la base de datos
    And debo ver la serie en el listado