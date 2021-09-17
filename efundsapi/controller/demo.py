import logging
from efundsapi.controller.base import BaseController

LOG = logging.getLogger(__name__)


class DemoController(BaseController):

    def get_queryset(self, **search_opts):
        return search_opts

    def get_object(self, id):
        return id

    def create(self, **kwargs):
        LOG.info("create finished")
        return kwargs

    def delete(self, id):
        LOG.info("delete %s finished" % id)
        return id
