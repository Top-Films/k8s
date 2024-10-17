from selenium import webdriver  
from selenium.webdriver.common.by import By
from threading import Thread
import psycopg2
import logging
import uuid
import time
import datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

	def run(self):
		# run scraping in new thread
		thread = Thread(target=self.scrape)
		thread.start()

	def scrape(self):
		# parse values from genre
		genre_url_path = self.genre[0]
		genre_name = self.genre[1]
		genre_id = self.genre[2]

		# continue until max_retries_genre exceeded
		page_error_count = 0
		page_num = 1
		while page_error_count < self.max_retries_genre:
			# concat all logs for each page into one string for readability while each thread executes
			logs = f"-------------------- {genre_name} ({page_num}): Errors {page_error_count}/{self.max_retries_genre} --------------------\n"
			url = f"https://www.allmovie.com/genre/{genre_url_path}/alltime-desc/{page_num}"
			page_error_count = page_error_count + self.__scrape_page(url, page_num, genre_name, genre_id, logs)
			page_num = page_num + 1
			log.info(logs)

		self.conn.close()
		self.driver.quit()
					
	def __scrape_page(self, url, page_num, genre_name, genre_id, logs):
		start_time = time.time()

		# attempt to parse page max_retries_page times
		attempt_count = 1
		while attempt_count <= self.max_retries_page:
			logs = logs + f"Attempt {attempt_count}/{self.max_retries_page}: {url}\n"
			try:
				# get driver and url
				self.driver.get(url)
				self.driver.maximize_window()

				# attempt to parse all 20 movies on a page
				for movie_num in range(self.page_offset, self.num_movies_per_page + self.page_offset):
					self.__parse_movie(movie_num, genre_id, logs)

				# page complete with more movies within the genre
				end_time = time.time()
				logs = logs + f"Successfully scraped {genre_name} ({page_num}): {round(end_time-start_time, 2)}s\n\n"
				return 0

			except Exception as e:
				# failed to parse page for unknown reason
				logs = logs + f"Error on attempt {attempt_count}: {url}\n"
				logs = logs + f"{e}\n"

				# increase count
				attempt_count = attempt_count + 1

				# re init driver fully
				self.driver.quit()
				self.driver = self.__init_driver()

		# failed to parse max_retries_page times
		logs = logs + f"Maximum attempts reached: url={url} | genre={genre_name} | page_num={page_num}\n\n"
		return 1
	
	def __parse_movie(self, movie_num, genre_id, logs):
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
			logs = logs + f"No director for movie: {title}\n"

		# parse year
		year = None
		try:
			year_elem = movie_wrapper_elem.find_element(By.CLASS_NAME, 'movie-year')
			year = year_elem.text
		except Exception:
			logs = logs + f"No year for movie: {title}\n"


		# ensure movie does not already exist
		cursor = self.conn.cursor()
		cursor.execute('SELECT * FROM MOVIE WHERE name = %s AND year = %s', (title, year))
		if len(cursor.fetchall()) > 0:
			# ignore duplicate record
			logs = logs + f"Movie already exists - {movie_num}: title={title} | director={director}\n"
			cursor.close()
			return

		# create new record
		timestamp = datetime.datetime.now()
		id = str(uuid.uuid4())
		logs = logs + f"Inserting movie - {movie_num}: title={title} | director={director} | year={year} | time={timestamp} | id={id}\n"
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