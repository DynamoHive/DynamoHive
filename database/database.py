import sys # make old imports work sys.modules["database"] = sys.modules[__name__] sys.modules["database.database"] = sys.modules[__name__]
from backend.database import *
