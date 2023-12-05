from sqlalchemy import Column, Integer, Text, Enum, PrimaryKeyConstraint
from app.extensions import db

# CREATE TABLE startpage_sections (
#     version_id INT AUTO_INCREMENT,
#     version_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     section ENUM('INFORMATION', 'PRIORITIES'),
#     content TEXT,
#     PRIMARY KEY (version_id, version_date, section)
# );

class StartPageSections(db.Model):
    __tablename__ = 'startpage_sections'

    version_id = Column(Integer, autoincrement=True)
    version_date = Column(db.DateTime, server_default=('CURRENT_TIMESTAMP'))
    section = Column(Enum('INFORMATION', 'PRIORITIES', 'HEADING', name='section_types'))
    content = Column(Text)

    __table_args__ = (
        PrimaryKeyConstraint('version_id', 'version_date', 'section'),
    )