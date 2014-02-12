

# class to handle model translation options
class ModelTranslationOptions(object):
    """
        Encapsulates modeli18n translation options for a
        given model.

        This should be extended when defining your
        translatable models
    """
    attributes = ()
    db_table = None
    related_name = 'translations'

    def __init__(self, model):
        self.model = model
        self.db_table = '_'.join([model._meta.db_table, 'translation'])
        super(ModelTranslationOptions, self).__init__()
