"""
routers/hero.py
================
HERO SECTION API

Manages the homepage hero: title, subtitle, banner image, and CTA buttons.

PUBLIC (no API key needed):
    GET /api/hero
        -> returns title, subtitle, banner image url, and list of CTA buttons

ADMIN ONLY (require header:  X-API-Key: <your key>):
    PUT    /api/hero                     -> update title / subtitle / banner image
    POST   /api/hero/cta-buttons         -> add a CTA button
    PUT    /api/hero/cta-buttons/{id}    -> update a CTA button
    DELETE /api/hero/cta-buttons/{id}    -> delete a CTA button
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/api/hero", tags=["Hero Section"])


def _get_or_create_hero_section(db: Session) -> models.HeroSection:
    """The hero section is a SINGLETON (only one row ever exists)."""
    section = db.query(models.HeroSection).first()
    if not section:
        section = models.HeroSection(title="Welcome to Our Website")
        db.add(section)
        db.commit()
        db.refresh(section)
    return section


# ------------------------------------------------------------------
# GET full hero section (title + subtitle + banner + CTA buttons)
# ------------------------------------------------------------------
@router.get("", response_model=schemas.HeroFullOut)
def get_hero(db: Session = Depends(get_db)):
    section = _get_or_create_hero_section(db)
    cta_buttons = (
        db.query(models.HeroCTAButton).order_by(models.HeroCTAButton.order).all()
    )
    return schemas.HeroFullOut(section=section, cta_buttons=cta_buttons)


# ------------------------------------------------------------------
# UPDATE hero title / subtitle / banner image
# ------------------------------------------------------------------
@router.put(
    "",
    response_model=schemas.HeroSectionOut,
    dependencies=[Depends(verify_api_key)],
)
def update_hero(payload: schemas.HeroSectionUpdate, db: Session = Depends(get_db)):
    section = _get_or_create_hero_section(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    db.commit()
    db.refresh(section)
    return section


# ------------------------------------------------------------------
# CTA BUTTONS (full CRUD)
# ------------------------------------------------------------------
@router.get("/cta-buttons", response_model=list[schemas.CTAButtonOut])
def list_cta_buttons(db: Session = Depends(get_db)):
    return db.query(models.HeroCTAButton).order_by(models.HeroCTAButton.order).all()


@router.post(
    "/cta-buttons",
    response_model=schemas.CTAButtonOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_cta_button(btn: schemas.CTAButtonCreate, db: Session = Depends(get_db)):
    db_btn = models.HeroCTAButton(**btn.model_dump())
    db.add(db_btn)
    db.commit()
    db.refresh(db_btn)
    return db_btn


@router.put(
    "/cta-buttons/{btn_id}",
    response_model=schemas.CTAButtonOut,
    dependencies=[Depends(verify_api_key)],
)
def update_cta_button(
    btn_id: int, btn: schemas.CTAButtonUpdate, db: Session = Depends(get_db)
):
    db_btn = db.query(models.HeroCTAButton).filter(models.HeroCTAButton.id == btn_id).first()
    if not db_btn:
        raise HTTPException(status_code=404, detail="CTA button not found")
    for field, value in btn.model_dump(exclude_unset=True).items():
        setattr(db_btn, field, value)
    db.commit()
    db.refresh(db_btn)
    return db_btn


@router.delete(
    "/cta-buttons/{btn_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_cta_button(btn_id: int, db: Session = Depends(get_db)):
    db_btn = db.query(models.HeroCTAButton).filter(models.HeroCTAButton.id == btn_id).first()
    if not db_btn:
        raise HTTPException(status_code=404, detail="CTA button not found")
    db.delete(db_btn)
    db.commit()
    return None