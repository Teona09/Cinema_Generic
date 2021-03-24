from math import fabs

from Domain.Movie import Movie
from Domain.CustomerCard import CustomerCard
from Domain.Reservation import Reservation
from Repository.RepositoryGeneric import RepositoryGeneric

EPSILON = 0.001


def test_repository_movie():
    r = RepositoryGeneric("testMovies.pkl")
    r.clear()
    movie = Movie(1,"Kingsman 2", 2017, 15.7, True)
    r.create(movie)
    assert len(r.read()) == 1
    movie2 = Movie(1,"Kingsman 2", 2017, 23.7, False)
    r.update(movie2)
    assert r.read(1).getInTheaters() is False
    assert (r.read(1).getTicketPrice() - 23.7 < 0.00001)
    r.delete(movie2)
    assert len(r.read()) == 0


def test_repository_customerCard():
    r = RepositoryGeneric("testCustomerCards.pkl")
    r.clear()
    c = CustomerCard(23, "Pop", "Adrian", "5000323370032", "23.03.2000", "09.08.2018", 320)
    r.create(c)
    assert len(r.read()) == 1
    c2 = CustomerCard(23, "Pop", "Adrian", "5000323370032", "23.03.2000", "09.08.2018", 360)
    r.update(c2)
    assert r.read(23).getPointsEarned() == 360
    r.delete(c2)
    assert len(r.read()) == 0


def test_repository_reservation():
    r = RepositoryGeneric("testReservations.pkl")
    r.clear()
    t = Reservation(12, 1, 23, "20.11.2019 20:00")
    r.create(t)
    assert len(r.read()) == 1
    t2 = Reservation(12, 1, 28, "20.11.2019 20:00")
    r.update(t2)
    assert r.read(12).getIdCustomerCard() == 28
    r.delete(t2)
    assert len(r.read()) == 0


def test_repository():
    test_repository_movie()
    test_repository_customerCard()
    test_repository_reservation()