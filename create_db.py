from main import Base, engine  # adjust this if Base and engine are from another file

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
