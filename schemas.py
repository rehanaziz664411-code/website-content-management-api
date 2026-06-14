"""
schemas.py
==========
Pydantic schemas used for request validation and response serialization.

Naming convention used throughout:
    *Base    -> shared fields common to create/read
    *Create  -> fields required when creating a new record (POST)
    *Update  -> all fields optional, used for partial updates (PUT)
    *Out     -> what gets returned to the client (includes `id`)

`model_config = ConfigDict(from_attributes=True)` allows these schemas
to be created directly from SQLAlchemy ORM objects (formerly `orm_mode`).
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ============================================================
# 1. HEADER SCHEMAS
# ============================================================

class HeaderConfigBase(BaseModel):
    logo_url: Optional[str] = None
    logo_alt_text: Optional[str] = None


class HeaderConfigUpdate(HeaderConfigBase):
    """All fields optional -> client can update just one field at a time."""
    pass


class HeaderConfigOut(HeaderConfigBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NavMenuItemBase(BaseModel):
    label: str
    url: str
    order: int = 0
    is_active: bool = True


class NavMenuItemCreate(NavMenuItemBase):
    pass


class NavMenuItemUpdate(BaseModel):
    label: Optional[str] = None
    url: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class NavMenuItemOut(NavMenuItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ActionButtonBase(BaseModel):
    label: str
    url: str
    style: str = "primary"
    order: int = 0


class ActionButtonCreate(ActionButtonBase):
    pass


class ActionButtonUpdate(BaseModel):
    label: Optional[str] = None
    url: Optional[str] = None
    style: Optional[str] = None
    order: Optional[int] = None


class ActionButtonOut(ActionButtonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HeaderFullOut(BaseModel):
    """Combined response returned by GET /api/header"""
    logo: HeaderConfigOut
    navigation_menu: List[NavMenuItemOut]
    action_buttons: List[ActionButtonOut]


# ============================================================
# 2. HERO SECTION SCHEMAS
# ============================================================

class HeroSectionBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    banner_image_url: Optional[str] = None


class HeroSectionUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    banner_image_url: Optional[str] = None


class HeroSectionOut(HeroSectionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CTAButtonBase(BaseModel):
    label: str
    url: str
    style: str = "primary"
    order: int = 0


class CTAButtonCreate(CTAButtonBase):
    pass


class CTAButtonUpdate(BaseModel):
    label: Optional[str] = None
    url: Optional[str] = None
    style: Optional[str] = None
    order: Optional[int] = None


class CTAButtonOut(CTAButtonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class HeroFullOut(BaseModel):
    """Combined response returned by GET /api/hero"""
    section: HeroSectionOut
    cta_buttons: List[CTAButtonOut]


# ============================================================
# 3. FAQ SCHEMAS
# ============================================================

class FAQBase(BaseModel):
    question: str
    answer: str
    order: int = 0
    is_active: bool = True


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class FAQOut(FAQBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 4. FOOTER SCHEMAS
# ============================================================

class FooterConfigBase(BaseModel):
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_address: Optional[str] = None
    copyright_text: Optional[str] = None


class FooterConfigUpdate(FooterConfigBase):
    pass


class FooterConfigOut(FooterConfigBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class FooterLinkBase(BaseModel):
    label: str
    url: str
    group_name: str = "General"
    order: int = 0


class FooterLinkCreate(FooterLinkBase):
    pass


class FooterLinkUpdate(BaseModel):
    label: Optional[str] = None
    url: Optional[str] = None
    group_name: Optional[str] = None
    order: Optional[int] = None


class FooterLinkOut(FooterLinkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SocialMediaLinkBase(BaseModel):
    platform: str
    url: str
    icon: Optional[str] = None
    order: int = 0


class SocialMediaLinkCreate(SocialMediaLinkBase):
    pass


class SocialMediaLinkUpdate(BaseModel):
    platform: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None


class SocialMediaLinkOut(SocialMediaLinkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class FooterFullOut(BaseModel):
    """Combined response returned by GET /api/footer"""
    config: FooterConfigOut
    links: List[FooterLinkOut]
    social_links: List[SocialMediaLinkOut]