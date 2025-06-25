from database.models import Serie, Grupo, Curso, serie_asignada 
from DBManager import db
from sqlalchemy import text

class SerieService:
    @staticmethod
    def create_serie(nombre, activa, grupo_nombre=None):
        """
        Crea una nueva serie de ejercicios y opcionalmente la asigna a un grupo
        interactuando directamente con la tabla de asociación.
        No se puede crear una serie ya existente o con el mismo nombre en el mismo grupo.
        No se puede crear una serie con nombre vacío.
        """
        try:
            if not nombre or nombre.strip() == "":
                raise ValueError("El nombre de la serie es requerido")
            
            if not grupo_nombre or grupo_nombre.strip() == "":
                raise ValueError("La serie se debe asignar a un grupo")

            if grupo_nombre:
                existing_serie = Serie.query.filter_by(nombre=nombre).first()
                existing_grupo = Grupo.query.filter_by(nombre=grupo_nombre).first()
                if existing_serie and existing_grupo:
                    assignment_exists = db.session.query(serie_asignada).filter(
                        serie_asignada.c.id_serie == existing_serie.id,
                        serie_asignada.c.id_grupo == existing_grupo.id
                    ).first()
                    if assignment_exists:
                        raise ValueError("Ya existe una serie con ese nombre asignada a este grupo.")

            new_serie = Serie.query.filter_by(nombre=nombre).first()
            if not new_serie:
                new_serie = Serie(nombre=nombre, activa=activa)
                db.session.add(new_serie)
                db.session.commit()
                db.session.refresh(new_serie)

            if grupo_nombre:
                grupo = Grupo.query.filter_by(nombre=grupo_nombre).first()

                if not grupo:
                    dummy_curso = Curso.query.filter_by(nombre="Curso General Para Grupos").first()
                    if not dummy_curso:
                        dummy_curso = Curso(nombre="Curso General Para Grupos", activa=True)
                        db.session.add(dummy_curso)
                        db.session.commit()
                        db.session.refresh(dummy_curso)
                    
                    grupo = Grupo(nombre=grupo_nombre, id_curso=dummy_curso.id)
                    db.session.add(grupo)
                    db.session.commit()
                    db.session.refresh(grupo)

                assignment_exists = db.session.query(serie_asignada).filter(
                    serie_asignada.c.id_serie == new_serie.id,
                    serie_asignada.c.id_grupo == grupo.id
                ).first()

                if not assignment_exists:
                    insert_stmt = serie_asignada.insert().values(
                        id_serie=new_serie.id, 
                        id_grupo=grupo.id
                    )
                    db.session.execute(insert_stmt)
                    db.session.commit()
            
            return new_serie
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear serie o asignarla a un grupo: {e}")
            raise e

    @staticmethod
    def get_serie_by_nombre(nombre):
        """Obtiene una serie por su nombre."""
        return Serie.query.filter_by(nombre=nombre).first()

    @staticmethod
    def get_serie_by_id(serie_id):
        """Obtiene una serie por su ID."""
        if not serie_id or serie_id <= 0:
            raise ValueError("ID de serie inválido")
        return Serie.query.get(serie_id)

    @staticmethod
    def get_all_series():
        """Obtiene todas las series."""
        return Serie.query.all()

    @staticmethod
    def is_serie_assigned_to_group(serie_nombre, grupo_nombre):
        """
        Verifica si una serie está asignada a un grupo específico
        consultando directamente la tabla de asociación.
        """
        serie = Serie.query.filter_by(nombre=serie_nombre).first()
        grupo = Grupo.query.filter_by(nombre=grupo_nombre).first()

        if not serie or not grupo:
            return False
        
        assignment_exists = db.session.query(serie_asignada).filter(
            serie_asignada.c.id_serie == serie.id,
            serie_asignada.c.id_grupo == grupo.id
        ).first()

        return assignment_exists is not None
