# -*- coding:utf-8 -*-
from framework.base import Base
title_id = 'title_tx'


class AppInstall(Base):

    def find_title(self):
        return self.find_element_by_id(title_id).text