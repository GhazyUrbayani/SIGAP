"""Initialize the database safely on Render startup.

This script checks if the database is already seeded by looking for the admin user.
If it is empty, it runs the three seed scripts automatically.
This makes it safe to run in the render.yaml startCommand.
"""

import asyncio
import sys

from sqlalchemy import select

from app.database import async_session_factory
from app.models.user import User

from scripts.seed_kelurahan import seed as seed_kel
from scripts.seed_dummy_indicators import seed as seed_ind
from scripts.run_initial_uss import run as seed_uss

async def check_and_seed():
    async with async_session_factory() as db:
        # Check if users exist
        try:
            result = await db.execute(select(User).limit(1))
            user = result.scalar_one_or_none()
        except Exception as e:
            print(f"Database error during check (maybe migrations didn't run?): {e}")
            sys.exit(1)
            
        if user is not None:
            print("✅ Database is already seeded. Skipping initial data generation.")
            return
            
    print("🚀 Database is empty. Running initial seed scripts...")
    
    print("Step 1: Seeding Kelurahan & Users...")
    await seed_kel()
    
    print("Step 2: Seeding Dummy Indicators...")
    await seed_ind()
    
    print("Step 3: Running Initial USS Engine...")
    await seed_uss()
    
    print("🎉 All initial database setup completed successfully!")

if __name__ == "__main__":
    asyncio.run(check_and_seed())
