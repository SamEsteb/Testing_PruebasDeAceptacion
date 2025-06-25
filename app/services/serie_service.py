from DBManager import db
from database.models import Serie, Supervisor # Make sure these imports are correct based on your file structure

class SerieService:
    @staticmethod
    def create_serie(nombre: str, activa: bool) -> Serie:
        try:
            new_serie = Serie(nombre=nombre, activa=activa)
            db.session.add(new_serie)
            db.session.commit()
            db.session.refresh(new_serie)

            print(f"Serie '{nombre}' created successfully with ID: {new_serie.id}")
            return new_serie
        except Exception as e:
            db.session.rollback()
            print(f"Error creating series '{nombre}': {e}")
            raise 

    @staticmethod
    def get_serie_by_nombre(nombre: str) -> Serie | None:
        try:
            serie = Serie.query.filter_by(nombre=nombre).first()
            return serie
        except Exception as e:
            print(f"Error retrieving series by name '{nombre}': {e}")
            return None

    @staticmethod
    def get_all_series() -> list[Serie]:
        try:
            all_series = Serie.query.all()
            return all_series
        except Exception as e:
            print(f"Error retrieving all series: {e}")
            return []

