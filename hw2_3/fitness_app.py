import datetime

from flask import Flask, request, jsonify

from context import MongoFitnessContext, StatusCode
from models import Pass, Statistic, Event, EXIT, ENTER, DATE_FORMAT

app = Flask(__name__)
Context = MongoFitnessContext()
statistic = Statistic()


def main():
    global statistic
    all_events = Context.events.get_all_evensts()
    statistic = Statistic(all_events)
    app.run()


@app.route('/manager/clear', methods=['GET'])
def clear_db():
    Context.events.drop()
    Context.passes.drop()
    return jsonify(success=True)


@app.route('/manager/create', methods=['POST'])
def create_pass():
    pass_id = request.json['pass_id']
    start_time = datetime.datetime.strptime(request.json['start'], DATE_FORMAT)
    finish_time = datetime.datetime.strptime(request.json['finish'], DATE_FORMAT)
    this_pass = Pass(
        pass_id, start_time, finish_time
    )
    res = Context.passes.get_by_id(pass_id)
    if res is None:
        Context.passes.create(this_pass)
    else:
        return f"Pass #{pass_id} already created", StatusCode.CANT_CREATE
    return jsonify(success=True)


@app.route('/manager/update', methods=['POST'])
def update_pass():
    new_pass = Pass(
        pass_id=request.json['pass_id'],
        start_time=datetime.datetime.now(),
        finish_time=datetime.datetime.strptime(request.json['finish'], DATE_FORMAT)
    )
    res = Context.passes.update(new_pass)
    if res is None:
        return f"Pass ID ={request.json['pass_id']} does not exist in database", StatusCode.NOT_IN_DATABASE

    return jsonify(success=True)


@app.route('/manager/get_info/<pass_id>', methods=['GET'])
def get_info(pass_id):
    ps = Context.passes.get_by_id(int(pass_id))
    if ps is None:
        return f"Pass ID = {pass_id} does not exist in database", StatusCode.NOT_IN_DATABASE
    return str(ps), StatusCode.OK


@app.route('/report/daily', methods=['GET'])
def daily_report():
    res = statistic.get_report_by_days()
    return "{ res :" + res + " }", StatusCode.OK


@app.route('/report/total', methods=['GET'])
def total_report():
    res = statistic.calc_visits_in_minutes()
    return {"Average duration": f"{res} minutes per visit"}, StatusCode.OK


@app.route('/user/enter', methods=['POST'])
def user_enter():
    pass_id = request.json['pass_id']
    user = Context.passes.get_by_id(pass_id)
    if user is None:
        return f"Pass ID ={pass_id} does not exist in database", StatusCode.NOT_IN_DATABASE
    elif user.get_finish_time() < datetime.datetime.now():
        return "Please update your pass", StatusCode.OLD_PASS
    prev_event = Context.events.get_last_event_by_id(pass_id)
    if prev_event and prev_event.get_event_type() == ENTER:
        return "You are already in", StatusCode.ALREADY_IN

    event = Event(pass_id, ENTER, time=datetime.datetime.now())
    statistic.add_event(event)
    Context.events.create(event)
    return jsonify(success=True)


@app.route('/user/exit', methods=['POST'])
def user_exit():
    pass_id = request.json['pass_id']
    exit_time = datetime.datetime.now()
    user = Context.passes.get_by_id(pass_id)
    if user is None:
        return f"Pass ID ={pass_id} does not exist in database", StatusCode.NOT_IN_DATABASE
    prev_event = Context.events.get_last_event_by_id(pass_id)
    if prev_event is None or prev_event.get_event_type() == EXIT:
        return "You are not membership of gym or you don't enter", StatusCode.NOT_ENTER
    event = Event(pass_id, EXIT, exit_time)
    Context.events.create(event)

    statistic.add_visit(exit_time - prev_event.get_time())
    statistic.add_event(event)
    return jsonify(success=True)


if __name__ == '__main__':
    main()
