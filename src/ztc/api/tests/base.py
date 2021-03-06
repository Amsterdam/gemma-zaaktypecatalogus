import warnings

from rest_framework.test import APITestCase as _APITestCase
from zds_schema.tests import JWTScopesMixin, get_operation_url

from ...datamodel.tests.factories import CatalogusFactory
from ..scopes import SCOPE_ZAAKTYPES_READ


class ClientAPITestMixin(JWTScopesMixin):

    scopes = [
        SCOPE_ZAAKTYPES_READ
    ]

    @property
    def api_client(self):
        warnings.warn("Use the built in `self.client` instead of `self.api_client`", DeprecationWarning)
        return self.client


class CatalogusAPITestMixin:
    API_VERSION = '1'

    def setUp(self):
        super().setUp()

        self.catalogus = CatalogusFactory.create(domein='ABCDE', rsin='000000001')

        self.catalogus_list_url = get_operation_url('catalogus_list')
        self.catalogus_detail_url = get_operation_url('catalogus_read', uuid=self.catalogus.uuid)


class APITestCase(ClientAPITestMixin, CatalogusAPITestMixin, _APITestCase):
    pass
