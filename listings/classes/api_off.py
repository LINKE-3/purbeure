"""API request for get product"""
import requests


class ApiOff:

	def __init__(self):
		self.search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'

	def research_products(self, category, quantity):
		"""Research and return the first product found
		according to the research terms
		"""
		params = {'search_terms' : category, 'json' : 1, 'page_size' : quantity}
		api_get = requests.get(self.search_url, params=params).json()
		try:
			products = api_get['products']
		except:
			return False
		else:
			result = []
			for count, product in enumerate(products):
				if len(result) < quantity:
					try:
						product = {'name': products[count]['product_name_fr'],
								   'nutriscore': products[count]['nutriments']['nutrition-score-fr'],
								   'nutrigrade' : products[count]['nutrition_grade_fr'].upper(),
								   'image_url': products[count]['image_front_url'],
								   'url' : products[count]['url'],
								   'salt' : products[count]['nutriments']['salt'],
								   'sugar' : products[count]['nutriments']['sugars'],
								   'fat' : products[count]['nutriments']['fat'],
								   'calories' : products[count]['nutriments']['energy_value']}
					except IndexError:
						break
					except:
						continue
					else:
						result.append(product)
			return result
