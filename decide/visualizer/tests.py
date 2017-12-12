from django.test import TestCase
from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from voting.models import Voting, Question

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

class VisualizerTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()


    def test_simpleVisualizer(self):        
            q = Question(desc='test question')
            q.save()
            v = Voting(name='test voting', question=q)
            v.save()
            response =self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
            vState= self.driver.find_element(By.TAG_NAME,"h2").text
            self.assertTrue(vState, "Votación no comenzada")