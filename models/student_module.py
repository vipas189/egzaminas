from extensions import db

student_module = db.Table(
    "student_module",
    db.Column("student_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("module_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True),
)
