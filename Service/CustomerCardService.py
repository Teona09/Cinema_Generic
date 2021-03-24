import datetime

from Domain.CustomerCard import CustomerCard


class CustomerCardService:
    """
        Manages a Customer Card Logic
    """

    def __init__(self, repository, validator, repositoryReservation, undoList, redoList):
        """
        Creates a customer card service.
        """
        self.__repository = repository
        self.__validator = validator
        self.__repositoryReservation = repositoryReservation
        self.__undoList = undoList
        self.__redoList = redoList

    def add(self, idCustomerCard, surname, firstName, cnp, dateOfBirth, dateOfRegistration, pointsEarned):
        """
        creates a customer card
        :param idCustomerCard: int
        :param surname: string
        :param firstName: string
        :param cnp: string, contains only digits
        :param dateOfBirth: string, the format is dd.mm.yyyy
        :param dateOfRegistration: string, the format is dd.mm.yyyy
        :param pointsEarned: int
        :return:
        """
        customerCard = CustomerCard(idCustomerCard, surname, firstName, cnp, dateOfBirth, dateOfRegistration,
                                    pointsEarned)
        self.__validator.validate(customerCard)
        self.__repository.create(customerCard)
        self.__undoList.append([lambda: self.__repository.delete(customerCard),
                                lambda: self.__repository.create(customerCard)])
        self.__redoList.clear()

    def delete(self, id):
        """
        deletes a customerCard
        :param id: int
        """
        list = []
        card = self.__repository.read(id)
        for reservation in self.__repositoryReservation.read():
            if reservation.getIdMovie() == id:
                list.append(reservation)
        for i in range(len(list)):
            self.__repositoryReservation.delete(list[i])
        self.__repository.delete(card)
        self.__undoList.append([lambda: self.__repository.create(card), lambda: self.__repository.delete(id)])
        self.__redoList.clear()

    def update(self, idCustomerCard, surname, firstName, cnp, dateOfBirth, dateOfRegistration, pointEarned):
        """
        updates a customerCard
        :param idCustomerCard: int
        :param surname: string
        :param firstName: string
        :param cnp: string made only from digits
        :param dateOfBirth: string with the format dd.mm.yyyy
        :param dateOfRegistration: string with the format dd.mm.yyyy
        :param pointEarned: int
        """
        customerCard1 = self.__repository.read(id)
        customerCard = CustomerCard(idCustomerCard, surname, firstName, cnp, dateOfBirth, dateOfRegistration,
                                    pointEarned)
        self.__validator.validate(customerCard)
        self.__repository.update(customerCard)
        self.__undoList.append([lambda: self.__repository.update(customerCard1),
                                lambda: self.__repository.update(customerCard)])
        self.__redoList.clear()

    def getObjects(self):
        """
        :return: a list of all the cars.
        """
        return self.__repository.read()

    def sortDescendingByPointsEarned(self):
        return sorted(self.getObjects(),
                      key=lambda customerCard: customerCard.getPointsEarned(),
                      reverse=True)

    def searchBySurname(self, surname):
        list = []
        for customerCard in self.__repository.read():
            if customerCard.getSurname() == surname:
                list.append(customerCard)
        if not list:
            list.append("no match found")
        return list

    def searchByFirstName(self, firstName):
        list = []
        for customerCard in self.__repository.read():
            if customerCard.getFirstName() == firstName:
                list.append(customerCard)
        if not list:
            list.append("no match found")
        return list

    def searchByCnp(self, CNP):
        list = []
        for customerCard in self.__repository.read():
            if customerCard.getCnp() == CNP:
                list.append(customerCard)
        if not list:
            list.append("no match found")
        return list

    def searchByDateOfBirth(self, date):
        list = []
        for customerCard in self.__repository.read():
            if customerCard.getDateOfBirth() == date:
                list.append(customerCard)
        if not list:
            list.append("no match found")
        return list

    def searchByDateOfRegistration(self, date):
        list = []
        for customerCard in self.__repository.read():
            if customerCard.getDateOfRegistration() == date:
                list.append(customerCard)
        if not list:
            list.append("no match found")
        return list

    def sortBySurname(self):
        """
        Sorts transactions by workmanship price
        :return: a list of sorted transactions
        """
        sort = self.mySort(list(self.__repository.read()), key=lambda customerCard: customerCard.getSurname(),
                      reverse=False)
        return sort

    @staticmethod
    def mySort(list, key=None, reverse=False):
        """
        Selection sort
        :param list: a list
        :param key: the key
        :param reverse: bool
        :return: the list of sorted elements
        """
        newList = list[:]
        for index in range(len(newList)):
            for index2 in range(index + 1, len(newList)):
                elem1 = newList[index]
                elem2 = newList[index2]
                if key is not None:
                    elem1 = key(elem1)
                    elem2 = key(elem2)
                cond = elem1 > elem2
                if reverse is True:
                    cond = not cond
                if cond:
                    newList[index], newList[index2] = newList[index2], newList[index]
        return newList

    def incrementPoints(self, day1, day2, extraPoints):
        """
        add extra points to customers born between 2 dates
        :param day1: first day, string
        :param day2: second day, string
        :param extraPoints: int
        """
        list = []
        x = day1.split(".")
        try:
            int(x[0])
            int(x[1])
            int(x[2])
            day1 = datetime.date(int(x[2]), int(x[1]), int(x[0]))
        except ValueError:
            raise ValueError("Wrong date")
        y = day2.split(".")
        try:
            int(y[0])
            int(y[1])
            int(y[2])
            day2 = datetime.date(int(y[2]), int(y[1]), int(y[0]))
        except ValueError:
            raise ValueError("Wrong date")
        for customerCard in self.__repository.read():
            date = customerCard.getDateOfBirth()
            a = date.split(".")
            date = datetime.date(int(a[2]), int(a[1]), int(a[0]))
            if day1 <= date <= day2:
                list.append(customerCard)
                id = customerCard.getId()
                oldPoints = customerCard.getPointsEarned()
                extraPoints += oldPoints
                self.__repository.read(id).setPointsEarned(extraPoints)
                self.__repository.writeToFile()
        self.__undoList.append(list)

    def permutations(self):
        results = []
        crtPermut = list(self.__repository.read())
        n = len(crtPermut)

        def inner(crtPerm):
            if len(crtPerm) == n:
                results.append(crtPerm)
                return

            for i in range(n):
                if crtPermut[i] not in crtPerm:
                    inner(crtPerm + [crtPermut[i]])

        inner([])
        return results