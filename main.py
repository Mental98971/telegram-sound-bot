import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultAudio, Message
from aiogram import F
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Boolean, BigInteger
from slugify import slugify

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
Session = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()

class Sound(Base):
    __tablename__ = "sounds"
    keyword = Column(String, primary_key=True)
    file_id = Column(String)
    owner_id = Column(BigInteger)
    deleted = Column(Boolean, default=False)

async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(F.audio)
    async def save_audio(msg: Message):
        await msg.answer("Send keyword")
        audio = msg.audio

        @dp.message()
        async def get_key(m: Message):
            key = slugify(m.text)[:32]
            async with Session() as s:
                s.add(Sound(keyword=key, file_id=audio.file_id, owner_id=m.from_user.id))
                await s.commit()
            await m.answer(f"Saved as {key}")

    @dp.inline_query()
    async def inline(q: InlineQuery):
        async with Session() as s:
            res = await s.execute(
                Sound.__table__.select().where(
                    Sound.keyword.contains(q.query),
                    Sound.deleted == False
                )
            )
            sounds = res.fetchall()

        results = [
            InlineQueryResultAudio(
                id=r.keyword,
                audio_file_id=r.file_id,
                title=r.keyword
            )
            for r in sounds
        ]

        await q.answer(results, cache_time=1)

    await dp.start_polling(bot)

asyncio.run(start())
