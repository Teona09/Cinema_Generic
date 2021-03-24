class ReservationView:

    def __init__(self, reservation, movie, customerCard):
        self.reservation = reservation
        self.movie = movie.getTitle()+' '+str(movie.getTicketPrice())
        self.customerCard = customerCard.getSurname()

    def __str__(self):
        return "{}. movie: {} -- customerCard: {}".format(self.reservation, self.movie, self.customerCard)