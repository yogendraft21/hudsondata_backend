from sqlalchemy.orm import Session,load_only
from sqlalchemy import select,update,func
from models.users import users,friend_requests
from schemas.user import User,FriendRequestCreate,FriendRequest
from math import ceil

def get_user_by_email(db: Session, email: str):
    return db.execute(select(users).where(users.c.email == email)).fetchone()

def create_user(db: Session, user: User):
    new_user = users.insert().values(email=user.email, password=user.password)
    result = db.execute(new_user)
    db.commit()
    return result.inserted_primary_key


def respond_friend_request(db: Session, friend_request_id: int, to_user_id: int, action: str):
    status = 'accepted' if action == 'accept' else 'rejected'
    
    # Perform the update and check if the row was affected
    result = db.execute(
        update(friend_requests)
        .where(friend_requests.c.from_user_id == friend_request_id)
        .where(friend_requests.c.to_user_id == to_user_id)
        .values(status=status)
    )
    
    if result.rowcount == 0:
        raise ValueError("Friend request not found or not authorized to update this request")
    
    db.commit()


def get_pending_friend_requests(
    db: Session,
    to_user_id: int,
    page: int = 1,
    items_per_page: int = 10,
    search_query: str = None,
    from_user_id: int = None,
):
    query = db.query(friend_requests).filter(
        friend_requests.c.to_user_id == to_user_id,
        friend_requests.c.status == 'pending'
    )
    print(query.all())

    if search_query:
        query = query.filter(friend_requests.c.from_user_id.ilike(f"%{search_query}%"))
    
    total_items = query.count()
    total_pages = ceil(total_items / items_per_page)
    results = query.offset((page - 1) * items_per_page).limit(items_per_page).all()

    from_user_ids = [result.from_user_id for result in results]
    usersList = db.query(users).filter(users.c.id.in_(from_user_ids)).all()

    usersList = [{"id": user.id, "email": user.email} for user in usersList]
    # print(usersList)
    return {"results": usersList, "total_pages": total_pages}



def get_accepted_friends(
    db: Session,
    user_id: int,
    page: int = 1,
    items_per_page: int = 10,
    search_query: str = None,
):
    sent_requests = db.query(friend_requests).filter(
        friend_requests.c.from_user_id == user_id,
        friend_requests.c.status == 'accepted'
    ).with_entities(friend_requests.c.to_user_id)

    received_requests = db.query(friend_requests).filter(
        friend_requests.c.to_user_id == user_id,
        friend_requests.c.status == 'accepted'
    ).with_entities(friend_requests.c.from_user_id)

    # Combine the IDs from both sent and received requests
    friend_ids = sent_requests.union(received_requests).all()
    friend_ids = [friend_id[0] for friend_id in friend_ids]
    # print(friend_ids)

    if friend_ids:
        # Query for users with the combined friend IDs
        friends_query = db.query(users).filter(users.c.id.in_(friend_ids))

        if search_query:
            friends_query = friends_query.filter(users.c.email.ilike(f"%{search_query}%"))

        total_items = friends_query.count()
        total_pages = ceil(total_items / items_per_page)

        results = friends_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

        return [{"id": user.id, "email": user.email} for user in results], {"total_page":total_pages}
    else:
        return [], 0