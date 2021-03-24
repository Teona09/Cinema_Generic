from Domain.Entity import Entity


class Reservation(Entity):
    """
    reservation object
    """
    def __init__(self, id, idMovie, idCustomerCard, dateAndTime):
        """
        creates a reservation
        :param id: int
        :param idMovie: int
        :param idCustomerCard: int
        :param dateAndTime: string representing a date and an hour with the format dd.mm.yyyy hh:mm
        """
        super().__init__(id)
        self.__idMovie = idMovie
        self.__idCustomerCard = idCustomerCard
        self.__dateAndTime = dateAndTime

    def getIdMovie(self):
        return self.__idMovie

    def setIdMovie(self, newIdMovie):
        self.__idMovie = newIdMovie

    def getIdCustomerCard(self):
        return self.__idCustomerCard

    def setIdCustomerCard(self, newIdCustomerCard):
        self.__idCustomerCard = newIdCustomerCard

    def getDateAndTime(self):
        return self.__dateAndTime

    def setDateAndTime(self, newDateAndTime):
        self.__dateAndTime = newDateAndTime

    def __str__(self):
        return "Reservation {} - {} - {} - {}".format(self.getId(),
                                                      self.__idMovie,
                                                      self.__idCustomerCard,
                                                      self.__dateAndTime)

    def __eq__(self, other):
        if not isinstance(other, Reservation):
            return False
        return self.getId() == other.getId() \
               and self.getIdMovie() == other.getIdMovie() \
               and self.getIdCustomerCard() == other.getIdCustomerCard() \
               and self.getDateAndTime() == other.getDateAndTime()

    def __ne__(self, other):
        return not self.__eq__(other)
