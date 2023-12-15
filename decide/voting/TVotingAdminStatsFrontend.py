
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLoadVotingAdminStatsTestSuccess():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_loadVotingAdminStatsTestSuccess(self):
    self.driver.get("http://localhost:5173/admin/voting/stats")
    self.driver.set_window_size(1064, 691)
    self.driver.find_element(By.CSS_SELECTOR, "#app > #app").click()
  
  def test_testcheck2(self):
    self.driver.get("http://localhost:5173/admin/voting/stats")
    self.driver.set_window_size(1064, 692)
    h2_element = self.driver.find_element(By.CSS_SELECTOR, "h2")
    assert h2_element.text == "Datos de Votaciones"
  
