from requests import Response
from flask import request
from flask import jsonify
from flask import render_template
from restful_snmp_api.modules.api import CustomBlueprint
from restful_snmp_api.modules.api.v1.api import schedules as api_schedules

bp = CustomBlueprint('schedules', __name__,
                     template_folder='templates',
                     static_folder='static', static_url_path='assets')


@bp.route('/', methods=('GET', 'POST'))
def schedules():
    if request.method == 'GET':
        collector = bp.gv['collector']
        a : Response= api_schedules()
        print(a.status_code)
        schedule_list = collector.get_schedule_jobs()
        return render_template('schedules/view.html',
                               schedule_list=schedule_list)





