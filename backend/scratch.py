import asyncio
from sqlalchemy import select
from app.database import async_session_factory
from app.models.alert import Alert
from app.models.kelurahan import Kelurahan
from app.models.uss_score import USSScore

async def main():
    async with async_session_factory() as db:
        res = await db.execute(select(Kelurahan.id, Kelurahan.nama))
        kelurahans = {row.id: row.nama for row in res.all()}
        
        print("Latest USS Scores:")
        for kel_id, nama in kelurahans.items():
            res = await db.execute(
                select(USSScore).where(USSScore.kelurahan_id == kel_id).order_by(USSScore.computed_at.desc()).limit(1)
            )
            score = res.scalar_one_or_none()
            if score:
                print(f"{nama}: USS={score.uss}")

        print("\nAlerts:")
        res = await db.execute(select(Alert).where(Alert.is_resolved == False))
        for alert in res.scalars():
            print(f"[{kelurahans[alert.kelurahan_id]}] Level: {alert.trigger_level}, USS: {alert.uss_value}")

if __name__ == "__main__":
    asyncio.run(main())
