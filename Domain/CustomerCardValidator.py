import datetime


def checkDate(date):
    day, month, year = date.split('.')
    try:
        datetime.datetime(int(year), int(month), int(day))
        valid = True
    except ValueError:
        valid = False
    return valid


def correctDataChronology(date1, date2):
    day1, month1, year1 = date1.split('.')
    day2, month2, year2 = date2.split('.')
    if year2 < year1:
        return False
    elif year1 == year2 and month2 < month1:
        return False
    elif year1 == year2 and month2 == month1 and day2 < day1:
        return False
    else:
        return True


class CustomerCardValidator:
    @staticmethod
    def validate(customerCard):
        errors = []
        if not customerCard.getSurname().isalpha():
            errors.append("The Surname must be a string/text")
        if not customerCard.getFirstName().isalpha():
            errors.append("The First Name must be a string/text")
        if len(customerCard.getCnp()) != 13 and customerCard.getCnp().isnumeric() is False:
            errors.append("This CNP is incorrect")
        if len(customerCard.getDateOfBirth()) != 10 or not checkDate(customerCard.getDateOfBirth()):
            errors.append("Date of Birth incorrect")
        if len(customerCard.getDateOfRegistration()) != 10 or not checkDate(customerCard.getDateOfRegistration()):
            errors.append("Date of Registration incorrect")
        if correctDataChronology(customerCard.getDateOfBirth(), customerCard.getDateOfRegistration()) is False:
            errors.append("The date of birth can be more recent than the date of registration")
        if type(customerCard.getPointsEarned()) != int:
            errors.append("Points Earned must be a number(int)")
        if errors:  # errors != []
            raise ValueError(errors)
