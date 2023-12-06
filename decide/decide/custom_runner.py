from django_nose import NoseTestSuiteRunner
import os
from django.conf import settings

class CustomNoseTestSuiteRunner(NoseTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        os.system("kill $(ps aux | grep 'npm run dev' | awk '{print $2}' | head -n 1)")
		
        os.system(f"API_BASE_URL=http://localhost:8000 && cd ../decide-frontend && nohup npm run dev -- --host 0 &")
        os.system(f"FRONTEND_URL=http://localhost:5173")
		
        NoseTestSuiteRunner.setup_test_environment(self, **kwargs)

    def teardown_test_environment(self, **kwargs):
        os.system("kill $(ps aux | grep 'npm run dev' | awk '{print $2}' | head -n 1)")

        NoseTestSuiteRunner.teardown_test_environment(self, **kwargs)