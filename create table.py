from database import Base, engine



print(" Creating tables in PostgreSQL database...")
Base.metadata.create_all(bind=engine)
print(" Tables created successfully!")
