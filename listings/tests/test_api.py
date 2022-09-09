from django.test import TestCase
from mock import patch
from listings.classes.api_off import ApiOff

# Create your tests here.

class ApiOpenFood(TestCase):
    """Contain the test for the OpenFoodFact Api"""

    def setUp(self):
        """
        self.list is a list that should be contained into a dict index
        'products', I'm using just the list because I need this contain to
        multiplicate it into the dict.
        Response is a expected result for a self.list, can be multiplicate aswell
        """
        self.api = ApiOff()
        self.list = [
            {
                'product_name_fr': 'name',
                'image_front_url': 'image_url',
                'nutrition_grade_fr':'e',
                'nutriments':{
                    'nutrition-score-fr':25,
                    'salt': 0.1,
                    'sugars': 56.3,
                    'fat': 30.9,
                    'energy_value': 50,
                },
                'categories': 'Pate à pain',
                'url': 'url.com'
            }
        ]

        self.response = [
            {
                'name': 'name',
                'nutriscore': 25,
                'nutrigrade': 'E',
                'image_url': 'image_url',
                'url': 'url.com',
                'salt': 0.1,
                'sugar': 56.3,
                'fat': 30.9,
                'calories': 50,
            }
        ]


    def get_api_result(self, quantity=1):
        """set the api_result with how many results you want"""
        api_result = {'products' : self.list * quantity}
        return api_result

    @patch('requests.get')
    def test_less_result_than_quantity(self, mock_api):
        """Testing asking for 5 products when there is only one result"""
        api_result = self.get_api_result()
        mock_api.return_value.json.return_value = api_result
        self.assertEqual(self.response, self.api.research_products('test', 5))


    @patch('requests.get')
    def test_more_result_than_quantity(self, mock_api):
        """Testing asking for 5 products when there are 10 results"""
        api_result = self.get_api_result(10)
        mock_api.return_value.json.return_value = api_result
        self.assertEqual(self.response * 5, self.api.research_products('test', 5))
        self.assertEqual(len(self.api.research_products('test', 5)), 5)

    @patch('requests.get')
    def test_as_result_as_quantity(self, mock_api):
        """Testing asking for 5 products when there are 5 results"""
        api_result = self.get_api_result(5)
        mock_api.return_value.json.return_value = api_result
        self.assertEqual(self.response * 5, self.api.research_products('test', 5))
        self.assertEqual(len(self.api.research_products('test', 5)), 5)

    @patch('requests.get')
    def test_no_result(self, mock_api):
        """Testing a failing result"""
        mock_api.return_value.json.return_value = 'No valuable value, yes I wrote that'
        self.assertFalse(self.api.research_products('test', 5))

