from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        self.driver.get(f'{self.live_server_url}/admin/')
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
        
class TestLoadVotingAdminStatsTestSuccess(StaticLiveServerTestCase):
    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()
	
        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        super().setUp() 
        
  
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
  
    def test_correctLoadVotingAdminStatsTest(self):
        self.driver.get("http://localhost:5173/admin/voting/stats")
        self.driver.set_window_size(1064, 692)
        h2_element = self.driver.find_element(By.CSS_SELECTOR, "h2")
        #Comprueba que los elementos se cargaron correctamente
        assert h2_element.text == "Datos de Votaciones"
