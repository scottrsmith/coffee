
"""
**Introduction**

The Coffee shop app includes uses a single Alchemy classes to manage Drinks.

- Drink Class : a persistent drink entity, extends the base SQLAlchemy Model.

The drink class has the following attributes:

- id: The auto-generated record ID
- title: The name of the drink, unique
- List of ingredients, as an json object like 
  [{'color': string, 'name':string, 'parts':number}]

"""
# ----------------------------------------------------------------------------#

import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, 
                                      database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple 
    verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



# ----------------------------------------------------------------------------#
#  Class Drink
# ----------------------------------------------------------------------------#
class Drink(db.Model):
    '''
    Drink
    A persistent drink entity, extends the base SQLAlchemy Model
    '''
        
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    """*id* is the auto assigned primary key.
        Type: Integer, Primary key. Required.
    """

    # String Title
    title = Column(String(80), unique=True)
    '''
    title, String(80)
    The title (name) of the drink
    '''

    recipe =  Column(String(180), nullable=False)
    ''' 
    recipe, string(160)
    The ingredients blob - this stores a lazy json blob
    The required datatype is [{'color': string, 'name':string, 'parts':number}]
    '''

    def __init__(self, title, recipe):
        print ('before: title, recipe', title, recipe)
        self.title = title
        self.recipe = json.dumps(recipe)
        print ('again title, recipe', self.title, self.recipe)
    

    def short(self):
        '''
        short()
            short form representation of the Drink model

            Returns::

                { 'id': self.id,
                  'title': self.title,
                  'recipe': [{'color': string, 
                             'name':string, 
                             'parts':number
                            }]
                }

        '''
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

 
    def long(self):
        '''
        long()
            long form representation of the Drink model. 

            Returns::

                { 'id': self.id,
                  'title': self.title,
                  'recipe': self.recipe
                }

        '''
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }


    def insert(self):
        '''
        insert()
            Inserts a new model into a database. The model must have a unique name.
            The model must have a unique id or null id.

            EXAMPLE::

                drink = Drink(title=req_title, recipe=req_recipe)
                drink.insert()

        '''
        db.session.add(self)
        db.session.commit()

    
    def delete(self):
        '''
        delete()
            deletes a new model into a database
            the model must exist in the database

            EXAMPLE::

                drink = Drink(title=req_title, recipe=req_recipe)
                drink.delete()

        '''
        db.session.delete(self)
        db.session.commit()

    
    def update(self):
        '''
        update()
            updates a new model into a database
            the model must exist in the database

            EXAMPLE::

                drink = Drink.query.filter(Drink.id == id).one_or_none()
                drink.title = 'Black Coffee'
                drink.update()

        '''
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())