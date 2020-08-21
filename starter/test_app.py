
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Actor, Movie, setup_db
from app import create_app
from models import db
from datetime import datetime

'''
Casting Assistant

    Can view actors and movies:

Casting Director

    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies


Executive Producer

    All permissions a Casting Director has and…
    Add or delete a movie from the database

'''

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()
        #fake data 
        Movie(title = 'Godzila' , relaseData = datetime(20,2,11)).insert()
        Movie(title = 'Ahmad' , relaseData = datetime(20,2,11)).insert()
        Actor(name = "Ahmad" , age = 22 , gender = 'M').insert()
        Actor(name = "Ali" , age = 27 , gender = 'M').insert()

        self.Executive_Producer_Token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpCd0ZKVXFibjRsMUE5b3E0aXcxUCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZ3MzaXVmai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZTY4YzhhOWNlZDkwMDE5ZDM4MzI0IiwiYXVkIjoiYXV0aFRlc3QiLCJpYXQiOjE1OTgwNDM2MjIsImV4cCI6MTU5ODA1MDgyMiwiYXpwIjoiR095cWtqV25GcWlNcGpKOTdOelVueGhXa1c4ZFR1ajgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzICIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzICIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ZeNgPggK4gbiJC4rWn5BLUqOxl9a6avPes2lWvV6iNqNgfcDzEI87XLckNqNPPcIpUR0Dv4oWSpqmlwmPpNyDNU7e_EiR4oGRodVacpO39BevY1ANoLQtM24413lVJnlhz9lZDn6_KmSLaXoDa4kpGKbZ9g60nvBs6TFkz4DQiNYOUE1VX6LH9I9wqIBKxdKtenDlqsS0veacjiGaANPHH0SuDV2AyeR2yM9TyZcX7hjq6yk3-DT6VKmaV269yi0AxiWm4gxO3JQlzlbvFt_jXpscO6keNORdpCEFDUDnBp0-fAuVvDWCQvKiq00mqv2_JP_Gqy4uDQ1dNGZzOCEJw"

        self.Casting_Director_Token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpCd0ZKVXFibjRsMUE5b3E0aXcxUCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZ3MzaXVmai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZTY4YzhhOWNlZDkwMDE5ZDM4MzI0IiwiYXVkIjoiYXV0aFRlc3QiLCJpYXQiOjE1OTgwNDM3MzIsImV4cCI6MTU5ODA1MDkzMiwiYXpwIjoiR095cWtqV25GcWlNcGpKOTdOelVueGhXa1c4ZFR1ajgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyAiLCJwb3N0OmFjdG9ycyJdfQ.ur3cwy_0IAwmxQteV3zIyEtbnjj0phgLy1KLnVL8dJRE4YP_2Sr2z43E1_5v7FfgAdAZVrRxi2nA2_gXYW5LHeQCvfwyTHyjkzDcqfoqBhxitM-7AlgKDsGDDhrXCUTV1sCeoLz042owdCvR97hQg3QNGbJMurr1DNvdLKEPmgUKMWMv0b3ppfyJxRSRC5I37_jjM1lsyNYUgqhtkfhOUwD2CerVSj4aKzf95GDDyUIpYHyIjjmvRlAvdDSn1ABh7iTaTNfjI6j2vAuUM3X0v2uwBGpn_Y9nWI9k0c3P2u7i_4fBFddsGnEH6wH4VgG2ZftXhc-3hODT11dMzi4mMg"

        self.Casting_Assistant_Token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpCd0ZKVXFibjRsMUE5b3E0aXcxUCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZ3MzaXVmai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZTY4YzhhOWNlZDkwMDE5ZDM4MzI0IiwiYXVkIjoiYXV0aFRlc3QiLCJpYXQiOjE1OTgwNDM2ODEsImV4cCI6MTU5ODA1MDg4MSwiYXpwIjoiR095cWtqV25GcWlNcGpKOTdOelVueGhXa1c4ZFR1ajgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Ak0kZVFg0rqXo8_zjrPrBnNXexyTH40YOkrJGIx7t9lGQ3gd7l5H7ntsnfVNy_gjWKmS6Cr0DuUrIK8jt-4hVsq31KdT0SpZi4RaDG3LaXHtOKWcfTKq6fxFzr8RvwNw_cpihnTrZXTWWvTb_OwcmiydgL9fGRCb8vW3IcCxQkMdYMaZD65i0qKW6JsOC5CmlkYxdwtOakzWnrOvNP88HFCBkRhnSO5ZE-pjPzLjcop6CGO5mSoshpk57rnq4QDopL0rKagHnFoT4Mfi-rXVu11VIQvjJo-mn7ccjM0vloufD5l8GSskeEfJJojgcnQ411FHidtf141MnlQjVTk4vg"


        self.new_movie = {
            'title': 'movie',
            'relaseData' : datetime(20,10,11)
        }


        self.new_movie_1 = {
            'title': 'WAJED',
            'relaseData' : datetime(20,10,11)
        }

        self.new_actor = {
            'name': 'Ahmad',
            'age': 24,
            'gender': 'M'
        }


        self.new_actor_1 = {
            'name': 'Ali',
            'age': 27,
            'gender': 'M'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

  

    
    def tearDown(self):
        pass

    def test_get_movies(self):
        header = {
            "authorization" : "bearer {}".format(self.Casting_Assistant_Token)
        }
        res = self.client().get('/movies' , headers=header)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_fail(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_get_actors(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Assistant_Token)
        }
        res = self.client().get('/actors'  , headers = header)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_fail(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_create_movie(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Executive_Producer_Token)
        }
        res = self.client().post('/movies/create', json=self.new_movie , headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Director_Token)
        }
        res = self.client().post('/actors/create' , json = self.new_actor, headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'Ahmad')
    


    def test_delete_movie(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Executive_Producer_Token)
        }
        res = self.client().delete('/movies/delete/1' , headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/delete/1')
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_fail_400(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Executive_Producer_Token)
        }
        res = self.client().delete('/movies/delete/1000' , headers =header)
        self.assertEqual(res.status_code, 400)
    
    def test_delete_actor(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Executive_Producer_Token)
        }
        res = self.client().delete('/actors/delete/1' , headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_actor_fail_401(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Executive_Producer_Token)
        }
        res = self.client().delete('/actors/delete/10000' , headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    
    def test_delete_actor_fail_401(self):
        res = self.client().delete('/actors/delete/1000')
        self.assertEqual(res.status_code, 401)
    
    def test_patch_movie(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Director_Token)
        }
        res = self.client().patch('/movies/patch/2', json=self.new_movie_1 , headers =header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_patch_movie_400(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Director_Token)
        }
        res = self.client().patch('/movies/patch/200', json=self.new_movie , headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
    
    def test_patch_movie_fail(self):
        res = self.client().patch('/movies/patch/2000', json=self.new_movie)
        self.assertEqual(res.status_code, 401)

    


    def test_patch_actor(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Director_Token)
        }
        res = self.client().patch('/actors/patch/2', json=self.new_actor_1 , headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_400(self):
        header = {
            "Authorization" : "Bearer {}".format(self.Casting_Director_Token)
        }
        res = self.client().patch('/actors/patch/200', json=self.new_actor , headers = header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    






if __name__ == "__main__":
    unittest.main()