from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase): #extends test case
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') #matches every string past domain name #ex: app.me(**after this domain name)/lisis/123ab
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() #represents url request, python abstraction for what a browser what look for that value
        response = home_page(request)
        expected_html = render_to_string('home.html') #after deleting tests below, put in this
        self.assertEqual(response.content.decode(), expected_html)

class NewListTest(TestCase):
    def test_home_can_save_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data = {'item_text' : 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'item_text' : 'A new list item'}
        )
        self.assertRedirects(response, '/lists/the-only-list/')

class ListViewTest(TestCase):

        def test_uses_list_template(self):
            response = self.client.get('/lists/the-only-list/')
            self.assertTemplateUsed(response, 'list.html')

        def test_displays_all_items(self):
            new_list = List.objects.create()
            Item.objects.create(text= 'itemey 1', list = new_list)
            Item.objects.create(text='itemey 2', list = new_list)

            response = self.client.get('/lists/the-only-list/')

            self.assertContains(response, 'itemey 1')
            self.assertContains(response, 'itemey 2')

class ItemAndListModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = new_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, new_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, new_list)


        # self.assertTrue(response.content.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', response.content)
        # self.assertTrue(response.content.strip().endswith('</html>'))


        # class SmokeTest(TestCase):
        #     def test_bad_maths(self): #failing test
        #         self.assertEqual(1+1,3)
