from selenium import webdriver  
from selenium.webdriver.common.by import By
import psycopg2
import logging
import uuid
import time
import datetime
import psycopg2
import logging
import os
import datetime
import sys

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# constants
jenkinsUserId = '4308b779-f616-4ada-9ac8-4ddb27bcd749' # srv-jenkins id
genres = [
	['action-adventure-ag100', 'Action Adventure', '97128c0e-c0e9-4c0c-93bd-fdb5f7bf2c3c'],
	['animation-ag102', 'Animation', '2d44a66c-29d6-43c8-9f30-371c93073ec9'],
	['anime-ag103', 'Anime', '1fb085b3-12f9-4062-94be-34f0348a52f3'],
	['avant-garde-experimental-ag104', 'Avant Garde Experimental', '72ea1bbe-32cc-4d82-9385-f16907e6df13'],
	['biography-ag105', 'Biography', 'c4b91c13-ff2f-4cdb-80aa-77a01e43d1a7'],
	['childrens-ag106', 'Childrens', '494bbaf6-d2f2-4fe4-980c-b90ea398a98e'],
	['comedy-ag107', 'Comedy', '33a72196-1d57-4ba8-8538-6d25c2119925'],
	['comedy-drama-ag108', 'Comedy Drama', '41e2c73a-8396-42d3-8eb0-effb32a77ae3'],
	['crime-ag109', 'Crime', 'f57899bb-bae9-451c-abd5-bba97acb58a3'],
	['documentary-ag110', 'Documentary', '3ac7a1e6-2443-49d6-8160-0e90e1486fd3'],
	['drama-ag111', 'Drama', '6afedc3a-ad16-4dd9-946b-d8d5c73ec9af'],
	['epic-ag112', 'Epic', '9de7758e-9974-4dc3-af12-9b8c7f480eda'],
	['family-ag113', 'Family', '057ab3da-d8b8-45e5-9a1e-c0ce9ace997d'],
	['fantasy-ag114', 'Fantasy', '5a6c0b79-9aa4-4f21-88b8-784cda95be4f'],
	['history-ag115', 'History', '11620510-48d0-4157-b2fd-c1878f9989a9'],
	['horror-ag116', 'Horror', 'd9de27d3-a56a-412e-9085-1a9f26908dfe'],
	['mature-ag101', 'Mature', '30145432-b725-420a-a537-3697a7e9ddb8'],
	['music-ag117', 'Music', '16f0667f-68dd-4ac6-bd7a-8d7591365334'],
	['mystery-suspense-ag118', 'Mystery Suspense', 'b807b590-77f1-49aa-8dd0-81863748d89c'],
	['romance-ag120', 'Romance', '0335c01e-b63e-4977-a05a-e7f4c09ff827'],
	['science-fiction-ag121', 'Science Fiction', '47920959-4cda-43d7-90d4-a64fcc1e50bb'],
	['silent-film-ag122', 'Silent Film', 'a060ef47-5389-412b-b670-846703affcbf'],
	['sports-ag123', 'Sports', '378fa0a7-a49e-4408-a309-57f841536661'],
	['spy-film-ag124', 'Spy Film', 'f7fb53d6-b5d5-4c80-9fa7-6f538de9904e'],
	['thriller-ag125', 'Thriller', 'c2e3f791-c5e1-4be8-a8f7-4e5f58d59ccd'],
	['war-ag126', 'War', 'a12da96c-068a-4388-ab4a-57dd7132d0a3'],
	['western-ag127', 'Western', '918f037f-c91b-4fce-aadd-16b2b10008a5']
]

class ScrapeGenre():
	def __init__(self, db_name, db_host, db_username, db_password, db_port, userId, genre):
		# db conn
		self.conn = psycopg2.connect(database=db_name,
									 host=db_host,
									 user=db_username,
									 password=db_password,
									 port=db_port)

		# vars
		self.userId = userId
		self.genre = genre

		# constants
		self.num_movies_per_page = 20
		self.page_offset = 1
		self.max_retries_genre = 3
		self.max_retries_page = 5
		self.timeout_sec = 60

		# selenium driver
		self.driver = self.__init_driver()

	def scrape(self):
		# parse values from genre
		genre_url_path = self.genre[0]
		genre_name = self.genre[1]
		genre_id = self.genre[2]

		# continue until max_retries_genre exceeded
		page_error_count = 0
		page_num = 1
		while page_error_count < self.max_retries_genre:
			log.info(f"-------------------- {genre_name} ({page_num}): Errors {page_error_count}/{self.max_retries_genre} --------------------")
			url = f"https://www.allmovie.com/genre/{genre_url_path}/alltime-desc/{page_num}"
			page_error_count = page_error_count + self.__scrape_page(url, page_num, genre_name, genre_id)
			page_num = page_num + 1

		self.conn.close()
		self.driver.quit()
					
	def __scrape_page(self, url, page_num, genre_name, genre_id):
		start_time = time.time()

		# attempt to parse page max_retries_page times
		attempt_count = 1
		while attempt_count <= self.max_retries_page:
			log.info(f"Attempt {attempt_count}/{self.max_retries_page}: {url}")
			try:
				# get driver and url
				self.driver.get(url)
				self.driver.maximize_window()

				# attempt to parse all 20 movies on a page
				for movie_num in range(self.page_offset, self.num_movies_per_page + self.page_offset):
					self.__parse_movie(movie_num, genre_id)

				# page complete with more movies within the genre
				end_time = time.time()
				log.info(f"Successfully scraped {genre_name} ({page_num}): {round(end_time-start_time, 2)}s\n")
				return 0

			except Exception as e:
				# failed to parse page for unknown reason
				log.warning(f"Error on attempt {attempt_count}: {url}")
				log.warning(e)

				# increase count
				attempt_count = attempt_count + 1

				# re init driver fully
				self.driver.quit()
				self.driver = self.__init_driver()

		# failed to parse max_retries_page times
		log.error(f"Maximum attempts reached: url={url} | genre={genre_name} | page_num={page_num}\n")
		return 1
	
	def __parse_movie(self, movie_num, genre_id):
		# get wrapper element
		movie_wrapper_elem = None
		movie_wrapper_elem = self.driver.find_element(By.CLASS_NAME, f"num-{movie_num}") 
		
		# parse title
		title_wrapper_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'title')
		title_elem = title_wrapper_elem.find_element(By.TAG_NAME, 'a')
		title = title_elem.text

		# parse director
		director = None
		try:
			directors_wrapper_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'directors')
			directors_elem = directors_wrapper_elem.find_element(By.TAG_NAME, 'a')
			director = directors_elem.text
		except Exception:
			log.warning(f"No director for movie: {title}")

		# parse year
		year = None
		try:
			year_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'movie-year')
			year = year_elem.text
		except Exception:
			log.warning(f"No year for movie: {title}")

		# ensure movie does not already exist
		cursor = self.conn.cursor()
		cursor.execute('SELECT * FROM MOVIE WHERE name = %s AND year = %s', (title, year))
		if len(cursor.fetchall()) > 0:
			# ignore duplicate record
			log.info(f"Movie already exists - {movie_num}: title={title} | director={director}")
			cursor.close()
			return

		# create new record
		timestamp = datetime.datetime.now()
		id = str(uuid.uuid4())
		log.info(f"Inserting movie - {movie_num}: title={title} | director={director} | year={year} | time={timestamp} | id={id}")
		cursor.execute('INSERT INTO MOVIE (id, created_by, updated_by, created_at, updated_at, name, director, movie_genre_id, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, self.userId, self.userId, timestamp, timestamp, title, director, genre_id, year))
		self.conn.commit()
		cursor.close()

	def __init_driver(self):
		# init chrome driver for chromium browser arm64 linux
		options = webdriver.ChromeOptions()
		options.add_argument('--headless=new')
		options.add_argument("--no-sandbox")
		options.add_argument('--disable-gpu')
		options.add_argument('--disable-dev-shm-usage')

		service = webdriver.ChromeService(executable_path=r"/usr/bin/chromedriver")

		driver = webdriver.Chrome(options=options, service=service)
		driver.set_page_load_timeout(self.timeout_sec)

		return driver

if __name__ == "__main__":
	db_name = os.environ.get('DB_NAME')
	db_host = os.environ.get('DB_HOST')
	db_username = os.environ.get('DB_USERNAME')
	db_password = os.environ.get('DB_PASSWORD')
	db_port = os.environ.get('DB_PORT')
	genre_name = os.environ.get('GENRE_NAME')	

	log.info('Picked up environment variables:')
	log.info(f"db_name={db_name}")
	log.info(f"db_host={db_host}")
	log.info(f"db_username={db_username}")
	log.info(f"db_password={db_password}")
	log.info(f"genre_name={genre_name}\n")

	found = False
	for genre in genres:
		if genre_name == genre[1]:
			log.info(f"Scraping genre: {genre_name}\n")
			ScrapeGenre(db_name, db_host, db_username, db_password, db_port, jenkinsUserId, genre).scrape()
			found = True
			break
	
	if not found:
		log.error(f"Invalid genre name: {genre_name}")
		sys.exit(1)