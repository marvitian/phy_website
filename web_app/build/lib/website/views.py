# Store standard roots for our server
from flask import Blueprint, render_template, request, flash, jsonify, send_file, redirect, url_for, copy_current_request_context
from flask_login import login_required, current_user

from . import db, app, logging #turbo
from operator import attrgetter

from .models import Note, Request
from csrStructDB.queryDB import query_csr_db

import threading, os, json, copy

views = Blueprint('views', __name__)

OPTIONS_REQUIRED = {'MajorSystemMode':'LP4,LP5', 'MinorMode':'8,16', 'DFI2CKRatio':'1,2,4'}
CSRSTRUCT_OUTDIR = "/home/mohamed/dbWeb/website/key_files"

@views.route('/', methods=['GET'])
# @login_required 
def home(): 
    if current_user.is_authenticated:
        logging.info(f"HOME:  At Home ... ")   
        logging.info(f"HOME:  Retrieving All User Requests ")   
        user_prev_requests = Request.query.filter_by(user_id=current_user.id).all()
        logging.info(f"HOME:  Rendering User Info ")     
        
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=user_prev_requests, py_enumerate=enumerate, py_json_loads=json.loads) 
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
        board_setup = int(request_data['MinorMode'])
        dfi2ckratio = int(request_data['DFI2CKRatio'])
        baud = int(request_data['baud'])
        
        # Add new request
        new_request = Request(user_id=current_user.id, data=data, status='In Progress')
        db.session.add(new_request)
        db.session.commit()
        
        # Render All Requests
        user_prev_requests = Request.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=user_prev_requests, py_enumerate=enumerate, py_json_loads=json.loads)
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
        board_setup = int(request_data['MinorMode'])
        dfi2ckratio = int(request_data['DFI2CKRatio'])
        baud = int(request_data['baud'])
        
        logging.info("Process-Request:      Get New Request from DB")
        logging.info(f"Process-Request:     current_user.id({type(current_user.id)}) = {current_user.id}")
        
        all_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        new_request = max(all_user_requests, key=attrgetter('id'))  # Ids are assigned chronologically
        logging.info(f"Process-Request:     new_request = {new_request}")
        
        # if all_user_requests:
        #     logging.info(f"Process-Request:      all_user_requests = {all_user_requests}" )
        # else:
        #     logging.info(f"Process-Request:      all_user_requests EMPTY " )
        #     return 500
            
        logging.info("Process-Request:      Query CSR DB")
        output_baud = query_csr_db(out_path=CSRSTRUCT_OUTDIR, args=request_data)
        
        logging.info("Process-Request:      Updating Status")
        filename = f"csrInitStruct_cfg3_LP{protocol}_x{board_setup}_{output_baud}Mbps.txt"
            
        # Successful Query
        if os.path.exists(os.path.join(CSRSTRUCT_OUTDIR, filename)):
            new_request.status = 'Ready'            # Update request status in db
            new_request.output_rate = output_baud   # Update db with chosen baud
            db.session.commit()
            
        logging.info("Process-Request:      Rendering Template")
        
        updated_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, data=OPTIONS_REQUIRED, prev_requests=updated_user_requests, py_enumerate=enumerate, py_json_loads=json.loads) 
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


@views.route('/download', methods=['GET'])
# @login_required
def download():
    if current_user.is_authenticated:
        # Get the idx that is sent
        request_body = json.loads(request.data)
        req_idx = request_body['req_idx']
        logging.info(f"Download:       request_data = {request_data}")
        logging.info(f"Download:       req_idx = {req_idx}")
        
        # query db, match the idx
        all_user_requests = Request.query.filter_by(user_id=current_user.id).all()
        csr_request = all_user_requests[req_idx]
        logging.info(f"Download:       all_user_requests = {reall_user_requestsquest_data}")
        logging.info(f"Download:       csr_request = {csr_request}")
        
        # get request info; phy_cfg, protocol. board_setup, output_baud
        csr_request_data = json.load(csr_request.data)
        # phy_cfg = 
        protocol = csr_request_data['MajorSystemMode']
        board_setup = csr_request_data['MinorMode']
        
        logging.info(f"Download:       protocol = {protocol}")
        logging.info(f"Download:       board_setup = {board_setup}")
        
        
        # get correct file path
        # file_name = f"csrInitStruct_cfg3_LP{protocol}_x{board_setup}_{output_baud}Mbps.txt"
        # file_path = os.path.join(CSRSTRUCT_OUTDIR, filename)
        # check file path
        #   change request status to complete
        #   if good --> send file

        # Successful Query
        # return send_file(path, as_attachment=True)
        return jsonify({})
    else:
        return redirect(url_for('auth.login'))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # We will look for the noteId that was sent to us, but we are not sending the request as a form, the request will come-in in the data parameter of our request obj which means we need load it as json
    # we will take in request.data which is a string that we sent from deleteNote
    # we take this str and turn it into a python dict object so we can access the noteId
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: # if the note belongs to the user, delete it
            db.session.delete(note)
            db.session.commit()
    return jsonify({})  # flask requires us to return something, we just return an empty json obj

# NOT WORKING - have to reload page for it to show
@views.route('/request-error', methods=['POST'])
def request_error():
    flash('Error in submitting request', category='error')
    return redirect(url_for('views.home', user=current_user))

@views.route('/request-success', methods=['POST'])
def request_success():
    flash('Request Submitted', category='success')
    return redirect(url_for('views.home', user=current_user))

'''

Next:
1) Unsuccessful query, both in handler and in views.py
2) Input validation using bootstrap
3) Adding more options to modal
4) User configs
5) Change Major sys mode to protocol ....

Big:
1) Admin user
2) Distribution to multiple users - run locally, test it with Mihail
















NEXT STEPS:
1) Website Database Handler:
    1.1) Add ability to update status of request
    1.2) 

1) Rest API
2) Threading
3) Task Manager

NEXT:
- Fix processing: we create a request instead of pulling the resuest that was submitted to db in rendering step

'''
# <form method="POST" id="request-form" class="needs-validation" novalidate>
# <button type="submit" class="btn btn-default btn-success" name="action" value="Submit" form="request-form">Save</button>

# /*
#       const form = event.currentTarget;
      
#       try {
#         const formData = new FormData(form);
#         const renderResponseData = await renderRequest({ formData });
#         console.log("Rendering Complete")

#         const prcsResponseData = await processRequest({ formData });
#         console.log("Processing Complete")
#       } catch (error) {
#         // Send request to 'Unexpected Error occured' route
#         // reload window maybe? or just close modal
#         console.error(error);
#         return ;
#       }*/

# 14:39:03: render_request   : Checking Request Data ...
# 14:39:03: render_request:  request_data = {'MajorSystemMode': 'LP5', 'MinorMode': '16', 'DFI2CKRatio': '1', 'baud': '500'}
# 14:39:03: 127.0.0.1 - - [22/Mar/2023 14:39:03] "POST / HTTP/1.1" 200 -
# AT HOME
# 14:39:03: 127.0.0.1 - - [22/Mar/2023 14:39:03] "GET / HTTP/1.1" 200 -
# 14:39:03: 127.0.0.1 - - [22/Mar/2023 14:39:03] "GET /static/style.css HTTP/1.1" 304 -
# 14:39:03: 127.0.0.1 - - [22/Mar/2023 14:39:03] "GET /static/index.js HTTP/1.1" 304 -