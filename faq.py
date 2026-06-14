"""
routers/faq.py
===============
FAQ API

Full CRUD for Frequently Asked Questions.

PUBLIC (no API key needed):
    GET /api/faqs        -> list all FAQs, ordered by `order` field
    GET /api/faqs/{id}   -> get a single FAQ by id

ADMIN ONLY (require header:  X-API-Key: <your key>):
    POST   /api/faqs        -> create a new FAQ
    PUT    /api/faqs/{id}   -> update an existing FAQ
    DELETE /api/faqs/{id}   -> delete an FAQ
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/api/faqs", tags=["FAQ"])


# ------------------------------------------------------------------
# READ (public)
# ------------------------------------------------------------------
@router.get("", response_model=list[schemas.FAQOut])
def list_faqs(db: Session = Depends(get_db)):
    """Return all FAQs ordered for display."""
    return db.query(models.FAQ).order_by(models.FAQ.order).all()


@router.get("/{faq_id}", response_model=schemas.FAQOut)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = db.query(models.FAQ).filter(models.FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq


# ------------------------------------------------------------------
# CREATE (admin only)
# ------------------------------------------------------------------
@router.post(
    "",
    response_model=schemas.FAQOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_faq(faq: schemas.FAQCreate, db: Session = Depends(get_db)):
    db_faq = models.FAQ(**faq.model_dump())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq


# ------------------------------------------------------------------
# UPDATE (admin only)
# ------------------------------------------------------------------
@router.put(
    "/{faq_id}",
    response_model=schemas.FAQOut,
    dependencies=[Depends(verify_api_key)],
)
def update_faq(faq_id: int, faq: schemas.FAQUpdate, db: Session = Depends(get_db)):
    db_faq = db.query(models.FAQ).filter(models.FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    for field, value in faq.model_dump(exclude_unset=True).items():
        setattr(db_faq, field, value)
    db.commit()
    db.refresh(db_faq)
    return db_faq


# ------------------------------------------------------------------
# DELETE (admin only)
# ------------------------------------------------------------------
@router.delete(
    "/{faq_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    db_faq = db.query(models.FAQ).filter(models.FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db.delete(db_faq)
    db.commit()
    return None