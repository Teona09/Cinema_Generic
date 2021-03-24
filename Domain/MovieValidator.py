from Domain.ValidationError import ValidationError

class MovieValidator:
	@staticmethod
	def validate(movie):
		errors = []
		if movie.getReleaseYear() < 1800:
			errors.append("There were no movies in this year")
		elif movie.getReleaseYear() > 2050:
			errors.append("We can't store movies that will be released 30 years from now")
		if movie.getTicketPrice() <= 0:
			errors.append("Ticket Price should be a positive number (float)")
		if movie.getInTheaters() not in ["yes", "no"]:
			errors.append("In Theaters should be yes or no")

		if errors:  # errors != []
			raise ValidationError(errors)