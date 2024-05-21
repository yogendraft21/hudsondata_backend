# HUDSON DATA BACKEND ASSIGNMENT

A simple CRUD Application

## Usage

Clone the project and follow the steps below for MAC
```
python3

# create a virtual environment
python3 -m venv venv

# activate the virtual environment
. venv/bin/activate

# install the required packages inside venv
pip3 install -r requirements.txt

# if you need to upgrade pip for package compatibility please run the command below
# and install the require package again
pip3 install --upgrade pip

# run the project with uvicorn autoreload to watch the file changes
uvicorn main:app --reload

# deactivate the virtual environment
deactivate

# Access the swagger API docs
http://127.0.0.1:8000/docs
```

# API Endpoints

<div class="endpoint">
    <span class="method POST">POST</span>
    <strong>/user/register</strong>
    <p>Create User</p>
</div>
<div class="endpoint">
    <span class="method POST">POST</span>
    <strong>/user/login</strong>
    <p>Login</p>
</div>
<div class="endpoint">
    <span class="method POST">POST</span>
    <strong>/user/send-friend-request</strong>
    <p>Send Friend Request</p>
</div>
<div class="endpoint">
    <span class="method PUT">PUT</span>
    <strong>/user/respond-friend-request</strong>
    <p>Respond Friend Request Endpoint</p>
</div>
<div class="endpoint">
    <span class="method GET">GET</span>
    <strong>/user/list-friends</strong>
    <p>List Friends</p>
</div>
<div class="endpoint">
    <span class="method GET">GET</span>
    <strong>/user/list-pending-requests</strong>
    <p>List Pending Requests</p>
</div>

