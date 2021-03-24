import collections
import operator
import datetime

from Domain.Movie import Movie
from Domain.Reservation import Reservation
from Domain.ReservationView import ReservationView
from Service.ServiceError import ServiceError


class ReservationService:
    """
        Manages a Reservation Logic
        """

    def __init__(self, repositoryReservation, repositoryMovie, repositoryCustomerCard, validator, undoList, redoList):
        """
        Creates a reservation service.
        """
        self.__repositoryReservation = repositoryReservation
        self.__repositoryMovie = repositoryMovie
        self.__repositoryCustomerCard = repositoryCustomerCard
        self.__validator = validator
        self.__undoList = undoList
        self.__redoList = redoList

    def add(self, idReservation, idMovie, idCustomerCard, dateAndTime):
        """
        creates a reservation
        :param idReservation: int
        :param idMovie: int
        :param idCustomerCard: int
        :param dateAndTime: string, the format is dd.mm.yyyy hh:mm
        """
        if self.__repositoryMovie.read(idMovie) is None:
            raise ServiceError("there is no movie with this id")
        if self.__repositoryMovie.read(idMovie).getInTheaters() in ["no"]:
            raise ServiceError("the movie is not in theaters anymore")
        if self.__repositoryCustomerCard.read(idCustomerCard) in ["None"]:
            idCustomerCard = None
        idCustomerCard = int(idCustomerCard)
        reservation = Reservation(idReservation, idMovie, idCustomerCard, dateAndTime)
        self.__validator.validate(reservation)
        if idCustomerCard is not None:
            if self.__repositoryCustomerCard.read(idCustomerCard) is None:
                raise ServiceError("no customer card id")
            else:
                newPoints = int(self.__repositoryMovie.read(idMovie).getTicketPrice() / 10)
                card = self.__repositoryCustomerCard.read(idCustomerCard)
                oldPoints = card.getPointsEarned()
                newPoints += oldPoints
                self.__repositoryCustomerCard.read(idCustomerCard).setPointsEarned(newPoints)
                self.__repositoryCustomerCard.writeToFile()
                print("the current number of points", newPoints)
        self.__repositoryReservation.create(reservation)
        self.__undoList.append([lambda: self.__repositoryReservation.delete(reservation),
                                lambda: self.__repositoryReservation.create(self.__repositoryReservation.read(id)),
                                lambda: self.__repositoryCustomerCard.read(idCustomerCard).setPointsEarned(
                                    oldPoints), ])
        self.__redoList.clear()

    def delete(self, id):
        """
        deletes a reservation
        :param id: int
        """
        for reservation in self.__repositoryReservation.read():
            if id == reservation.getId():
                self.__repositoryReservation.delete(reservation)
                break
        self.__undoList.append([lambda: self.__repositoryReservation.create(reservation),
                                lambda: self.__repositoryReservation.delete(reservation)])
        self.__redoList.clear()

    def update(self, idReservation, idMovie, idCustomerCard, dateAndTime):
        if self.__repositoryMovie.read(idMovie) is None:
            raise IndexError("there is no movie with this id")
        if self.__repositoryMovie.read(idMovie).getInTheaters() is False:
            raise IndexError("the movie is not in theaters anymore")
        if self.__repositoryCustomerCard.read(idCustomerCard) in ["None"]:
            idCustomerCard = None
        reservation = Reservation(idReservation, idMovie, int(idCustomerCard), dateAndTime)
        reservation1 = self.__repositoryReservation.read(id)
        self.__validator.validate(reservation)
        self.__repositoryReservation.update(reservation)
        self.__undoList.append([lambda: self.__repositoryReservation.update(reservation1),
                                lambda: self.__repositoryReservation.update(reservation)])
        self.__redoList.clear()

    def getReservations(self):
        """
        :return: a list of all the reservations.
        """
        return self.__repositoryReservation.read()

    def getObjects(self):
        """
        :return: a list of all the reservations.
        """
        reservations = self.__repositoryReservation.read()
        return map(
            lambda reservation: ReservationView(reservation, self.__repositoryMovie.read(reservation.getIdMovie()),
                                                self.__repositoryCustomerCard.read(reservation.getIdCustomerCard())),
                                                reservations)

    def sortByIdReservation(self):
        return sorted(self.getObjects(),
                      key=lambda reservation: reservation.getId(),
                      reverse=False)

    def sortMoviesDescendingByNumberOfReservations(self):
        """
        sorts movies descending by number of reservations
        :return: a dict of sorted movies
        """
        movies = {}
        for reservation in self.__repositoryReservation.read():
            movieId = reservation.getIdMovie()
            movie = self.__repositoryMovie.read(movieId)
            if movie.getTitle() in movies.keys():
                movies[movie.getTitle()] += 1
            else:
                movies[movie.getTitle()] = 1
        sortedDict = sorted(movies.items(), key=operator.itemgetter(1), reverse=True)
        sortedDict = collections.OrderedDict(sortedDict)
        return sortedDict

    def deleteReservationsFromDays(self, day1, day2):
        """
        Deletes reservations from an interval of days
        :param day1: first day
        :param day2: second day
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
        for reservation in self.__repositoryReservation.read():
            date = reservation.getDateAndTime()
            z = date.split(" ")
            a = z[0].split(".")
            date = datetime.date(int(a[2]), int(a[1]), int(a[0]))
            if day1 <= date <= day2:
                list.append(reservation)
        for i in range(len(list)):
            self.__repositoryReservation.delete(list[i])
        self.__undoList.append(list)
    
    def showReservationsBetweenHours(self, time1, time2):
        """
        returns a list of reservations from an interval of days
        :param time1: first time
        :param time2: second time
        """
        list = []
        x = time1.split(":")
        try:
            int(x[0])
            int(x[1])
            time1 = datetime.time(int(x[0]), int(x[1]))
        except ValueError as e:
            print(e)
        y = time2.split(":")
        try:
            int(y[0])
            int(y[1])
            time2 = datetime.time(int(y[0]), int(y[1]))
        except ValueError:
            raise ValueError("Wrong time format")
        for reservation in self.__repositoryReservation.read():
            date = reservation.getDateAndTime()
            z = date.split(" ")
            a = z[1].split(":")
            time = datetime.time(int(a[0]), int(a[1]))
            if time1 <= time <= time2:
                list.append(reservation)
        return list

    def doUndo(self):
        """
        Undo function
        """
        if len(self.__undoList) > 0:
            op = self.__undoList.pop()
            if isinstance(op[0], int):
                l = []
                while op:
                    o = op[-1]
                    l.append(self.__repositoryMovie.read(o))
                    self.__repositoryMovie.delete(o)
                    del op[-1]
                self.__redoList.append(l)
            elif isinstance(op[0], Movie):
                l = []
                for i in range(len(op) - 1, -1, -1):
                    l.append(self.__repositoryMovie.read(op[i].entityId))
                    self.__repositoryMovie.update(op[i])
                l.append("update")
                self.__redoList.append(l)
            elif isinstance(op[0], Reservation):
                if isinstance(op[-1], list):
                    l = []
                    for i in range(len(op) - 2, -1, -1):
                        l.append(op[i].entityId)
                        self.__repositoryReservation.create(op[i])
                    l.append([op[len(op) - 1][1], op[len(op) - 1][0]])
                    op[len(op) - 1][0]()
                    self.__redoList.append(l)
                else:
                    l = []
                    for i in range(len(op) - 1, -1, -1):
                        l.append(op[i].entityId)
                        self.__repositoryReservation.create(op[i])
                    self.__redoList.append(l)
            else:
                self.__redoList.append([op[1], op[0]])
                op[0]()

    def doRedo(self):
        """
        Redo function
        :return:
        """
        if len(self.__redoList) > 0:
            op = self.__redoList.pop()
            if isinstance(op[0], Movie):
                if isinstance(op[-1], str):
                    l = []
                    for i in range(len(op) - 2, -1, -1):
                        l.append(self.__repositoryMovie.read(op[i].entityId))
                        self.__repositoryMovie.update(op[i])
                    self.__undoList.append(l)
                else:
                    l = []
                    for i in range(len(op) - 1, -1, -1):
                        l.append(op[i].entityId)
                        self.__repositoryMovie.create(op[i])
                    self.__undoList.append(l)
            elif isinstance(op[0], int):
                if isinstance(op[-1], list):
                    l = []
                    lst = [op[len(op) - 1][1], op[len(op) - 1][0]]
                    op[len(op) - 1][0]()
                    del op[-1]
                    while op:
                        o = op[-1]
                        l.append(self.__repositoryReservation.read(o))
                        self.__repositoryReservation.delete(o)
                        del op[-1]
                    l.append(lst)
                    self.__undoList.append(l)
                else:
                    l = []
                    while op:
                        o = op[-1]
                        l.append(self.__repositoryReservation.read(o))
                        self.__repositoryReservation.delete(o)
                        del op[-1]
                    self.__undoList.append(l)
            else:
                self.__undoList.append([op[1], op[0]])
                op[0]()
