from Domain.Movie import Movie


def test_movie():
	movie = Movie(1, "Kingsman 2", 2017, 15.7, "Da")
	assert movie.getId() == 1
	assert movie.getTitle() == "Kingsman 2"
	assert movie.getReleaseYear() == 2017
	assert movie.getTicketPrice() == 15.7
	assert movie.getInTheaters() == "Da"


def test_domain():
    test_movie()