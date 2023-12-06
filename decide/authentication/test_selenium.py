from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class AdminTestCase(StaticLiveServerTestCase):

    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()
	
        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_simpleCorrectLogin(self):      
       #Abre la ruta del navegador             
        self.driver.get(f'{self.live_server_url}/admin/')
       #Busca los elementos y “escribe”
        self.driver.find_element(By.ID,'id_username').send_keys("admin")
        self.driver.find_element(By.ID,'id_password').send_keys("qwerty",Keys.ENTER)
        
       #Verifica que nos hemos logado porque aparece la barra de herramientas superior
        self.assertTrue(len(self.driver.find_elements(By.ID, 'user-tools'))==1)
        
    def test_simpleWrongLogin(self):

        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID,'id_username').send_keys("WRONG")
        self.driver.find_element(By.ID,'id_password').send_keys("WRONG")       
        self.driver.find_element(By.ID,'login-form').submit()

       #Si no, aparece este error
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME,'errornote'))==1)
        time.sleep(5)

class VoterTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.port = 8000
        super().setUpClass()

    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()
	
        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_loginfakeuser(self):
        self.driver.get("http://localhost:5173/")
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
        self.driver.get("http://localhost:5173/")
        self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("noadmin")
        self.driver.find_element(By.ID, "password").send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR, ".login-button").click()
        # wait until something in the page changes (in this case, a div appears)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message")))
        message = self.driver.find_element(By.CSS_SELECTOR, ".success-message").text
        self.assertEquals(message, "Bienvenido noadmin")
        