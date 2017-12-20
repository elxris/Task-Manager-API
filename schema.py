import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, TaskList as TaskListModel, Data as DataModel

class TaskList(SQLAlchemyObjectType):
    class Meta:
        model = TaskListModel
        exclude_fields = ('secret')
        interfaces = (relay.Node, )

class TaskListInput(graphene.InputObjectType):
    secret = graphene.String(required=True)

class CreateTaskList(graphene.Mutation):
    class Arguments:
        input = TaskListInput(required=True)

    tasklist = graphene.Field(TaskList)

    @staticmethod
    def mutate(root, info, input=None):
        tasklist = TaskListModel(secret=input.secret)
        db_session.add(tasklist)
        db_session.commit()
        return CreateTaskList(tasklist=tasklist)

class Data(SQLAlchemyObjectType):
    class Meta:
        model = DataModel
        interfaces = (relay.Node, )

class DataInput(graphene.InputObjectType):
    data = graphene.String(required=True)
    parent = graphene.ID(required=True)

class CreateData(graphene.Mutation):
    class Arguments:
        input = DataInput(required=True)

    data = graphene.Field(Data)

    @staticmethod
    def mutate(root, info, input=None):
        # new_data = DataModel(data=input.data, parent_id=TaskList.get_query(info.context).first())
        new_data = DataModel(data=input.data)
        db_session.add(new_data)
        db_session.commit()
        return CreateData(data=new_data)

class Query(graphene.ObjectType):
    # tasklist = graphene.Field(TaskList, id=graphene.ID())
    tasklist = relay.Node.Field(TaskList)
    all_tasklists = SQLAlchemyConnectionField(TaskList)
    data = relay.Node.Field(Data)

    # def resolve_tasklist(self, args, context, info):
    #     query = TaskList.get_query(context)
    #     return query.get(args.get('id'))

class Mutation(graphene.ObjectType):
    create_list = CreateTaskList.Field()
    create_data = CreateData.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[TaskList, Data])
