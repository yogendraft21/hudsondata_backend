from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import get_db
from datetime import datetime, timedelta
from middleware.auth import get_current_user, auth_handler
from models.index import users, friend_requests
from services import crud
from schemas.user import User, UserCreate, FriendRequest, FriendRequestCreate, FriendRequestResponse
from typing import Optional
from middleware.rateLimit import rate_limit

user_router = APIRouter()

@user_router.post("/register", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_handler.get_password_hash(user.password)
    new_user = users.insert().values(email=user.email, password=hashed_password)
    result = db.execute(new_user)
    db.commit()

    user_id = result.inserted_primary_key[0]
    return {"id": user_id, "email": user.email}

@user_router.post("/login")
def login(user_login: UserCreate, db: Session = Depends(get_db)):
    user = db.execute(select(users).where(users.c.email == user_login.email)).fetchone()

    if not user or not auth_handler.verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = auth_handler.encode_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@user_router.post("/send-friend-request", response_model=None)
def send_friend_request(request_data: FriendRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    rate_limit()
    # Check if the target user exists
    target_user = db.query(users).filter(users.c.id == request_data.to_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    # Check if the user has already sent a friend request to the target user
    existing_request = db.query(friend_requests).filter(
        friend_requests.c.from_user_id == current_user.id,
        friend_requests.c.to_user_id == request_data.to_user_id
    ).first()

    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already sent to this user")

    # Send friend request
    friend_request = friend_requests.insert().values(
        from_user_id=current_user.id,
        to_user_id=request_data.to_user_id
    )
    db.execute(friend_request)
    db.commit()
    return {"message": "Friend request sent successfully"}

@user_router.put("/respond-friend-request", response_model=FriendRequestResponse)
def respond_friend_request_endpoint(request: FriendRequestResponse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if request.action not in ['accept', 'reject']:
        raise HTTPException(status_code=400, detail="Action must be 'accept' or 'reject'")
    
    crud.respond_friend_request(db=db, friend_request_id=request.friend_request_id, to_user_id=current_user.id, action=request.action)
    
    return FriendRequestResponse(friend_request_id=request.friend_request_id, action=request.action)


@user_router.get("/list-friends")
def list_friends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, description="Page number for pagination"),
    per_page: int = Query(10, description="Items per page for pagination"),
    search_query: Optional[str] = Query(None, description="Search query for filtering friends"),
):
    friends_list = crud.get_accepted_friends(
        db=db,
        user_id=current_user.id,
        page=page,
        items_per_page=per_page,
        search_query=search_query
    )
    return friends_list

@user_router.get("/list-pending-requests", response_model=dict)
def list_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search_query: Optional[str] = Query(None, description="Search query for filtering pending requests"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    items_per_page: int = Query(10, le=100, description="Number of items per page for pagination")
):
    pending_requests_data = crud.get_pending_friend_requests(
        db=db,
        to_user_id=current_user.id,
        search_query=search_query,
        page=page,
        items_per_page=items_per_page
    )
    return pending_requests_data



