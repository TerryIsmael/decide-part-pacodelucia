from django_nose import NoseTestSuiteRunner
import os
from django.conf import settings

class CustomNoseTestSuiteRunner(NoseTestSuiteRunner):
    def setup_test_environment(self, **kwargs):

        print("\nSetting up frontend test environment...")

        os.system("kill $(ps aux | grep -E 'node .*/node_modules/.bin/vite' | grep 'decide' | awk '{print $2}') 2>/dev/null")
        os.environ["VITE_API_URL"] = f"http://localhost:{settings.BACKEND_TEST_PORT}/"
        os.system(f"cd ../decide-frontend && nohup npm run dev -- --host 0 --port {settings.FRONTEND_TEST_PORT} &")
        print(f"FRONTEND URL: http://localhost:{settings.FRONTEND_TEST_PORT}")

        print("\nSetting up backend test environment...")
        print(f"BACKEND URL: http://localhost:{settings.BACKEND_TEST_PORT}")

        NoseTestSuiteRunner.setup_test_environment(self, **kwargs)

    def teardown_test_environment(self, **kwargs):
        os.system("kill $(ps aux | grep -E 'node .*/node_modules/.bin/vite' | grep 'decide' | awk '{print $2}') 2>/dev/null")

        NoseTestSuiteRunner.teardown_test_environment(self, **kwargs)