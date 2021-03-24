from Domain.ValidationError import ValidationError
from Domain.DomainError import DomainError
from Repository.RepositoryError import RepositoryError
from Service.ServiceError import ServiceError


class Console:

	def __init__(self, movieService, customerCardService, reservationService):
		self.__movieService = movieService
		self.__customerCardService = customerCardService
		self.__reservationService = reservationService

	@staticmethod
	def __showMenu():
		print("1. Movies")
		print("2. Customer Cards")
		print("3. Reservations")
		print("4. Search movies or clients")
		print("5. Undo")
		print("6. Redo")
		print("x. Exit")

	def runConsole(self):
		while True:
			self.__showMenu()
			op = input("Option: ")
			if op == '1':
				self.__showMovies()
			elif op == '2':
				self.__showCustomerCard()
			elif op == '3':
				self.__showReservation()
			elif op == '4':
				self.__showSearch()
			elif op == "5":
				self.__reservationService.doUndo()
			elif op == "6":
				self.__reservationService.doRedo()
			elif op == 'x':
				break
			else:
				print("Invalid option!")

	def __showMovies(self):
		while True:
			self.__showMenuMovies()
			op = input("Option: ")
			if op == '1':
				self.__handleAddMovie()
			elif op == '2':
				self.__handleDeleteMovie()
			elif op == '3':
				self.__handleUpdateMovie()
			elif op == '4':
				self.__showList(self.__movieService.sortByTitle())
			elif op == '5':
				self.__handleAddRandomMovie()
			elif op == '6':
				self.__showDict(self.__reservationService.sortMoviesDescendingByNumberOfReservations())
			elif op == '7':
				self.__showList(self.__movieService.sortById())
			elif op == '8':
				self.__showList(self.__movieService.sortRec())
			elif op == 'a':
				self.__showList(self.__movieService.getObjects())
			elif op == 'b':
				break
			else:
				print("Invalid option!")

	@staticmethod
	def __showMenuMovies():
		print("--- Movies ---")
		print("1. Add")
		print("2. Delete/Remove")
		print("3. Update")
		print("4. Show movies sorted alphabetically by title")
		print("5. Populate n")
		print("6. Show movies ordered descending by number of reservations")
		print("7. Show movies sorted by ID")
		print("8. Show movies sorted recursive")
		print("a. Show all movies")
		print("b. Back")

	def __handleAddMovie(self):
		try:
			idMovie = int(input("ID: "))
			title = input("Movie title: ")
			releaseYear = int(input("Movie release year: "))
			ticketPrice = float(input("Ticket price: "))
			inTheaters = input("Is the movie still in theaters? (Yes/No): ")
			self.__movieService.add(idMovie, title, releaseYear, ticketPrice, inTheaters)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Movie added to database")

	def __handleDeleteMovie(self):
		try:
			self.__showList(self.__movieService.getObjects())
			idMovie = int(input("The ID of the movie you want to delete: "))
			self.__movieService.delete(int(idMovie))
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		except RuntimeError as ve:
			print(ve)
		else:
			print("Movie deleted from database")

	def __handleUpdateMovie(self):
		self.__showList(self.__movieService.getObjects())
		try:
			idMovie = int(input("ID: "))
			title = input("Movie title: ")
			releaseYear = int(input("Movie release year: "))
			ticketPrice = float(input("Ticket price: "))
			inTheaters = input("Is the movie still in theaters? (Yes/No): ")
			self.__movieService.update(idMovie,
									   title,
									   releaseYear,
									   ticketPrice,
									   inTheaters)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("The movie was updated successfully!")

	def __handleAddRandomMovie(self):
		try:
			n = int(input("n = "))
			self.__movieService.random(n)
		except TypeError as e:
			print(e)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Movies added to database")

	def __showCustomerCard(self):
		while True:
			self.__showMenuCustomerCards()
			op = input("Option: ")
			if op == '1':
				self.__handleAddCustomerCard()
			elif op == '2':
				self.__handleDeleteCustomerCard()
			elif op == '3':
				self.__handleUpdateCustomerCard()
			elif op == '4':
				self.__showList(self.__customerCardService.sortDescendingByPointsEarned())
			elif op == '5':
				self.__handleAddPoints()
			elif op == '6':
				self.__handleShowPermutations(self.__customerCardService.permutations())
			elif op == '7':
				self.__showList(self.__customerCardService.sortBySurname())
			elif op == 'a':
				self.__showList(self.__customerCardService.getObjects())
			elif op == 'b':
				break
			else:
				print("Invalid option!")

	@staticmethod
	def __showMenuCustomerCards():
		print("--- Customer Cards ---")
		print("1. Add")
		print("2. Delete/Remove")
		print("3. Update")
		print("4. Show customers sorted descending by points earned")
		print("5. Give points to the customers born between two dates")
		print("6. Permutations")
		print("7. Show customers sorted by surname")
		print("a. Show all customer cards")
		print("b. Back")

	def __handleAddCustomerCard(self):
		try:
			idCustomerCard = int(input("ID: "))
			surname = input("Surname: ")
			firstName = input("First Name: ")
			cnp = input("CNP (13digits): ")
			dateOfBirth = input("Date of Birth (dd.mm.yyyy): ")
			dateOfReservation = input("Date of Registration (dd.mm.yyyy): ")
			pointsEarned = int(input("Points Earned: "))
			self.__customerCardService.add(idCustomerCard,
										   surname,
										   firstName,
										   cnp,
										   dateOfBirth,
										   dateOfReservation,
										   pointsEarned)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Customer Card added")

	def __handleDeleteCustomerCard(self):
		try:
			self.__showList(self.__customerCardService.getObjects())
			idCustomerCard = int(input("The ID of the customer card you want to delete: "))
			self.__customerCardService.delete(int(idCustomerCard))
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Customer Card deleted from the database")

	def __handleUpdateCustomerCard(self):
		self.__showList(self.__customerCardService.getObjects())
		try:
			idCustomerCard = int(input("ID: "))
			surname = input("Surname: ")
			firstName = input("First Name: ")
			cnp = input("CNP (13digits): ")
			dateOfBirth = input("Date of Birth (dd.mm.yyyy): ")
			dateOfReservation = input("Date of Registration (dd.mm.yyyy): ")
			pointsEarned = int(input("Points Earned: "))
			self.__customerCardService.update(idCustomerCard,
											  surname,
											  firstName,
											  cnp,
											  dateOfBirth,
											  dateOfReservation,
											  pointsEarned)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("The customer card was updated successfully!")

	def __showReservation(self):
		while True:
			self.__showMenuReservations()
			op = input("Option: ")
			if op == '1':
				self.__handleAddReservation()
			elif op == '2':
				self.__handleDeleteReservation()
			elif op == '3':
				self.__handleUpdateReservation()
			elif op == '4':
				print("Reservation: ID Reservation - ID Movie - ID Customer Card - Date and Time")
				self.__showList(self.__reservationService.sortByIdReservation())
			elif op == '5':
				self.__handleReservationsBetweenTime()
			elif op == '6':
				self.__handleDeleteReservationFromInterval()
			elif op == 'a':
				# print("Reservation: ID Reservation - ID Movie - ID Customer Card - Date and Time")
				self.__showList(self.__reservationService.getObjects())
			elif op == 'b':
				break
			else:
				print("Invalid option!")

	def __handleAddPoints(self):
		try:
			day1 = input("The beginning date(dd.mm.yyyy): ")
			day2 = input("The ending date(dd.mm.yyyy): ")
			extraPoints = int(input("Number of extra points: "))
			self.__customerCardService.incrementPoints(day1, day2, extraPoints)
		except Exception as e:
			print(e)

	@staticmethod
	def __showMenuReservations():
		print("--- Reservations ---")
		print("1. Add")
		print("2. Delete/Remove")
		print("3. Update")
		print("4. Sort by Movie ID")
		print("5. Show reservations between two hours")
		print("6. Delete all reservations between two dates")
		print("a. Show all reservations")
		print("b. Back")

	def __handleAddReservation(self):
		try:
			idReservation = int(input("Reservation ID: "))
			idMovie = int(input("Movie ID: "))
			idCustomerCard = input("Customer Card ID:")
			dateAndTime = input("Date and Time (dd.mm.yyyy hh:mm): ")
			self.__reservationService.add(idReservation,
										  idMovie,
										  idCustomerCard,
										  dateAndTime)
		except IndexError as ve:
			print(ve)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Reservation added to database")

	def __handleDeleteReservation(self):
		try:
			self.__showList(self.__reservationService.getObjects())
			idReservation = int(input("The ID of the reservation you want to delete: "))
			self.__reservationService.delete(int(idReservation))
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Reservation deleted from the database")

	def __handleUpdateReservation(self):
		self.__showList(self.__reservationService.getObjects())
		try:
			idReservation = int(input("Reservation ID: "))
			idMovie = int(input("Movie ID: "))
			idCustomerCard = input("Customer Card ID:")
			dateAndTime = input("Date and Time (dd.mm.yyyy hh:mm): ")
			self.__reservationService.update(idReservation,
											 idMovie,
											 idCustomerCard,
											 dateAndTime)
		except ValueError as ve:
			print(ve)
		except ValidationError as ve:
			print("Errors: ")
			for error in ve.args[0]:
				print(error)
		except DomainError as ve:
			print(ve)
		except RepositoryError as ve:
			print(ve)
		except ServiceError as ve:
			print(ve)
		else:
			print("Reservation added to database")

	def __handleDeleteReservationFromInterval(self):
		try:
			day1 = input("The beginning date(dd.mm.yyyy): ")
			day2 = input("The ending date(dd.mm.yyyy): ")
			self.__reservationService.deleteReservationsFromDays(day1, day2)
		except Exception as e:
			print(e)

	def __handleReservationsBetweenTime(self):
		try:
			time1 = input("The beginning time(hh:mm): ")
			time2 = input("The ending time(hh:mm): ")
			self.__showList(self.__reservationService.showReservationsBetweenHours(time1, time2))
		except Exception as e:
			print(e)

	@staticmethod
	def __showList(objects):
		for object in objects:
			print(object)

	@staticmethod
	def __showDict(dict):
		for key in dict.keys():
			print(key + ' - ' + str(dict[key]))

	@staticmethod
	def __showMenuSearch():
		print(" ")
		print("---Search by---")
		print("1.Search movies by title")
		print("2.Search movies by release year")
		print("3.Search movies by ticket price")
		print("4.Search clients by surname")
		print("5.Search clients by first name")
		print("6.Search clients by CNP")
		print("7.Search clients by date of birth")
		print("8.Search clients by date of registration")
		print("b.Back")
		print(" ")

	def __showSearch(self):
		while True:
			self.__showMenuSearch()
			op = input("Option: ")
			if op == "1":
				title = input("Title: ")
				self.__showList(self.__movieService.searchByTitle(title))
			elif op == "2":
				year = input("Release Year: ")
				while type(year) is not int:
					try:
						year = int(year)
					except TypeError:
						print("You must introduce an integer")
						year = input("Release Year: ")
				self.__showList(self.__movieService.searchByReleaseYear(year))
			elif op == "3":
				price = input("Ticket price: ")
				while type(price) is not float:
					try:
						price = float(price)
					except TypeError as e:
						print(e)
						print("You must introduce a float")
						price = input("Ticket price: ")
					except ValueError as e:
						print(e)
						print("You must introduce a float")
						price = input("Ticket price: ")
				self.__showList(self.__movieService.searchByTicketPrice(price))
			elif op == "4":
				surname = input("Surname: ")
				self.__showList(self.__customerCardService.searchBySurname(surname))
			elif op == "5":
				firstName = input("First name: ")
				self.__showList(self.__customerCardService.searchByFirstName(firstName))
			elif op == "6":
				cnp = input("CNP: ")
				self.__showList(self.__customerCardService.searchByCnp(cnp))
			elif op == "7":
				date = input("Date of birth: ")
				self.__showList(self.__customerCardService.searchByDateOfBirth(date))
			elif op == "8":
				date = input("Date of registration: ")
				self.__showList(self.__customerCardService.searchByDateOfRegistration(date))
			elif op == 'b':
				break
			else:
				print("Invalid option!")

	@staticmethod
	def __handleShowPermutations(objects):
		i = 0
		for object in objects:
			i = i + 1
			print("Permutation " + str(i))
			for obj in object:
				print(obj)
