import re
import unittest
import threading
import time
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # if firefox are not start, ignore these test
        if cls.client:
            # create application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
            # forbidden log function
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')
            # create database, and insert some data
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)
            # add administrator
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            threading.Thread(target=cls.app.run).start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/main/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available.')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # enter index page
        self.client.get('http://localhost:5000/main/index')
        self.assertTrue(re.search('Hello,\s+Stranger', self.client.page_source))

        # enter login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # login
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john', self.client.page_source))

        # commit page content(add new page)
        insert_content = 'new article'
        self.client.find_element_by_name('body').send_keys(insert_content)
        self.client.find_element_by_name('submit').click()
        self.assertTrue(insert_content in self.client.page_source)

        # enter user's information page
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>john</h1>' in self.client.page_source)

        # enter moderate comments page
        self.client.find_element_by_link_text('Moderate Comments').click()
        self.assertTrue('<h1>Comment Moderation</h1>' in self.client.page_source)

    def test_edit_profile_page(self):
        self.client.get('http://localhost:5000/main/user/john')
        self.assertTrue('<h1>john</h1>' in self.client.page_source)

        # edit user information
        self.client.find_element_by_link_text('Edit Profile').click()
        self.assertTrue(re.search('Edit\s+your\s+profile', self.client.page_source))

        # commit user edition information
        self.client.find_element_by_name('submit').click()
        self.assertTrue('Your profile has been updated' in self.client.page_source)

        # edit user [admin] information
        self.client.find_element_by_link_text('Edit Profile [Admin]').click()
        self.assertTrue(re.search('Edit\s+your\s+profile', self.client.page_source))

        # commit user edition [admin] information
        self.client.find_element_by_name('submit').click()
        self.assertTrue('<h3>Posts by john</h3>' in self.client.page_source)

    def test_edit_post_page(self):
        self.client.get('http://localhost:5000/main/post/1')
        post_content = Post.query.filter_by(id=1).first().body
        self.assertTrue(post_content in self.client.page_source)

        # commit comments(add new comment)
        self.client.find_element_by_name('body').send_keys('a list of words')
        self.client.find_element_by_name('submit').click()
        self.assertTrue('Your comment has been published' in self.client.page_source)

