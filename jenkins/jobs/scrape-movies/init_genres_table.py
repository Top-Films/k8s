import psycopg2
import logging
import datetime
import psycopg2
import logging
import os
import datetime

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

# insert initial data into genres table
def init_genres_table(db_name, db_host, db_username, db_password, db_port):
	log.info(f"Initializing data in MOVIE_GENRE table")

	log.info("Creating connection to postgres")
	conn = psycopg2.connect(database=db_name,
									 host=db_host,
									 user=db_username,
									 password=db_password,
									 port=db_port)
	
	cursor = conn.cursor()
	for genre in genres:
		# genre data
		name = genre[1]
		id = genre[2]
		timestamp = datetime.datetime.now()
		
		# execute insert
		log.info(f"Inserting genre - created_by={jenkinsUserId} updated_by={jenkinsUserId} created_at={timestamp} updated_at={timestamp} id={id} name={name}")
		cursor.execute('INSERT INTO MOVIE_GENRE (id, created_by, updated_by, created_at, updated_at, name) VALUES (%s, %s, %s, %s, %s, %s)', (id, jenkinsUserId, jenkinsUserId, timestamp, timestamp, name))
	
	# finish transaction after all inserts
	conn.commit()
	cursor.close()
	conn.close()
	log.info(f"Successfully initialized data in MOVIE_GENRE table\n")


if __name__ == "__main__":
	db_name = os.environ.get('DB_NAME')
	db_host = os.environ.get('DB_HOST')
	db_username = os.environ.get('DB_USERNAME')
	db_password = os.environ.get('DB_PASSWORD')
	db_port = os.environ.get('DB_PORT')

	log.info('Picked up environment variables:')
	log.info(f"db_name={db_name}")
	log.info(f"db_host={db_host}")
	log.info(f"db_username={db_username}")
	log.info(f"db_password={db_password}\n")

	init_genres_table(db_name, db_host, db_username, db_password, db_port)

