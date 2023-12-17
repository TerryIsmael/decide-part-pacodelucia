
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from django.contrib.auth.models import User

class FrontendTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = settings.BACKEND_TEST_PORT
        super().setUpClass()

    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()

        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        #Crear votaciones y censos
        user = User.objects.get(username='noadmin')

        # crear una votación abierta, próxima y cerrada
        q = Question(desc='Descripcion')
        q.save()
        
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=q, option='opcion 2')
        opt1.save()

        self.voting1 = Voting.objects.create(name='test voting 1', question=q, desc='Voting 1 description')
        self.voting2 = Voting.objects.create(name='test voting 2', question=q, desc='Voting 2 description')
        self.voting3 = Voting.objects.create(name='test voting 3', question=q, desc='Voting 3 description')

        self.voting1.create_pubkey()
        self.voting1.start_date = timezone.now()
        self.voting1.save()

        self.voting3.create_pubkey()
        self.voting3.start_date = timezone.now() - timezone.timedelta(days=1)
        self.voting3.end_date = timezone.now()
        self.voting3.save()

        Census.objects.create(voter_id=user.pk, voting_id=self.voting1.pk)
        Census.objects.create(voter_id=user.pk, voting_id=self.voting2.pk)
        Census.objects.create(voter_id=user.pk, voting_id=self.voting3.pk)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_loginfakeuser(self):
        self.driver.get(f"http://localhost:{settings.FRONTEND_TEST_PORT}/")
        self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("test")
        self.driver.find_element(By.ID, "password").send_keys("test")
        self.driver.find_element(By.CSS_SELECTOR, ".login-button").click()
        # wait until something in the page changes (in this case, a div appears)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message")))
        message = self.driver.find_element(By.CSS_SELECTOR, ".error-message").text
        self.assertEquals(message, "Usuario o contraseña incorrectos")
    
    def test_login_success(self):
        self.driver.get(f"http://localhost:{settings.FRONTEND_TEST_PORT}/")
        self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("noadmin")
        self.driver.find_element(By.ID, "password").send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR, ".login-button").click()
        # wait until something in the page changes (in this case, a div appears)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message")))
        message = self.driver.find_element(By.CSS_SELECTOR, ".success-message").text
        self.assertEquals(message, "Bienvenido noadmin")
    
    def test_voter_votings(self):
        self.driver.get(f"http://localhost:{settings.FRONTEND_TEST_PORT}/")
        self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("noadmin")
        self.driver.find_element(By.ID, "password").send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR, ".login-button").click()

        # wait until something in the page changes (in this case, a voting-card class appears)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".voting-card")))
        open_votings_title = self.driver.find_element(By.XPATH, "//*[text()='Votaciones abiertas']")
        open_voting = self.driver.find_element(By.XPATH, "//*[text()='test voting 1']")
        next_votings_title = self.driver.find_element(By.XPATH, "//*[text()='Votaciones próximas']")
        next_voting = self.driver.find_element(By.XPATH, "//*[text()='test voting 2']")
        closed_votings_title = self.driver.find_element(By.XPATH, "//*[text()='Votaciones finalizadas']")
        closed_voting = self.driver.find_element(By.XPATH, "//*[text()='test voting 3']")

        self.assertTrue(open_votings_title.is_displayed())
        self.assertTrue(next_votings_title.is_displayed())
        self.assertTrue(closed_votings_title.is_displayed())

        self.assertTrue(open_voting.is_displayed())
        self.assertTrue(next_voting.is_displayed())
        self.assertTrue(closed_voting.is_displayed())
    
    def test_404(self):
        self.driver.get(f"http://localhost:{settings.FRONTEND_TEST_PORT}/asdfgasdf")
        message = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEquals(message, "404")