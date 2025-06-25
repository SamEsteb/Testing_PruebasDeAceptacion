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

  Scenario: Intentar crear una serie con un nombre ya existente y asignarla a un grupo
    Given soy un profesor autenticado
    And existe una serie llamada "Serie de Álgebra" asignada al grupo "Grupo Ejemplo"
    When ingreso el nombre "Serie de Álgebra", activo la serie y la asigno al grupo "Grupo Ejemplo"
    And presiono el botón de crear serie
    Then la serie "Serie de Álgebra" no debe duplicarse en la base de datos
    And debo ver un mensaje de error indicando "Ya existe una serie con ese nombre asignada a este grupo."
  
  Scenario: Intentar crear una serie sin proporcionar un nombre
    Given soy un profesor autenticado
    When dejo el campo de nombre vacío, activo la serie y la asigno al grupo "Grupo Temporal"
    And presiono el botón de crear serie
    Then la serie no debe guardarse en la base de datos
    And debo ver un mensaje de error indicando "El nombre de la serie es requerido"
    And no debo ver la serie en el listado