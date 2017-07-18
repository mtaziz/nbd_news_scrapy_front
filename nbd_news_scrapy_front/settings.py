is_development = False

if is_development:
    from settings_dev import *
else:
    from settings_pro import *