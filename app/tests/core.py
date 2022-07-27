import sys
from pathlib import Path

root = str(Path(__file__).parent.parent.resolve())
if root not in sys.path:
    sys.path.insert(1, root)

from main import app
from db import get_session
from tests.test_db import get_session as test_session


app.dependency_overrides[get_session] = test_session
router = app.router





