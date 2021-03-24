import random
from Domain.Movie import Movie


class MovieService:
    """
    Manages a Movie Logic
    """
    def __init__(self, repository, validator, repositoryReservation, undoList, redoList):
        """
        Creates a movie service.
        """
        self.__repository = repository
        self.__validator = validator
        self.__repositoryReservation = repositoryReservation
        self.__undoList = undoList
        self.__redoList = redoList

    def add(self, idMovie, title, releaseYear, ticketPrice, inTheaters):
        """
        Creates a movie
        :param idMovie: int
        :param title: string
        :param releaseYear: int
        :param ticketPrice: float
        :param inTheaters: string yes or no
        """
        if inTheaters in ["Yes", "yes", "YES", "TRUE", "true", "True"]:
            inTheaters = "yes"
        elif inTheaters in ["No", "no", "NO", "FALSE", "False", "false"]:
            inTheaters = "no"
        movie = Movie(idMovie, title, releaseYear, ticketPrice, inTheaters)
        self.__validator.validate(movie)
        self.__repository.create(movie)
        self.__undoList.append([lambda: self.__repository.delete(movie),
                                lambda: self.__repository.create(movie)])
        self.__redoList.clear()

    def delete(self, id):
        """
        deletes a movie
        :param id: int
        """
        list = []
        movie = self.__repository.read(id)
        for reservation in self.__repositoryReservation.read():
            if reservation.getIdMovie() == id:
                list.append(reservation)
        for i in range(len(list)):
            self.__repositoryReservation.delete(list[i])
        self.__repository.delete(movie)
        self.__undoList.append([lambda: self.__repository.create(movie), lambda: self.__repository.delete(movie)])
        self.__redoList.clear()

    def update(self, idMovie, title, releaseYear, ticketPrice, inTheaters):
        """
        updates a movie
        :param idMovie: int
        :param title: string
        :param releaseYear: int
        :param ticketPrice: float
        :param inTheaters: string yes or no
        """
        movie1 = self.__repository.read(id)
        if inTheaters in ["Yes", "yes", "YES", "TRUE", "true", "True"]:
            inTheaters = "yes"
        elif inTheaters in ["No", "no", "NO", "FALSE", "False", "false"]:
            inTheaters = "no"
        movie = Movie(idMovie, title, releaseYear, ticketPrice, inTheaters)
        self.__validator.validate(movie)
        self.__repository.update(movie)
        self.__undoList.append([lambda: self.__repository.update(movie1), lambda: self.__repository.update(movie)])
        self.__redoList.clear()

    def getObjects(self):
        """
        :return: a list of all the movies.
        """
        return self.__repository.read()

    def sortById(self):
        return sorted(self.getObjects(),
                      key=lambda movie: movie.getId(),
                      reverse=False)

    def sortByTitle(self):
        return sorted(self.getObjects(),
                      key=lambda movie: movie.getTitle(),
                      reverse=False)

    def searchByTitle(self, title):
        list = []
        for movie in self.__repository.read():
            if movie.getTitle() == title:
                list.append(movie)
        if not list:
            list.append("no match found")
        return list

    def searchByReleaseYear(self, year):
        list = []
        for movie in self.__repository.read():
            if movie.getReleaseYear() == year:
                list.append(movie)
        if not list:
            list.append("no match found")
        return list

    def searchByTicketPrice(self, price):
        list = []
        for movie in self.__repository.read():
            if movie.getTicketPrice() == price:
                list.append(movie)
        if not list:
            list.append("no match found")
        return list

    @staticmethod
    def randomTitle():
        """
        Gets a random title
        :return: the tile
        """
        return random.choice(["Matrix", "Harry Potter", "Divergent", "Star Wars", "Inception",
                              "A Christmas Carol", "Bambi", "Ford vs Ferrari"])

    @staticmethod
    def randomYear():
        """
        Gets a random year
        :return: the year
        """
        return random.choice([2010, 2011, 2012, 2013, 2014, 2003, 2009, 2007, 2018, 2017])

    @staticmethod
    def randomPrice():
        """
        Gets a random price
        :return: the price
        """
        return random.choice([12.5, 45.8, 64.0, 6.8, 46.8, 28.5, 35.5])

    @staticmethod
    def randomInTheaters():
        """
        Gets a random inTheaters
        :return: a string "yes" or "no"
        """
        return random.choice(["yes", "no", "yes"])

    def random(self, n):
        """
        Creates a number random movies
        :param n: the given number
        """
        list = []
        self.__repository.sortById()
        ind = max(self.__repository.read())
        ind = ind.getId()
        for index in range(n):
            ind = ind + 1
            movie = Movie(int(ind), self.randomTitle(), int(self.randomYear()),
                          float(self.randomPrice()), self.randomInTheaters())
            self.__repository.create(movie)
            list.append(ind)
        self.__undoList.append(list)
        self.__redoList.clear()

    def sortRec(self):
        return self.sortByMovieRecursive(list(self.__repository.read()))

    def sortByMovieRecursive(self, list):
        """
        :return: a list of sorted movies
        """
        if not list:
            return []
        return [self.__repository.read(list[0].getId())] + self.sortByMovieRecursive(list[1:])