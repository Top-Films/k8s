from selenium import webdriver  
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
import psycopg2
import os

class ScrapeMovies:
	def __init__(self, db_name, db_host, db_username, db_password, db_port):
		self.base_url = 'https://www.allmovie.com/genre'
		self.query = 'alltime-desc'
		self.num_movies_per_page = 20
		self.genres = [
			('action-adventure-ag100', 'Action Adventure'),
			('animation-ag102', 'Animation'),
			('anime-ag103', 'Anime'),
			('avant-garde-experimental-ag104', 'Avant Garde Experimental'),
			('biography-ag105', 'Biography'),
			('childrens-ag106', 'Childrens'),
			('comedy-ag107', 'Comedy'),
			('comedy-drama-ag108', 'Comedy Drama'),
			('crime-ag109', 'Crime'),
			('documentary-ag110', 'Documentary'),
			('drama-ag111', 'Drama'),
			('epic-ag112', 'Epic'),
			('family-ag113', 'Family'),
			('fantasy-ag114', 'Fantasy'),
			('history-ag115', 'History'),
			('horror-ag116', 'Horror'),
			('mature-ag101', 'Mature'),
			('music-ag117', 'Music'),
			('mystery-suspense-ag118', 'Mystery Suspense'),
			('romance-ag120', 'Romance'),
			('science-fiction-ag121', 'Science Fiction'),
			('silent-film-ag122', 'Silent Film'),
			('sports-ag123', 'Sports'),
			('spy-film-ag124', 'Spy Film'),
			('thriller-ag125', 'Thriller'),
			('war-ag126', 'War'),
			('western-ag127', 'Western')
		]

		self.conn = psycopg2.connect(database="db_name",
									 host="db_host",
									 user="db_user",
									 password="db_pass",
									 port="db_port")

	def scrapePage(self, driver, url):
		try:
			driver.get(url)
		except Exception as e:
			print(f"Could not get url: ${url}")
			print(e)
			
		for i in range(1, self.num_movies_per_page + 1):
			try:
				self.scrapeMovie(driver=driver, i=i)
			except Exception as e:
				print(f"Could not get movie number {i} for url {url}")
				print(e)


	def scrapeMovie(self, driver, i):
		print(f"Movie number: {i}")
		movie_wrapper_elem = driver.find_element(By.CLASS_NAME, f"num-{i}") 

		title_wrapper_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'title')
		title_elem = title_wrapper_elem.find_element(By.TAG_NAME, 'a')
		title = title_elem.text
		print(f"Title: {title}")

		directors_wrapper_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'directors')
		directors_elem = directors_wrapper_elem.find_element(By.TAG_NAME, 'a')
		director = directors_elem.text
		print(f"Director: {director}")

		year_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'movie-year')
		year = year_elem.text
		print(f"Year: {year}")

	def saveMovie(self, title, director, year):
		print('Saving movie...')

		self.conn.cursor().execute(f"INSERT INTO ")


	def main(self):
		url = f"{self.base_url}/{self.genres[0]}/{self.query}"

		options = Options()
		options.add_argument('--headless=new')

		with webdriver.Chrome(options=options) as driver: 
			self.scrapePage(driver=driver, url=url)
		
		
if __name__ == "__main__":
	db_name = os.environ.get('DB_NAME')
	db_host = os.environ.get('DB_HOST')
	db_username = os.environ.get('DB_USERNAME')
	db_password = os.environ.get('DB_PASSWORD')
	db_port = os.environ.get('DB_PORT')

	ScrapeMovies(db_name, db_host, db_username, db_password, db_port).main()