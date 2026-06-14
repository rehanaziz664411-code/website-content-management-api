"""
routers/header.py
==================
HEADER API

Manages the website header: logo, navigation menu, and action buttons.

PUBLIC (no API key needed):
    GET /api/header
        -> returns logo info + full navigation menu + action buttons

ADMIN ONLY (require header:  X-API-Key: <your key>):
    PUT    /api/header/logo                     -> update logo url/alt text
    POST   /api/header/nav-menu                 -> add a navigation menu item
    PUT    /api/header/nav-menu/{item_id}       -> update a navigation menu item
    DELETE /api/header/nav-menu/{item_id}       -> delete a navigation menu item
    POST   /api/header/action-buttons           -> add an action button
    PUT    /api/header/action-buttons/{btn_id}  -> update an action button
    DELETE /api/header/action-buttons/{btn_id}  -> delete an action button
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import verify_api_key

router = APIRouter(prefix="/api/header", tags=["Header"])


def _get_or_create_header_config(db: Session) -> models.HeaderConfig:
    """The header config is a SINGLETON (only one row ever exists)."""
    config = db.query(models.HeaderConfig).first()
    if not config:
        config = models.HeaderConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


# ------------------------------------------------------------------
# GET full header (logo + nav menu + action buttons)
# ------------------------------------------------------------------
@router.get("", response_model=schemas.HeaderFullOut)
def get_header(db: Session = Depends(get_db)):
    config = _get_or_create_header_config(db)
    nav_items = (
        db.query(models.NavMenuItem).order_by(models.NavMenuItem.order).all()
    )
    action_buttons = (
        db.query(models.HeaderActionButton)
        .order_by(models.HeaderActionButton.order)
        .all()
    )
    return schemas.HeaderFullOut(
        logo=config,
        navigation_menu=nav_items,
        action_buttons=action_buttons,
    )


# ------------------------------------------------------------------
# LOGO
# ------------------------------------------------------------------
@router.put(
    "/logo",
    response_model=schemas.HeaderConfigOut,
    dependencies=[Depends(verify_api_key)],
)
def update_logo(payload: schemas.HeaderConfigUpdate, db: Session = Depends(get_db)):
    """Update the site logo URL and/or alt text."""
    config = _get_or_create_header_config(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    db.commit()
    db.refresh(config)
    return config


# ------------------------------------------------------------------
# NAVIGATION MENU (full CRUD)
# ------------------------------------------------------------------
@router.get("/nav-menu", response_model=list[schemas.NavMenuItemOut])
def list_nav_menu(db: Session = Depends(get_db)):
    return db.query(models.NavMenuItem).order_by(models.NavMenuItem.order).all()


@router.post(
    "/nav-menu",
    response_model=schemas.NavMenuItemOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_nav_menu_item(item: schemas.NavMenuItemCreate, db: Session = Depends(get_db)):
    db_item = models.NavMenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/nav-menu/{item_id}",
    response_model=schemas.NavMenuItemOut,
    dependencies=[Depends(verify_api_key)],
)
def update_nav_menu_item(
    item_id: int, item: schemas.NavMenuItemUpdate, db: Session = Depends(get_db)
):
    db_item = db.query(models.NavMenuItem).filter(models.NavMenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Navigation menu item not found")
    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete(
    "/nav-menu/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_nav_menu_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.NavMenuItem).filter(models.NavMenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Navigation menu item not found")
    db.delete(db_item)
    db.commit()
    return None


# ------------------------------------------------------------------
# ACTION BUTTONS (full CRUD)
# ------------------------------------------------------------------
@router.get("/action-buttons", response_model=list[schemas.ActionButtonOut])
def list_action_buttons(db: Session = Depends(get_db)):
    return (
        db.query(models.HeaderActionButton)
        .order_by(models.HeaderActionButton.order)
        .all()
    )


@router.post(
    "/action-buttons",
    response_model=schemas.ActionButtonOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_action_button(btn: schemas.ActionButtonCreate, db: Session = Depends(get_db)):
    db_btn = models.HeaderActionButton(**btn.model_dump())
    db.add(db_btn)
    db.commit()
    db.refresh(db_btn)
    return db_btn


@router.put(
    "/action-buttons/{btn_id}",
    response_model=schemas.ActionButtonOut,
    dependencies=[Depends(verify_api_key)],
)
def update_action_button(
    btn_id: int, btn: schemas.ActionButtonUpdate, db: Session = Depends(get_db)
):
    db_btn = (
        db.query(models.HeaderActionButton)
        .filter(models.HeaderActionButton.id == btn_id)
        .first()
    )
    if not db_btn:
        raise HTTPException(status_code=404, detail="Action button not found")
    for field, value in btn.model_dump(exclude_unset=True).items():
        setattr(db_btn, field, value)
    db.commit()
    db.refresh(db_btn)
    return db_btn


@router.delete(
    "/action-buttons/{btn_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_action_button(btn_id: int, db: Session = Depends(get_db)):
    db_btn = (
        db.query(models.HeaderActionButton)
        .filter(models.HeaderActionButton.id == btn_id)
        .first()
    )
    if not db_btn:
        raise HTTPException(status_code=404, detail="Action button not found")
    db.delete(db_btn)
    db.commit()
    return None