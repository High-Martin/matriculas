from django.apps import AppConfig


class MatriculasappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "matriculasapp"

    def ready(self):
        from matriculasapp.dao.core.dao_factory import DaoFactory

        factory = DaoFactory()
        factory.get_filtro_alunos_dao().migrate_table()
        factory.get_filtro_cursos_dao().migrate_table()
