#!/usr/bin/python3
import json


class FileStorage:
    """
    The FileStorage class handles the serialization and deserialization of
    objects to and from a JSON file. It acts as a simple storage system,
    storing all instances in a dictionary and allowing for the persistence
    of data across sessions by saving to and reloading from a file.

    Attributes:
        __file_path (str): The path to the JSON file used for data storage.
        __objects (dict): A dictionary containing all instances by their unique
                          identifiers, in the format "ClassName.id".

    Methods:
        all(): Returns the dictionary of stored objects.
        new(obj): Adds a new object to the storage dictionary.
        save(): Serializes and writes the storage dictionary to a JSON file.
        reload(): Loads objects from the JSON file
        back into the storage dictionary.
    """

    __file_path = './file.json'
    __objects = {}

    def all(self):
        """
        Retrieves the dictionary of all stored objects.

        Returns:
            dict: The dictionary containing all objects currently stored.
                  The keys are in the format "ClassName.id", and the values
                  are the corresponding instance data in dictionary format.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary with a unique key.

        Args:
            obj (BaseModel): The object to add to storage, expected to have
                             an `id` attribute and a `to_dict`
                             method for serialization.

        Side Effects:
            Updates the __objects dictionary by adding a new entry with the
            key formatted as "ClassName.id" and value as the dictionary
            representation of the object.
        """
        self.__objects[f"{type(obj).__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """
        Serializes the __objects dictionary and writes it to the JSON file.

        Side Effects:
            Writes the current state of the __objects dictionary to the file
            specified in __file_path in JSON format.
        """
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(self.__objects, f, indent=2)

    def reload(self):
        """
        Loads objects from the JSON file into the __objects dictionary.

        This method deserializes data from the JSON file if it exists and
        populates the __objects dictionary with stored instance data.
        Each instance is represented in dictionary format with a key formatted
        as "ClassName.id".

        Side Effects:
            Updates the __objects dictionary by adding entries from the file.
            If the file does not exist or is empty, __objects
            remains unchanged.
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    pass
                else:
                    for v in data.values():
                        self.__objects[f"{v['__class__']}.{v['id']}"] = v
        except FileNotFoundError:
            pass