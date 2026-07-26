from extensions import db
from datetime import datetime

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)

    slug = db.Column(db.String(300), unique=True, nullable=False)

    category = db.Column(db.String(100))

    excerpt = db.Column(db.Text)

    content = db.Column(db.Text, nullable=False)

    seo_title = db.Column(db.String(255))

    seo_description = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)