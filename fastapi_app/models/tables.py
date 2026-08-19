from datetime import datetime, date, time
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class Category(Base):
    __tablename__ = 'blog_category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(50))


class Blog(Base):
    __tablename__ = 'blog_blog'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(50))
    author_id: Mapped[int | None] = mapped_column(ForeignKey('accounts_adminuser.id'))
    category_id: Mapped[int | None] = mapped_column(ForeignKey('blog_category.id'))
    content: Mapped[str] = mapped_column(Text)
    featured_image: Mapped[str] = mapped_column(String(500))
    tags: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(10))
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    views_count: Mapped[int] = mapped_column(Integer)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class Event(Base):
    __tablename__ = 'events_event'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(20))
    event_date: Mapped[date] = mapped_column(Date)
    event_time: Mapped[time] = mapped_column(Time)
    venue: Mapped[str] = mapped_column(String(200))
    image: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    registration_link: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(10))


class Faculty(Base):
    __tablename__ = 'faculty_faculty'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    designation: Mapped[str] = mapped_column(String(24))
    specialization: Mapped[str] = mapped_column(String(500))
    email: Mapped[str] = mapped_column(String(254))
    phone: Mapped[str] = mapped_column(String(15))
    scholar_link: Mapped[str] = mapped_column(String(200))
    profile_link: Mapped[str | None] = mapped_column(String(500))
    photo: Mapped[str] = mapped_column(String(500))
    bio: Mapped[str] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)


class GalleryImage(Base):
    __tablename__ = 'gallery_galleryimage'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    image: Mapped[str] = mapped_column(String(500))
    thumbnail: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(100))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime)


class ContactMessage(Base):
    __tablename__ = 'contact_contactmessage'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime)


class NewsItem(Base):
    __tablename__ = 'news_newsitem'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    slug: Mapped[str] = mapped_column(String(260))
    category: Mapped[str] = mapped_column(String(20))
    summary: Mapped[str] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text)
    is_pinned: Mapped[bool] = mapped_column(Boolean)
    attachment: Mapped[str | None] = mapped_column(String(500))
    external_link: Mapped[str] = mapped_column(String(200))
    is_published: Mapped[bool] = mapped_column(Boolean)
    published_at: Mapped[datetime] = mapped_column(DateTime)
    views_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class ScheduleItem(Base):
    __tablename__ = 'events_scheduleitem'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(20))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    start_time: Mapped[time | None] = mapped_column(Time)
    end_time: Mapped[time | None] = mapped_column(Time)
    venue: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    registration_link: Mapped[str] = mapped_column(String(200))
    attachment: Mapped[str | None] = mapped_column(String(500))
    is_academic_calendar: Mapped[bool] = mapped_column(Boolean)
    is_published: Mapped[bool] = mapped_column(Boolean)
    source_event_id: Mapped[int | None] = mapped_column(ForeignKey('events_event.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class DepartmentDocument(Base):
    __tablename__ = 'core_departmentdocument'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(32))
    academic_year: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    pdf_file: Mapped[str | None] = mapped_column(String(500))
    external_url: Mapped[str] = mapped_column(String(500))
    display_order: Mapped[int] = mapped_column(Integer)
    is_published: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class PlacementStat(Base):
    __tablename__ = 'core_placementstat'
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    students_placed: Mapped[int] = mapped_column(Integer)
    total_offers: Mapped[int] = mapped_column(Integer)
    highest_package: Mapped[str] = mapped_column(String(50))
    average_package: Mapped[str] = mapped_column(String(50))
    top_recruiters: Mapped[str] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer)
    is_published: Mapped[bool] = mapped_column(Boolean)


class DepartmentLab(Base):
    __tablename__ = 'core_departmentlab'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    domain: Mapped[str] = mapped_column(String(255))
    computers_count: Mapped[int] = mapped_column(Integer)
    printers_count: Mapped[int] = mapped_column(Integer)
    ups_info: Mapped[str] = mapped_column(String(100))
    software_installed: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500))
    display_order: Mapped[int] = mapped_column(Integer)


class DepartmentMilestone(Base):
    __tablename__ = 'core_departmentmilestone'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    metric_value: Mapped[str] = mapped_column(String(50))
    icon: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    display_order: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)


class AdminUser(Base):
    __tablename__ = 'accounts_adminuser'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    password: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(16))
    is_active: Mapped[bool] = mapped_column(Boolean)
