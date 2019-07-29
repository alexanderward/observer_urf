import os
if os.environ.get("environment", "local") == 'PROD':
    from .prod import *
else:
    from .local import *
