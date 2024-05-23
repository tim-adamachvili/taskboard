from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()
app_ = Flask(__name__)

class ListModel(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    tasks = relationship('TaskModel', backref='list', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<List {self.name}>'


class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'


class TaskBoardApp:
    def __init__(self, memory=False):
        self.app = app_
        if not memory:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskboard.db'
        else:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self.app)
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///taskboard.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        self.add_routes()

        self.List = ListModel
        self.Task = TaskModel

    def add_routes(self):
        app = self.app

        @app.route('/lists', methods=['GET'])
        def get_lists():
            lists = self.session.query(self.List).all()
            return jsonify([{'id': l.id, 'name': l.name, 'tasks': [{'id': t.id, 'name': t.name, 'description': t.description}
                                                                   for t in l.tasks]} for l in lists])

        @app.route('/lists', methods=['POST'])
        def create_list():
            data = request.json
            new_list = self.List(name=data['name'])
            self.session.add(new_list)
            self.session.commit()
            return jsonify({'id': new_list.id, 'name': new_list.name}), 201

        @app.route('/lists/<int:list_id>/tasks', methods=['POST'])
        def create_task(list_id):
            data = request.json
            list_ = self.session.query(self.List).get(list_id)
            if not list_:
                abort(404)
            new_task = self.Task(name=data['name'], description=data.get('description'), list=list_)
            self.session.add(new_task)
            self.session.commit()
            return jsonify({'id': new_task.id, 'name': new_task.name, 'description': new_task.description}), 201

        @app.route('/tasks/<int:task_id>', methods=['PUT'])
        def update_task(task_id):
            data = request.json
            task = self.session.query(self.Task).get(task_id)
            if not task:
                abort(404)
            task.name = data['name']
            task.description = data.get('description')
            self.session.commit()
            return jsonify({'id': task.id, 'name': task.name, 'description': task.description})

        @app.route('/tasks/<int:task_id>', methods=['DELETE'])
        def delete_task(task_id):
            task = self.session.query(self.Task).get(task_id)
            if not task:
                abort(404)
            self.session.delete(task)
            self.session.commit()
            return '', 204

        @app.route('/lists/<int:list_id>', methods=['DELETE'])
        def delete_list(list_id):
            list_ = self.session.query(self.List).get(list_id)
            if not list_:
                abort(404)
            self.session.delete(list_)
            self.session.commit()
            return '', 204

        @app.route('/tasks/<int:task_id>/move', methods=['PUT'])
        def move_task(task_id):
            data = request.json
            new_list_id = data['list_id']
            task = self.session.query(self.Task).get(task_id)
            if not task:
                abort(404)
            new_list = self.session.query(self.List).get(new_list_id)
            if not new_list:
                abort(404)
            task.list = new_list
            self.session.commit()
            return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'list_id': task.list_id})

    def run(self, debug=False):
        self.app.run(debug=debug)


if __name__ == '__main__':
    task_board_app = TaskBoardApp()
    task_board_app.run(debug=False)
