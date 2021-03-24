import pickle
from collections import OrderedDict
from Repository.RepositoryError import RepositoryError


class RepositoryGeneric:
    """
    Repository for storing data in memory
    """

    def __init__(self, fileName):
        """
        Creates an in memory repository
        """
        self.__fileName = fileName
        # self.__storage = {}
        self.__storage = self.__readFromFile()

    def __readFromFile(self):
        """
        Reads the data from a file
        """
        try:
            f = open(self.__fileName, "rb")
            dict = pickle.load(f)
            f.close()
        except FileNotFoundError:
            dict = self.__storage.clear()
        except RepositoryError:
            dict = self.__storage.clear()
        return dict

    def writeToFile(self):
        """
        Writes the data to a file
        """
        f = open(self.__fileName, "wb")
        pickle.dump(self.__storage, f)
        f.close()

    def create(self, entity):
        """
        Creates an object
        """
        if entity.getId() in self.__storage.keys():
            raise RepositoryError
        self.__storage[entity.getId()] = entity
        self.writeToFile()

    def read(self, id=None):
        """
        Returns an object if the id is not none
        and a list with all the objects is id is none
        """
        if not (id is None):
            if not (id in self.__storage):
                return None
            return self.__storage[id]
        return self.__storage.values()

    def update(self, entity):
        """
        Updates an object
        """
        if not entity.getId() in self.__storage:
            raise RepositoryError("Doesn't exist")
        self.__storage[entity.getId()] = entity
        self.writeToFile()

    def delete(self, entity):
        """
        Deletes an objects
        """
        if not (entity.getId() in self.__storage):
            raise RepositoryError("Doesn't exist")
        del self.__storage[entity.getId()]
        self.writeToFile()

    def clear(self):
        """
        Clears the file
        """
        self.__storage.clear()
        self.writeToFile()
        return self.__storage

    def sortById(self):
        self.__storage = OrderedDict(sorted(self.__storage.items()))
        self.writeToFile()