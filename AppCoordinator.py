from Tests.Test_Domain import test_domain
from Tests.Test_Repository import test_repository
from Tests.Test_Service import test_service
from Repository.RepositoryGeneric import RepositoryGeneric
from Domain.MovieValidator import MovieValidator
from Domain.CustomerCardValidator import CustomerCardValidator
from Domain.ReservationValidator import ReservationValidator
from Service.MovieService import MovieService
from Service.CustomerCardService import CustomerCardService
from Service.ReservationService import ReservationService
from UserInterface.Console import Console


def main():
    test_domain()
    test_repository()
    test_service()
    undoList = []
    redoList = []
    movieRepository = RepositoryGeneric("movie.pkl")
    movieValidator = MovieValidator()
    customerCardRepository = RepositoryGeneric("customerCard.pkl")
    customerCardValidator = CustomerCardValidator()
    reservationRepository = RepositoryGeneric("reservation.pkl")
    reservationValidator = ReservationValidator()
    movieService = MovieService(movieRepository, movieValidator, reservationRepository, undoList, redoList)
    customerCardService = CustomerCardService(customerCardRepository, customerCardValidator, reservationRepository,
                                              undoList, redoList)
    reservationService = ReservationService(reservationRepository, movieRepository, customerCardRepository,
                                            reservationValidator, undoList, redoList)
    console = Console(movieService, customerCardService, reservationService)
    console.runConsole()


main()