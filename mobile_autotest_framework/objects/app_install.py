# -*- coding:utf-8 -*-

import logging
from framework.base import Base
from objects.guide_page import title_id

logger = logging.getLogger('ClassBox')


class AppInstall(Base):

    def find_title(self):
        logger.info("    确定找到title '掌上校园' ")
        return self.find_element_by_id(title_id).text
