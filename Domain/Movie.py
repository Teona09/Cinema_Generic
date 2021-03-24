from Domain.Entity import Entity


class Movie(Entity):
    """
    movie object
    """
    def __init__(self, id, title, releaseYear, ticketPrice, inTheaters):
        """
        creates a movie
        :param id: int
        :param title: string
        :param releaseYear: int
        :param ticketPrice: float
        :param inTheaters: string yes or no
        """
        super().__init__(id)
        self.__title = title
        self.__releaseYear = releaseYear
        self.__ticketPrice = ticketPrice
        self.__inTheaters = inTheaters

    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title = title

    def getReleaseYear(self):
        return self.__releaseYear

    def setReleaseYear(self, releaseYear):
        self.__releaseYear = releaseYear

    def getTicketPrice(self):
        return self.__ticketPrice

    def setTicketPrice(self, price):
        self.__ticketPrice = price

    def getInTheaters(self):
        return self.__inTheaters

    def setInTheaters(self, inTheaters):
        self.__inTheaters = inTheaters

    def __str__(self):
        return "Movie {}. {} ({}) - {} - {}".format(self.getId(),
                                                    self.__title,
                                                    self.__releaseYear,
                                                    self.__ticketPrice,
                                                    self.__inTheaters)

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.getId() == other.getId() \
               and self.getTitle() == other.getTitle() \
               and self.getReleaseYear() == other.getReleaseYear() \
               and self.getTicketPrice() == other.getTicketPrice() \
               and self.getInTheaters() == other.getInTheaters()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.getId() < other.getId()