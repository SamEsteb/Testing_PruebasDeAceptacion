Feature: Crear series de ejercicios
  Como profesor
  Quiero crear y definir nuevas series de ejercicios, y poder asignarlas a los grupos que superviso,
  para organizar actividades para mis estudiantes.

  Scenario: Crear una serie exitosamente y asignarla a un grupo
    Given soy un profesor autenticado
    When ingreso el nombre "Serie de Álgebra", activo la serie y la asigno al grupo "Grupo Ejemplo"
    And presiono el botón de crear serie  
    Then la serie "Serie de Álgebra" debe guardarse en la base de datos
    And debo ver un mensaje de éxito
    And debo ver la serie "Serie de Álgebra" en el listado
    And la serie "Serie de Álgebra" debe estar asignada al grupo "Grupo Ejemplo"