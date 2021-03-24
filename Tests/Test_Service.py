from Domain.Movie import Movie
from Domain.MovieValidator import MovieValidator
from Domain.CustomerCard import CustomerCard
from Domain.CustomerCardValidator import CustomerCardValidator
from Domain.DomainError import DuplicateCNPError
from Domain.Reservation import Reservation
from Domain.ReservationValidator import ReservationValidator
from Repository.RepositoryGeneric import RepositoryGeneric
from Repository.RepositoryError import RepositoryError
from Service.MovieService import MovieService
from Service.CustomerCardService import CustomerCardService
from Service.ReservationService import ReservationService

EPSILON = 0.001


def test_movie_service():
    undoList = []
    redoList = []
    movieValidator = MovieValidator()
    reservationRepository = RepositoryGeneric("testReservations.pkl")
    movieRepository = RepositoryGeneric("testMovies.pkl")
    movieRepository.clear()
    movieService = MovieService(movieRepository, movieValidator, reservationRepository, undoList, redoList)
    movie = Movie(1, "Matrix", 2000, 34.6, "yes")
    movieService.add(movie.getId(), movie.getTitle(), movie.getReleaseYear(),
                              movie.getTicketPrice(), movie.getInTheaters())
    assert list(movieService.getObjects()) == [movie]
    try:
        movieService.add(movie.getId(), movie.getTitle(), movie.getReleaseYear(),
                              movie.getTicketPrice(), movie.getInTheaters())
        assert False
    except RepositoryError:
        assert True


def test_customerCard_service():
    undoList = []
    redoList = []
    reservationRepository = RepositoryGeneric("testReservations.pkl")
    customerCardRepository = RepositoryGeneric("testCustomerCards.pkl")
    customerCardValidator = CustomerCardValidator()
    customerCardRepository.clear()
    customerCardService = CustomerCardService(customerCardRepository,
                                                      customerCardValidator, reservationRepository,
                                                      undoList, redoList)
    customerCard = CustomerCard(1, "Pop", "Mircea", "1960412123456", "12.04.1996", "21.10.2018", 320)
    customerCardService.add(customerCard.getId(), customerCard.getSurname(),
                                    customerCard.getFirstName(), customerCard.getCnp(),
                                    customerCard.getDateOfBirth(), customerCard.getDateOfRegistration(),
                                    customerCard.getPointsEarned())
    assert list(customerCardService.getObjects()) == [customerCard]
    try:
        customerCardService.add(customerCard.getId(), customerCard.getSurname(),
                                    customerCard.getFirstName(), customerCard.getCnp(),
                                    customerCard.getDateOfBirth(), customerCard.getDateOfRegistration(),
                                    customerCard.getPointsEarned())
        assert False
    except DuplicateCNPError:
        assert True
    except RepositoryError:
        assert True


def test_reservation_service():
    undoList = []
    redoList = []
    reservationValidator = ReservationValidator()
    customerCardRepository = RepositoryGeneric("testCustomerCards.pkl")
    movieRepository = RepositoryGeneric("testMovies.pkl")
    reservationRepository = RepositoryGeneric("testReservations.pkl")
    reservationRepository.clear()
    reservationService = ReservationService(reservationRepository, movieRepository, customerCardRepository,
                                            reservationValidator, undoList, redoList)
    reservation = Reservation(1, 1, 1, "21.10.2019 14:34")
    reservationService.add(reservation.getId(), reservation.getIdMovie(),
                           reservation.getIdCustomerCard(), reservation.getDateAndTime())
    try:
        reservationService.add(reservation.getId(), reservation.getIdMovie(),
                           reservation.getIdCustomerCard(), reservation.getDateAndTime())
        assert False
    except RepositoryError:
        assert True
    l = list(reservationService.getReservations())
    elem = l[0]
    assert elem.getId() == 1
    assert elem.getIdMovie() == 1
    assert elem.getIdCustomerCard() == 1
    assert elem.getDateAndTime() == "21.10.2019 14:34"
    l2 = reservationService.showReservationsBetweenHours("09:30", "18:15")
    assert l2[0] == elem
    reservationService.deleteReservationsFromDays("07.07.2019", "12.12.2019")
    l3 = list(reservationService.getReservations())
    assert l3 == []


def test_service():
    test_movie_service()
    test_customerCard_service()
    test_reservation_service()
