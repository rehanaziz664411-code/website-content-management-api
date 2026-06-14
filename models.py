"""
models.py
=========
SQLAlchemy ORM models (database tables) for the four content sections:

    1. Header  -> HeaderConfig, NavMenuItem, HeaderActionButton
    2. Hero    -> HeroSection, HeroCTAButton
    3. FAQ     -> FAQ
    4. Footer  -> FooterConfig, FooterLink, SocialMediaLink

"Config" tables (HeaderConfig, HeroSection, FooterConfig) are treated
as SINGLETONS -> only one row will ever exist (id=1), representing the
single global configuration for that section. The other tables can hold
many rows (e.g. many nav menu items, many FAQs, etc.).
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base


# ============================================================
# 1. HEADER
# ============================================================

class HeaderConfig(Base):
    """Singleton row holding the site logo information."""
    __tablename__ = "header_config"

    id = Column(Integer, primary_key=True, index=True)
    logo_url = Column(String, nullable=True)
    logo_alt_text = Column(String, nullable=True)


class NavMenuItem(Base):
    """A single item in the header's navigation menu."""
    __tablename__ = "nav_menu_items"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)        # e.g. "Home", "About Us"
    url = Column(String, nullable=False)          # e.g. "/about"
    order = Column(Integer, default=0)            # controls display order
    is_active = Column(Boolean, default=True)     # show/hide without deleting


class HeaderActionButton(Base):
    """A call-to-action button shown in the header (e.g. 'Sign Up')."""
    __tablename__ = "header_action_buttons"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    url = Column(String, nullable=False)
    style = Column(String, default="primary")     # primary, secondary, outline...
    order = Column(Integer, default=0)


# ============================================================
# 2. HERO SECTION
# ============================================================

class HeroSection(Base):
    """Singleton row holding the homepage hero content."""
    __tablename__ = "hero_section"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subtitle = Column(Text, nullable=True)
    banner_image_url = Column(String, nullable=True)


class HeroCTAButton(Base):
    """A call-to-action button shown inside the hero section."""
    __tablename__ = "hero_cta_buttons"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    url = Column(String, nullable=False)
    style = Column(String, default="primary")
    order = Column(Integer, default=0)


# ============================================================
# 3. FAQ
# ============================================================

class FAQ(Base):
    """A single Frequently Asked Question + answer pair."""
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


# ============================================================
# 4. FOOTER
# ============================================================

class FooterConfig(Base):
    """Singleton row holding contact details and copyright text."""
    __tablename__ = "footer_config"

    id = Column(Integer, primary_key=True, index=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_address = Column(String, nullable=True)
    copyright_text = Column(String, nullable=True)


class FooterLink(Base):
    """A single link shown in the footer (e.g. Privacy Policy)."""
    __tablename__ = "footer_links"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    url = Column(String, nullable=False)
    group_name = Column(String, default="General")   # e.g. "Company", "Legal"
    order = Column(Integer, default=0)


class SocialMediaLink(Base):
    """A single social media link shown in the footer."""
    __tablename__ = "social_media_links"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)         # e.g. "facebook", "twitter"
    url = Column(String, nullable=False)
    icon = Column(String, nullable=True)               # icon name/class, optional
    order = Column(Integer, default=0)