# import django deps
from django.test import TestCase

# import c3po deps
from c3po.options import ModelTranslationOptions
from c3po.tests.base import MockModel, MockModelOptions


# class to test the translation options class
class ModelTranslationOptionsTestCase(TestCase):
    def test_base_class(self):
        trans_opts = ModelTranslationOptions(MockModel)
        self.assertEqual(MockModel, trans_opts.model)
        self.assertEqual((), trans_opts.attributes)
        self.assertEqual(u'tests_mockmodel_translation', trans_opts.db_table)
        self.assertEqual(u'translations', trans_opts.related_name)

    def test_sublass(self):
        # test options when subclassed
        trans_opts = MockModelOptions(MockModel)
        self.assertEqual(MockModel, trans_opts.model)
        self.assertEqual(
            ('test_field_1', 'test_field_2'), trans_opts.attributes)
        self.assertEqual(u'tests_mockmodel_translation', trans_opts.db_table)
        self.assertEqual(u'translations', trans_opts.related_name)
