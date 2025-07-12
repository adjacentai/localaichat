from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_reset_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Reset Context", callback_data="reset_context")]
    ]) 