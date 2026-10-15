import html
from aiogram import Router, types
from aiogram.types import (
    InlineQueryResultCachedAudio,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from config import BOT_USERNAME
from database import get_cached_audio
from services.music_service import search_tracks

router = Router()

@router.inline_query()
async def inline_search_handler(inline_query: types.InlineQuery):
    query = inline_query.query.strip()
    articles = []

    # 1. If query is a cached video_id or media id directly
    if query:
        cached = await get_cached_audio(query)
        if cached and cached.get("file_id"):
            esc_artist = html.escape(cached.get("artist", "Track"))
            esc_title = html.escape(cached.get("title", "Music"))
            articles.append(
                InlineQueryResultCachedAudio(
                    id=f"cached_{query}",
                    audio_file_id=cached["file_id"],
                    caption=f"🎧 <b>{esc_artist} — {esc_title}</b>\n\n📥 <i>@{BOT_USERNAME} orqali tinglang</i>",
                    parse_mode="HTML"
                )
            )

    search_term = query if query else "uzbek xit 2026"
    results = await search_tracks(search_term, limit=15)

    for item in results:
        vid_id = item["id"]
        if query and vid_id == query:
            continue
        title = item["title"]
        artist = item["artist"]
        duration = item.get("duration", 0)
        thumb = item.get("thumbnail")

        esc_artist = html.escape(artist)
        esc_title = html.escape(title)

        # Check if we have cached telegram file_id
        cached = await get_cached_audio(vid_id)
        if cached and cached.get("file_id"):
            articles.append(
                InlineQueryResultCachedAudio(
                    id=f"cached_{vid_id}",
                    audio_file_id=cached["file_id"],
                    caption=f"🎧 <b>{esc_artist} — {esc_title}</b>\n\n📥 <i>@{BOT_USERNAME} orqali yuklab olindi</i>",
                    parse_mode="HTML"
                )
            )
        else:
            # Article with direct link to bot /start <vid_id>
            bot_link = f"https://t.me/{BOT_USERNAME}?start={vid_id}"
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🎧 Yuklab olish / Tinglash", url=bot_link)
            ]])

            content_text = (
                f"🎧 <b>{esc_artist} — {esc_title}</b>\n"
                f"⏱ <b>Davomiyligi:</b> {item.get('duration_str', '00:00')}\n\n"
                f"📥 <i>@{BOT_USERNAME} orqali yuklab olish</i>"
            )

            articles.append(
                InlineQueryResultArticle(
                    id=vid_id,
                    title=f"{artist} - {title}",
                    description=f"⏱ {item.get('duration_str', '00:00')}",
                    thumbnail_url=thumb,
                    input_message_content=InputTextMessageContent(
                        message_text=content_text,
                        parse_mode="HTML"
                    ),
                    reply_markup=kb
                )
            )

    await inline_query.answer(
        results=articles[:25],
        cache_time=60,
        is_personal=True
    )

