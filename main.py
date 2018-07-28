
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from apptypes import Priority, Status, Points

Base = declarative_base()

class Project(Base):
    __tablename__ = 'Projects'

    proj_id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(), default=datetime.datetime.now())
    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)

    storys = relationship("Story")

    def __repr__(self):
        return "<Project(id='%d', date='%s', title='%s')>" % (
                            self.proj_id, self.created_date, self.title)

class Story(Base):
    __tablename__ = 'Storys'

    story_id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime(), default=datetime.datetime.now())
    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    status = Column(Integer, default=Status.OPEN)
    priority = Column(Integer, default=Priority.LOW)
    points = Column(Integer, default=Points.M)
    proj_id = Column(Integer, ForeignKey('Projects.proj_id'))
    sprint_id = Column(Integer, ForeignKey('Sprints.sprint_id'))

    def __repr__(self):
        return "<Story(id='%d', date='%s', title='%s')>" % (
                            self.story_id, self.created_date, self.title)

class Sprint(Base):
    __tablename__ = 'Sprints'
    sprint_id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime(), default=datetime.datetime.now())
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    title = Column(String(128), nullable=False)
    active = Column(Boolean, nullable=True)
    description = Column(String(1024), nullable=True)
    velocity = Column(Integer, default=0, nullable=True)
    storys = relationship("Story")

    def __repr__(self):
        return "<Sprint(id='%d', date='%s', title='%s')>" % (
                            self.sprint_id, self.created_date, self.title)

class DataBase:
    # TODO: Allow single instance of this class

    def __init__(self, db_path="deepscrum-test.db"):
        self.engine = create_engine('sqlite:///'+ db_path)
        Base.metadata.create_all(self.engine)

        # Create a session to handle updates.
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_project(self, project):
        self.session.add(project)
        self.session.commit()
        return project.proj_id

    def add_story(self, story):
        self.session.add(story)
        self.session.commit()
        return story.story_id

    def add_sprint(self, sprint):
        self.session.add(sprint)
        self.session.commit()
        return sprint.sprint_id

    def get_projects(self, all=True, limit=0):
        return self.session.query(Project).all()

    def get_storys(self, all=True, limit=0):
        return self.session.query(Story).all()

    def get_sprints(self, all=True, limit=0):
        return self.session.query(Sprint).all()

if __name__ == '__main__':
    db = DataBase()

    proj = Project(title='Project A', description='Sample Project Apple')
    proj_id = db.add_project(proj)
    print(proj_id)

    result = db.get_projects()
    print(result)
