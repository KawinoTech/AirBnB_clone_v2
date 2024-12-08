import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine #create a 
#connection engine that serves as an interface between your Python application and the database
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.place import Place
user = os.environ.get("HBNB_MYSQL_USER")
password = os.environ.get("HBNB_MYSQL_PWD")
host = os.environ.get("HBNB_MYSQL_HOST")
database = os.environ.get("HBNB_MYSQL_DB")

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{:s}:{:s}@{:s}/{:s}'.format(user,
                                                                                   password,
                                                                                   host,
                                                                                   database),
                                                                                   pool_pre_ping=True)
    
    def all(self, cls=None):
        """query on the current database session"""
        objs_dict = {}
        objs = self.__session.query(cls).all()
        for k in objs:
            objs_dict[f"{type(k).__name__}.{k.id}"] = k.to_dict()
        return objs_dict
    
    def reload(self):
        Base.metadata.create_all(bind=self.__engine)
        factory = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session
    
    def new(self, obj):
        self.__session.add(obj)
    
    def save(self):
        self.__session.commit()
