from app import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db_cmd():
    """Cria tabelas no banco (via SQLAlchemy)."""
    with app.app_context():
        db.create_all()
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    app.run(host=app.config.get("API_HOST", "0.0.0.0"), port=app.config.get("API_PORT", 5000), debug=True)

