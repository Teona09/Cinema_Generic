import datetime
from Domain.ValidationError import ValidationError

def checkDateAndTime(DateAndTime):
	if not (' ' in DateAndTime):
		valid = False
	else:
		try:
			date, time = DateAndTime.split(' ')
			day, month, year = date.split('.')
			hour, minutes = time.split(':')
			datetime.datetime(int(year), int(month), int(day))
			hour = int(hour)
			minutes = int(minutes)
			valid = True
		except ValueError:
			valid = False
		else:
			if not (1 <= hour <= 24) or not (0 <= minutes <= 59):
				valid = False
			if int(year) < 2019:
				valid = False
	return valid


class ReservationValidator:
	@staticmethod
	def validate(reservation):
		errors = []
		if not checkDateAndTime(reservation.getDateAndTime()):
			errors.append("Date and time incorrect")
			errors.append("All reservation must be made after 01.01.2019")
		if errors:  # errors != []
			raise ValidationError(errors)
