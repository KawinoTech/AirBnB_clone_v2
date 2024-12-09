#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models #solves the problem of circular importation
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
Base = declarative_base()

class BaseModel:
    """
    The BaseModel class provides a foundation for other classes in the project.
    It defines common attributes and methods that can
    be shared across all derived classes.
    Each instance of BaseModel is assigned a unique identifier and timestamps
    for creation and last update, along with utility methods for saving and
    converting instance data to a dictionary format.

    Attributes:
        id (str): A unique identifier for each instance, generated using uuid4.
        created_at (datetime): The timestamp when the instance was created.
        updated_at (datetime): The timestamp of the
        last update to the instance.
    """
    
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class. Each instance is
        assigned a unique ID and timestamped upon creation. The updated_at
        attribute is also initialized to the creation time.

        If keyword arguments are provided, they are used to set instance
        attributes, allowing for initialization from a dictionary or JSON
        data. The 'created_at' and 'updated_at' timestamps are parsed from
        string format if included in kwargs.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments used to initialize
                      instance attributes. If 'created_at' or 'updated_at'
                      are provided, they should be in
                      ISO format (YYYY-MM-DDTHH:MM:SS.ssssss).
                      The '__class__' key, if present, is ignored.

        Attributes:
            id (str): The unique identifier generated
            with uuid4 for the instance.
            created_at (datetime): Timestamp for when the instance is created.
            updated_at (datetime): Timestamp initially set to creation time
                                   and updated on each save.
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k == 'created_at' or k == 'updated_at':
                        v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
                    setattr(self, k, v)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance,
        including the class name, ID, and all attribute values.

        Returns:
            str: A formatted string in the format
            "[ClassName] (id) {attributes}".
        """
        if hasattr(self, '_sa_instance_state'):
            del self._sa_instance_state
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the updated_at attribute with the current datetime. This
        method is intended to be called whenever the instance is modified,
        providing an accurate timestamp of the last modification.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance attributes to a dictionary format, making it
        easier to serialize and save the instance data. This includes all
        instance attributes and an additional __class__ key to indicate
        the class name.

        Returns:
            dict: A dictionary containing all instance attributes, with
                  datetime attributes in ISO format,
                  along with a __class__ key.
        """
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        del self