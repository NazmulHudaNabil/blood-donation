from app.database import engine, Base
import app.models

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Recreating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset successfully! (Now only containing users and blood_requests)")
