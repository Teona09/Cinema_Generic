from Domain.Entity import Entity


class CustomerCard(Entity):
    """
    customer card object
    """
    def __init__(self, id, surname, firstName, cnp, dateOfBirth, dateOfRegistration, pointsEarned):
        """
		creates a movie
		:param id: int
		:param surname: string
		:param firstName: string
		:param cnp: a string made only from numbers
		:param dateOfBirth: a string representing a date dd.mm.yyyy
		:param dateOfRegistration: a string representing a date dd.mm.yyyy
		:param pointsEarned: int
        """
        super().__init__(id)
        self.__surname = surname
        self.__firstName = firstName
        self.__cnp = cnp
        self.__dateOfBirth = dateOfBirth
        self.__dateOfRegistration = dateOfRegistration
        self.__pointsEarned = int(pointsEarned)

    def getSurname(self):
        return self.__surname

    def setSurname(self, newSurname):
        self.__surname = newSurname

    def getFirstName(self):
        return self.__firstName

    def setFirstName(self, newFirstName):
        self.__firstName = newFirstName

    def getCnp(self):
        return self.__cnp

    def setCnp(self, newCnp):
        self.__cnp = newCnp

    def getDateOfBirth(self):
        return self.__dateOfBirth

    def setDateOfBirth(self, newDateOfBirth):
        self.__dateOfBirth = newDateOfBirth

    def getDateOfRegistration(self):
        return self.__dateOfRegistration

    def setDateOfRegistration(self, newDateOfRegistration):
        self.__dateOfRegistration = newDateOfRegistration

    def getPointsEarned(self):
        return self.__pointsEarned

    def setPointsEarned(self, newPointsEarned):
        self.__pointsEarned = newPointsEarned

    def __str__(self):
        return "Customer Card {}.{} {} / {} / {} ~ {} - {} ".format(self.getId(),
                                                                    self.__surname,
                                                                    self.__firstName,
                                                                    self.__cnp,
                                                                    self.__dateOfBirth,
                                                                    self.__dateOfRegistration,
                                                                    self.__pointsEarned)

    def __eq__(self, other):
        if not isinstance(other, CustomerCard):
            return False
        return self.getId() == other.getId()\
               and self.getSurname() == other.getSurname() \
               and self.getFirstName() == other.getFirstName() \
               and self.getCnp() == other.getCnp() \
               and self.getDateOfBirth() == other.getDateOfBirth() \
               and self.getDateOfRegistration() == other.getDateOfRegistration() \
               and self.getPointsEarned() == other.getPointsEarned()

    def __ne__(self, other):
        return not self.__eq__(other)