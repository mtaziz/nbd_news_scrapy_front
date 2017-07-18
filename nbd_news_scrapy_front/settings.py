# coding: utf8
is_development = True

if is_development:
    from settings_dev import *
else:
    from settings_pro import *