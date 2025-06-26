Feature: Subir solución de un ejercicio
  Como estudiante, quiero poder subir la solución a un ejercicio que me ha sido asignado
  para que sea evaluada.

  Scenario: Un estudiante sube una solución exitosamente
    Given que existe una serie de ejercicios "Calculo 1" con un ejercicio "Limites"
    When un estudiante sube la solución "solucion_limites.pdf" para el ejercicio "Límites" de la serie "Cálculo I"
    Then la solución "solucion_limites.pdf" queda registrada para el ejercicio "Límites" de la serie "Cálculo I"


