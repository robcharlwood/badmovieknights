# import django deps
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

# import modeli18n related dependencies
from c3po.registry import C3PORegistry
from c3po.exceptions import AlreadyRegistered
from c3po.tests.base import (
    MockModel, MockModelUnique, MockModelReservedFieldName,
    MockNotAModel, MockModelOptions, MockModelReservedOptions)


# class to test c3po model registration
class ModelRegistrationTestCase(TestCase):
    def setUp(self):
        super(ModelRegistrationTestCase, self).setUp()
        self.reg = C3PORegistry()

    def test_register_non_model(self):
        # test attempt registration of a non model class
        self.assertRaises(
            AssertionError, self.reg.register, MockNotAModel,
            MockModelOptions)

    def test_register_model(self):
        # test registering of a model
        self.reg.register(MockModel, MockModelOptions)
        self.assertEqual(len(self.reg._registry), 1)
        self.assert_(MockModel in self.reg._registry)

        # time to check the models are as they should be
        trans_model = MockModel._translation_model
        self.assertTrue(hasattr(MockModel, 'translations'))
        self.assertTrue(hasattr(MockModel, '_translation_model'))
        self.assertEqual(trans_model, MockModel._translation_model)
        self.assertTrue(hasattr(trans_model, '_transmeta'))
        trans_model._meta.get_field('language')
        trans_model._meta.get_field('model_instance')
        trans_model._meta.get_field('test_field_1')
        trans_model._meta.get_field('test_field_2')

    def test_register_model_reserved_field_name(self):
        # test that an ImproperlyConfigured exception is raised
        # if we try to pass in a model translation with a reserved
        # field name (language, model_instance)
        self.assertRaises(
            ImproperlyConfigured,
            self.reg.register,
            MockModelReservedFieldName,
            MockModelReservedOptions
        )

    def test_model_already_registered(self):
        # test model already registered
        self.reg.register(MockModel, MockModelOptions)
        self.assertRaises(
            AlreadyRegistered,
            self.reg.register, MockModel,
            MockModelOptions)

    def test_register_model_unique(self):
        # test registering of a model whose translation field is marked
        # as unique
        self.reg.register(MockModelUnique, MockModelOptions)
        self.assertEqual(len(self.reg._registry), 1)
        self.assert_(MockModelUnique in self.reg._registry)

        # grab the newly generated translation model
        trans_model = MockModelUnique._translation_model

        # test that if a field is marked as unique in the model, that the
        # same attribute is not applied to the translation model since we
        # may have the same translation for the same field in different langs
        for trans_field in trans_model._transmeta.translatable_fields:
            for model_field in trans_model._meta.fields:
                if model_field.name == trans_field:
                    self.assertFalse(model_field.unique)
                    self.assertFalse(model_field._unique)

    def test_get_registered_models(self):
        # test get_registered_models method
        self.reg.register(MockModelUnique, MockModelOptions)
        self.reg.register(MockModel, MockModelOptions)
        self.assertEqual(2, len(self.reg.get_registered_models()))
        self.assertTrue(MockModelUnique in self.reg.get_registered_models())
        self.assertTrue(MockModel in self.reg.get_registered_models())
