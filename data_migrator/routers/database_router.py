class ReadOnlyDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'read_replica':
            return 'read_replica'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'read_replica':
            return False
        return True
