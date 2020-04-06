import datetime

from flask import Flask, request, jsonify

from context import MongoFitnessContext
from models import Pass, Statistic, Event, EXIT, ENTER

app = Flask(__name__)
Context = MongoFitnessContext()
statistic = Statistic()


def main():
    global statistic
    all_events = Context.events.get_all_evensts()
    statistic = Statistic(all_events)
    app.run()


@app.route('/manager/create', methods=['POST'])
def create_pass():
    pass_id = request.json['pass_id']
    start_time = datetime.datetime.strptime(request.json['start'], '%d/%m/%Y')
    finish_time = datetime.datetime.strptime(request.json['finish'], '%d/%m/%Y')
    this_pass = Pass(
        pass_id, start_time, finish_time
    )
    Context.passes.create(this_pass)

    return jsonify(success=True)


@app.route('/manager/update', methods=['POST'])
def update_pass():
    new_pass = Pass(
        pass_id=request.json['pass_id'],
        start_time=datetime.datetime.now(),
        finish_time=datetime.datetime.strptime(request.json['finish'], '%d.%m.%y')
    )
    res = Context.passes.update(new_pass)
    if res is None:
        return {"error": f"Pass ID ={request.json['pass_id']} does not exist in database"}

    return jsonify(success=True)


@app.route('/manager/get_info/<pass_id>', methods=['GET'])
def get_info(pass_id):
    ps = Context.passes.get_by_id(int(pass_id))
    if ps is None:
        return {"error": f"Pass ID = {pass_id} does not exist in database"}
    return str(ps)


@app.route('/report/daily/', methods=['GET'])
def daily_report():
    res = statistic.get_report_by_days()
    return res


@app.route('/report/total', methods=['GET'])
def total_report():
    res = statistic.calc_visits_in_minutes()
    return {"Average duration": f"{res} minutes per visit"}


@app.route('/user/enter/', methods=['POST'])
def user_enter():
    pass_id = request.json['pass_id']
    user: Pass = Context.passes.get_by_id()
    if user is None:
        return {"error": f"Pass ID ={pass_id} does not exist in database"}
    elif user.get_finish_time() < datetime.datetime.now():
        return {"error": "Please update your pass"}
    prev_event = Context.events.get_event_by_id(pass_id)
    if prev_event is None or prev_event.get_event_type() == ENTER:
        return {"error": "You are already in"}

    event = Event(pass_id, ENTER, time=datetime.datetime.now())
    statistic.add_event(event)
    Context.events.create(event)
    return jsonify(success=True)


@app.route('/user/exit/', methods=['POST'])
def user_exit():
    pass_id = request.json['pass_id']
    exit_time = datetime.datetime.now()
    user: Pass = Context.passes.get_by_id()
    if user is None:
        return {"error": f"Pass ID ={pass_id} does not exist in database"}
    prev_event = Context.events.get_event_by_id(pass_id)
    if prev_event is None or prev_event.get_event_type() == EXIT:
        return {"error": "You are not membership of gym or you don't enter"}
    event = Event(pass_id, EXIT, exit_time)
    Context.events.create(event)

    statistic.add_visit(exit_time - prev_event.get_time())
    statistic.add_event(event)
    return jsonify(success=True)


if __name__ == '__main__':
    main()
