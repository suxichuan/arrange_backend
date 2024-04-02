from arrange.utils import create_app,db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from arrange.utils.redis_queue import RedisQueue
from arrange.utils.arrange import to_arrange
from datetime import date
import pickle



app=create_app('dev')
manager=Manager(app)
weekQueue=RedisQueue(name='week_plan')
monthQueue=RedisQueue(name='month_plan')
Migrate(app=app,db=db)
manager.add_command('app',MigrateCommand)  #python .\manage.py app init

"""
    python .\manage.py app init   只需要执行一次
    python .\manage.py app migrate 生成表结构   
    python .\manage.py app upgrade  映射数据库
    在新增表的时候只需要 执行migrate和upgrade命令   执行命令时主函数里需要运行 manager.run
    python .\manage.py runserver  来运行flask项目
"""

@app.route("/")
def index():
    return 'ok'
#
@app.route("/test1")
def test1():
    value=weekQueue.get()
    print(value)
    return 'ok'

@app.route("/test2")
def test2():
    value1=weekQueue.get_list()
    value2=monthQueue.get_list()
    if '10154' in value1:
        print('存在于周计划列表中')
    else:
        print('不存在于周计划列表中')

    if '10154' in value2:
        print('存在于月计划列表中')
    else:
        print('不存在于月计划列表中')
    return 'ok'


@app.route("/test3")
def test3():
    weekQueue.truncate_list()
    monthQueue.truncate_list()
    return 'ok'



if __name__ == '__main__':
    app.run()
