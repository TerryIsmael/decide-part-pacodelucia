from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from base.models import Auth
from django.conf import settings
from django.utils import timezone

from voting.models import Question, Voting, QuestionOption

import pytest
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

class VisualizerTestCase(StaticLiveServerTestCase):
    def create_votings(self):
        q = Question(desc="Pregunta prueba")
        q.save()
        for i in range(3):
            opt = QuestionOption(question=q, option="opción {}".format(i + 1))
            opt.save()
        voting_open = Voting(
            name="Pregunta prueba", question=q, start_date=timezone.now()
        )
        voting_open.save()
        voting_closed = Voting(
            name="test voting closed", question=q, start_date=timezone.now()
        )
        voting_closed.save()
        voting_not_started = Voting(name="test voting not started", question=q)
        voting_not_started.save()
        auth, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        auth.save()
        voting_open.auths.add(auth)
        voting_closed.auths.add(auth)
        voting_not_started.auths.add(auth)
        # Close voting
        voting_closed.end_date = timezone.now()
        voting_closed.save()
        return voting_open, voting_closed, voting_not_started

    def setUp(self):
        (
            self.voting_open,
            self.voting_closed,
            self.voting_not_started,
        ) = self.create_votings()
        # Selenium Setup
        self.base = BaseTestCase()
        self.base.setUp()
        # Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_votacion_abierta(self):
     
        self.driver.get(f"{self.live_server_url}/visualizer/{self.voting_open.id}")
        self.assertTrue(len(self.driver.find_elements(By.ID, "app-visualizer")) == 1)
        self.assertTrue(
            len(
                self.driver.find_elements(
                    By.XPATH, "//*[contains(text(), 'Votación en curso')]"
                )
            )
            == 1
        )  


    def test_votacion_no_empezada(self):
        self.driver.get(
            f"{self.live_server_url}/visualizer/{self.voting_not_started.id}"
        )
        self.assertTrue(len(self.driver.find_elements(By.ID, "app-visualizer")) == 1)
        self.assertTrue(
            len(
                self.driver.find_elements(
                    By.XPATH, "//*[contains(text(), 'Votación no comenzada')]"
                )
            )
            == 1
        )  
