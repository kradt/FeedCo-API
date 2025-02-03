from sqlalchemy.orm import Session

from src.applications import models
from src.applications.schemas import ApplicationSearch, ApplicationBase, ApplicationUpdate, RatingCreate


def get_all(db: Session,
            queryset: ApplicationSearch):
    query = db.query(models.Application).filter_by(deleted=False)
    if queryset.name:
        query = query.filter(models.Application.name.like(f"%{queryset.name}%"))
    if queryset.description:
        query = query.filter(models.Application.description.like(f"%{queryset.description}%"))
    if queryset.user_id:
        query = query.filter_by(user_id=queryset.user_id)
    return query.all()


def exists(db: Session, name: str, description: str):
    app = db.query(models.Application).filter_by(name=name, description=description).all()
    return bool(app)


def get(db: Session, application_id: int):
    return db.query(models.Application).filter_by(id=application_id).first()


def create(db: Session, application: ApplicationBase, user_id: int):
    new_application = models.Application(
        name=application.name,
        description=application.description,
        date_created=application.date_created,
        hide_reviews=application.hide_reviews,
        user_id=user_id)
    db.add(new_application)
    db.commit()
    return new_application


def update(db: Session, application_data: ApplicationUpdate, application_id: int):
    application = get(db, application_id)
    if application_data.name:
        application.name = application_data.name
    if application.description:
        application.description = application_data.description
    if application_data.hide_reviews:
        application.hide_reviews = application_data.hide_reviews
    db.add(application)
    db.commit()
    return application


def delete(db: Session, application_id: int):
    application = get(db, application_id)
    db.delete(application)
    db.commit()


def rate(db: Session, rating_data: RatingCreate, application_id: int):
    application = get(db, application_id)

    review = models.Review(title=rating_data.review.title,
                           user_id=rating_data.user_id,
                           body=rating_data.review.body) if rating_data.review else None
    rating = models.Rating(grade=rating_data.grade, user_id=rating_data.user_id)
    rating.application = application
    rating.review = review
    db.add(rating)
    db.commit()
    return rating