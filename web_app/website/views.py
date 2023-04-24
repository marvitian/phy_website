# Store standard roots for our server
from flask import Blueprint, render_template, request, flash, jsonify, send_file, redirect, url_for, copy_current_request_context
from flask_login import login_required, current_user
from operator import attrgetter

from . import db, app, logging #turbo
from .models import Request
from csrStructDB.queryDB import query_csr_db
from csrStructDB import get_functional_mode, get_functional_test, get_functional_spec

import threading, os, json, copy

views = Blueprint('views', __name__)

OPTIONS_REQUIRED = {'MajorSystemMode':'LP4,LP5', 'byte-mode':'8,16', 'DFI2CKRatio':'1,2,4'}
CSRSTRUCT_OUTDIR = "/home/mohamed/dbWeb/website/key_files"
FUNCTIONAL_SPEC_KEYS = get_functional_spec()
FUNCTIONAL_MODE_KEYS = get_functional_mode()
FUNCTIONAL_TEST_KEYS = get_functional_test()

@views.route('/', methods=['GET'])
# @login_required 
def home(): 
    if current_user.is_authenticated:
        logging.info(f"HOME:  At Home ... ")   
        logging.info(f"HOME:  Retrieving All User Requests ")   
        user_prev_requests = Request.query.filter_by(user_id=current_user.id).all()
        logging.info(f"HOME:  Rendering User Info ")     
        
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=user_prev_requests, py_enumerate=enumerate, py_json_loads=json.loads, len=len, spec_keys=FUNCTIONAL_SPEC_KEYS, mode_keys=FUNCTIONAL_MODE_KEYS, test_keys=FUNCTIONAL_TEST_KEYS) 
    else:
        return redirect(url_for('auth.login'))


'''
    
'''
@views.route('/render-new-request', methods=['POST'])
def render_request():
    if current_user.is_authenticated:
        logging.info(f"Submit Request:  Rendering Request")    
        
        request_data = json.loads(request.data)
        logging.info(f"Submit Request:  request_data = {request_data}")
        data = json.dumps(request_data)
        
        protocol = int(request_data['MajorSystemMode'].split('LP')[-1])
        board_setup = int(request_data['byte-mode'].split('x')[-1])
        dfi2ckratio = int(request_data['DFI2CKRatio'])
        baud = int(request_data['baud'])
        
        print(f"board_setup = {board_setup}")
        
        # Add new request
        new_request = Request(user_id=current_user.id, data=data, status='In Progress')
        db.session.add(new_request)
        db.session.commit()
        
        # Render All Requests
        user_prev_requests = Request.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=user_prev_requests, py_enumerate=enumerate, py_json_loads=json.loads, len=len, spec_keys=FUNCTIONAL_SPEC_KEYS, mode_keys=FUNCTIONAL_MODE_KEYS, test_keys=FUNCTIONAL_TEST_KEYS)
    else:
        return redirect(url_for('auth.login'))


'''
    After a new request is rendered on the home page by views.render_request, this route queries the database for the arguments passed, verifies the csrStruct file, and updates the status of the request on the page.
'''
@views.route('/process-new-request', methods=['POST'])
def process_request():
    
    if current_user.is_authenticated:
        all_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        request_data = json.loads(request.data)
        
        logging.info(f"Process-Request:      current_user = {current_user}")
        logging.info(f"Process-Request:      all_user_requests = {all_user_requests}")
        logging.info(f"Process-Request:      request_data({type(request_data)}) = {request_data}")
        
        protocol = int(request_data['MajorSystemMode'].split('LP')[-1])
        board_setup = int(request_data['byte-mode'].split('x')[-1])
        dfi2ckratio = int(request_data['DFI2CKRatio'])
        baud = int(request_data['baud'])
        logging.info(f"Process-Request:      request_data({type(request_data)}) = {request_data}")
        phy_cfgs = current_user.phy_cfgs
        
        # TODO: Determine criteria for choosing which phy_cfg will be used if there's multiple
        request_data['phy_cfg'] = phy_cfgs[1]
        
        logging.info("Process-Request:      Get New Request from DB")
        
        all_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        new_request = max(all_user_requests, key=attrgetter('id'))  # Ids are assigned chronologically
        logging.info(f"Process-Request:     new_request = {new_request}")
        
        # if all_user_requests:
        #     logging.info(f"Process-Request:      all_user_requests = {all_user_requests}" )
        # else:
        #     logging.info(f"Process-Request:      all_user_requests EMPTY " )
        #     return 500
        
        ## Query CSR DB
        logging.info("Process-Request:      Query CSR DB")
        output_baud = query_csr_db(out_path=CSRSTRUCT_OUTDIR, args=request_data)
        
        logging.info("Process-Request:      Updating Status")
        filename = f"csrInitStruct_cfg{phy_cfgs[1]}_LP{protocol}_x{board_setup}_{output_baud}Mbps.txt"
            
        # Successful Query
        if (output_baud) and (os.path.exists(os.path.join(CSRSTRUCT_OUTDIR, filename))):
            new_request.status = 'Ready'            # Update request status in db
            new_request.output_rate = output_baud   # Update db with chosen baud
            db.session.commit()
        else:                                       # Requested struct not in db
            new_request.status = 'Under Review'
            new_request.output_rate = output_baud
            db.session.commit()
            # NOTE: File JIRA
            
        logging.info("Process-Request:      Rendering Template")
        
        updated_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=updated_user_requests, py_enumerate=enumerate, py_json_loads=json.loads, len=len, spec_keys=FUNCTIONAL_SPEC_KEYS, mode_keys=FUNCTIONAL_MODE_KEYS, test_keys=FUNCTIONAL_TEST_KEYS) 
    else:
        return redirect(url_for('auth.login'))


def handler(request_data):
    with app.app_context():
        
        logging.info("Handler:       ... ")
        logging.info(f"Handler:       current_user.id = {current_user.id}")
        
        table_obj = db.metadata.tables['request'] # TODO: there's another way of using reflectio in tut
        
        logging.info(f"Handler:       {table_obj}")
        query = db.session.query(table_obj)
        logging.info(f"Handler:       query before = {query}")
        query = query.filter(
            table_obj.c.user_id == current_user.id
        )
        logging.info(f"Handler:       query after = {query}")
        return query


@views.route('/download/<idx>', methods=['GET'])
# @login_required
def download(idx):
    if current_user.is_authenticated:
        # Get the idx that is sent
        
        logging.info(f"Download:       idx = {idx}")
        
        # query db, match the idx
        all_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        csr_request = all_user_requests[int(idx)]
        logging.info(f"Download:       all_user_requests = {all_user_requests}")
        logging.info(f"Download:       csr_request = {csr_request}")
        
        # get request info; phy_cfg, protocol. board_setup, output_baud
        csr_request_data = json.loads(csr_request.data)
        logging.info(f"Download:       csr_request_data({type(csr_request_data)}) = {csr_request_data}")
        
        protocol = csr_request_data['MajorSystemMode'].split('LP')[-1]
        board_setup = csr_request_data['byte-mode']
        phy_cfg = current_user.phy_cfgs[1]  # TODO: again picking schema here
        output_baud = csr_request.output_rate
        
        logging.info(f"Download:       protocol = {protocol}")
        logging.info(f"Download:       board_setup = {board_setup}")
        logging.info(f"Download:       phy_cfg = {phy_cfg}")
        logging.info(f"Download:       output_baud = {output_baud}")
        
        # get correct file path
        file_name = f"csrInitStruct_cfg{phy_cfg}_LP{protocol}_x{board_setup}_{output_baud}Mbps.txt"
        file_path = os.path.join(CSRSTRUCT_OUTDIR, file_name)

        if os.path.exists(file_path):
            csr_request.status = 'Complete'
            db.session.commit()
            return send_file(file_path, as_attachment=True)
        else:                                # Error along the way
            csr_request.status = 'Complete'
            db.session.commit()
    else:
        return redirect(url_for('auth.login'))

# NOTE: NOT WORKING - have to reload page for it to show
@views.route('/request-error', methods=['POST'])
def request_error():
    flash('Error in submitting request', category='error')
    return redirect(url_for('views.home', user=current_user))

@views.route('/request-success', methods=['POST'])
def request_success():
    flash('Request Submitted', category='success')
    return redirect(url_for('views.home', user=current_user))



@views.route('/vac', methods=['GET'])
def render_vac():
    return render_template("vac.html", user=None)

'''

Next steps 
1) Customization for each user
    1.1) Which keys to display
    1.2) Default parameters
    1.3) Allowed parameters, e.g. LP5 only
    1.4) Factoring in release date
2) Verification and Postprocessing
    2.1) Adding/removing keys from file
    2.2) Using the release date and the db entry date to get the correct csrinit executable and testing the file with that
    2.3) Client-side input validation and updating available configurations based on input, make sure invalid requests don't even make it through 













Next:
1) DONE Unsuccessful query, both in handler and in views.py
2) Input validation using bootstrap
3) DONEish Adding more options to modal
4) DONEish User configs
5) DONE Change Major sys mode to protocol, minormode to board setup ....
6) Release dates input, request date change to date, same with csrDB inputs - Bootstrap date picker
7) TODO-Determine criteria for choosing which phy_cfg will be used if there's multiple
8) DONE Download
9) Not adding duplicates in update flow
10) Add aditional parameters button
11) Client-side input validation
12) Run sim after generating file
13) 400 and 500 page

Big:
1) Admin user
    - maybe add an exit code column that can indicate weither the query ran but didn't find anything OR an error occured and reflect that for the admin user ONLY
2) Distribution to multiple users - run locally, test it with Mihail




'''