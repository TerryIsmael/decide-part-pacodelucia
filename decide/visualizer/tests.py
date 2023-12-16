from django.utils import timezone
from django.urls import reverse
from base.tests import BaseTestCase
from census.models import Census
from store.models import Vote
from visualizer.models import Stats
from voting.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
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
from django.conf import settings


class StatsViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.question = Question(desc='Test Question')
        self.question.save()
        self.auth = Auth(name=settings.BASEURL , url=settings.BASEURL, me=True)
        self.auth.save()
        self.voting = Voting(name='Test Voting', question=self.question, start_date=timezone.now())
        self.voting.save()
        self.voting.auths.set([self.auth])
        self.voting.save()
        self.census1 = Census(voting_id=self.voting.id, voter_id=1)
        self.census1.save()
        self.census2 = Census(voting_id=self.voting.id, voter_id=2)
        self.census2.save()
        self.vote1 = Vote(voting_id=self.voting.id, voter_id=1)
        self.vote1.save()
        self.vote2 = Vote(voting_id=self.voting.id, voter_id=2)
        self.vote2.save()
        self.stats = Stats(voting=self.voting)
        self.stats.save()

    def tearDown(self):
        super().tearDown()

    def test_stats(self):
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['voting'], self.voting.id)
        self.assertEqual(response.json()['votes'], 2)
        self.assertEqual(response.json()['census'], 100.0)
        self.assertEqual(response.json()['question'], 'Test Question')
    
    def test_stats_no_votes(self):
        self.vote1.delete()
        self.vote2.delete()
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 0)


    def test_simpleVisualizer(self):        
            q = Question(desc='test question')
            q.save()
            v = Voting(name='test voting', question=q)
            v.save()
            response =self.driver.get(f'{self.live_server_url}/visualizer/{v.pk}/')
            vState= self.driver.find_element(By.TAG_NAME,"h2").text
            self.assertTrue(vState, "Votación no comenzada")

    def test_stats_no_census(self):
        self.census1.delete()
        self.census2.delete()
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['census'], 0.0)

    def test_stats_invalid_voting_id(self):
        response = self.client.get(reverse('stats', kwargs={'voting_id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_stats_with_multiple_votes(self):
        Vote.objects.create(voting_id=self.voting.id, voter_id=3)
        Vote.objects.create(voting_id=self.voting.id, voter_id=4)
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 4)

    def test_stats_with_multiple_census(self):
        Census.objects.create(voting_id=self.voting.id, voter_id=3)
        Census.objects.create(voting_id=self.voting.id, voter_id=4)
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['census'], 50.0)


    def test_stats_with_no_votes_or_census(self):
        self.vote1.delete()
        self.vote2.delete()
        self.census1.delete()
        self.census2.delete()
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 0)
        self.assertEqual(response.json()['census'], 0.0)

    def test_stats_with_census_no_votes(self):
        Vote.objects.all().delete()
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 0)
        self.assertEqual(response.json()['census'], 0.0)

    def test_stats_with_votes_and_census(self):
        Census.objects.create(voting_id=self.voting.id, voter_id=3)
        Census.objects.create(voting_id=self.voting.id, voter_id=4)
        Vote.objects.create(voting_id=self.voting.id, voter_id=3)
        Vote.objects.create(voting_id=self.voting.id, voter_id=4)
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 4)
        self.assertEqual(response.json()['census'], 100.0)

    def test_stats_with_votes_no_census(self):
        Vote.objects.all().delete()
        Census.objects.all().delete()
        Vote.objects.create(voting_id=self.voting.id, voter_id=3)
        Vote.objects.create(voting_id=self.voting.id, voter_id=4)
        response = self.client.get(reverse('stats', kwargs={'voting_id': self.voting.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votes'], 2)
        self.assertEqual(response.json()['census'], 0.0)
