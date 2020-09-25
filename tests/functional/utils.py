from datetime import datetime
from functools import wraps

from selenium import webdriver

from Consts import project_dir


def screenshot_on_failure(test):
    @wraps(test)
    def decorated_test(firefox, request, *args, **kwargs):
        ARTIFACTS_DIR = project_dir / "tests" / "functional" / "artifacts"
        try:
            test(firefox, request, *args, **kwargs)
        except Exception:
            ts = datetime.now().strftime(f"%Y.%m.%d.%H.%M.%S")
            test_name = f"{request.module.__name__}.{test.__name__}"
            png = f"{test_name}.{ts}.png"
            html = f"{test_name}.{ts}.html"
            png_path = (ARTIFACTS_DIR / png).resolve()
            html_path = (ARTIFACTS_DIR / html).resolve()
            with html_path.open("w") as _dst:
                _dst.write(firefox.page_source)
            firefox.save_screenshot(png_path.as_posix())
            raise

    return decorated_test