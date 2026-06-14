"""
routers/footer.py
==================
FOOTER API

Manages footer links, contact details, social media links, and copyright text.

PUBLIC (no API key needed):
    GET /api/footer
        -> returns contact details + copyright, footer links, social media links

ADMIN ONLY (require header:  X-API-Key: <your key>):
    PUT    /api/footer/contact                  -> update contact details + copyright
    POST   /api/footer/links                    -> add a footer link
    PUT    /api/footer/links/{id}               -> update a footer link
    DELETE /api/footer/links/{id}               -> delete a footer link
    POST   /api/footer/social-links             -> add a social media link
    PUT    /api/footer/social-links/{id}        -> update a social media link
    DELETE /api/footer/social-links/{id}        -> delete a social media link
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/api/footer", tags=["Footer"])


def _get_or_create_footer_config(db: Session) -> models.FooterConfig:
    """The footer config is a SINGLETON (only one row ever exists)."""
    config = db.query(models.FooterConfig).first()
    if not config:
        config = models.FooterConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


# ------------------------------------------------------------------
# GET full footer (contact/copyright + links + social links)
# ------------------------------------------------------------------
@router.get("", response_model=schemas.FooterFullOut)
def get_footer(db: Session = Depends(get_db)):
    config = _get_or_create_footer_config(db)
    links = db.query(models.FooterLink).order_by(models.FooterLink.order).all()
    social_links = (
        db.query(models.SocialMediaLink).order_by(models.SocialMediaLink.order).all()
    )
    return schemas.FooterFullOut(config=config, links=links, social_links=social_links)


# ------------------------------------------------------------------
# CONTACT DETAILS + COPYRIGHT
# ------------------------------------------------------------------
@router.put(
    "/contact",
    response_model=schemas.FooterConfigOut,
    dependencies=[Depends(verify_api_key)],
)
def update_footer_contact(
    payload: schemas.FooterConfigUpdate, db: Session = Depends(get_db)
):
    """Update email, phone, address, and/or copyright text."""
    config = _get_or_create_footer_config(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    db.commit()
    db.refresh(config)
    return config


# ------------------------------------------------------------------
# FOOTER LINKS (full CRUD)
# ------------------------------------------------------------------
@router.get("/links", response_model=list[schemas.FooterLinkOut])
def list_footer_links(db: Session = Depends(get_db)):
    return db.query(models.FooterLink).order_by(models.FooterLink.order).all()


@router.post(
    "/links",
    response_model=schemas.FooterLinkOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_footer_link(link: schemas.FooterLinkCreate, db: Session = Depends(get_db)):
    db_link = models.FooterLink(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


@router.put(
    "/links/{link_id}",
    response_model=schemas.FooterLinkOut,
    dependencies=[Depends(verify_api_key)],
)
def update_footer_link(
    link_id: int, link: schemas.FooterLinkUpdate, db: Session = Depends(get_db)
):
    db_link = db.query(models.FooterLink).filter(models.FooterLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Footer link not found")
    for field, value in link.model_dump(exclude_unset=True).items():
        setattr(db_link, field, value)
    db.commit()
    db.refresh(db_link)
    return db_link


@router.delete(
    "/links/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_footer_link(link_id: int, db: Session = Depends(get_db)):
    db_link = db.query(models.FooterLink).filter(models.FooterLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Footer link not found")
    db.delete(db_link)
    db.commit()
    return None


# ------------------------------------------------------------------
# SOCIAL MEDIA LINKS (full CRUD)
# ------------------------------------------------------------------
@router.get("/social-links", response_model=list[schemas.SocialMediaLinkOut])
def list_social_links(db: Session = Depends(get_db)):
    return (
        db.query(models.SocialMediaLink).order_by(models.SocialMediaLink.order).all()
    )


@router.post(
    "/social-links",
    response_model=schemas.SocialMediaLinkOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_social_link(link: schemas.SocialMediaLinkCreate, db: Session = Depends(get_db)):
    db_link = models.SocialMediaLink(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


@router.put(
    "/social-links/{link_id}",
    response_model=schemas.SocialMediaLinkOut,
    dependencies=[Depends(verify_api_key)],
)
def update_social_link(
    link_id: int, link: schemas.SocialMediaLinkUpdate, db: Session = Depends(get_db)
):
    db_link = (
        db.query(models.SocialMediaLink)
        .filter(models.SocialMediaLink.id == link_id)
        .first()
    )
    if not db_link:
        raise HTTPException(status_code=404, detail="Social media link not found")
    for field, value in link.model_dump(exclude_unset=True).items():
        setattr(db_link, field, value)
    db.commit()
    db.refresh(db_link)
    return db_link


@router.delete(
    "/social-links/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_social_link(link_id: int, db: Session = Depends(get_db)):
    db_link = (
        db.query(models.SocialMediaLink)
        .filter(models.SocialMediaLink.id == link_id)
        .first()
    )
    if not db_link:
        raise HTTPException(status_code=404, detail="Social media link not found")
    db.delete(db_link)
    db.commit()
    return None