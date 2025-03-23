from extensions import db


module_prerequisites = db.Table(
    "module_prerequisites",
    db.Column("module_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True),
    db.Column(
        "prerequisite_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True
    ),
)
