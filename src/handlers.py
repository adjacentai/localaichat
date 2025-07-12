import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .assistant.ai_connector import AIConnector
from .assistant.dialog_history import DialogHistory
from .assistant.prompts import create_main_prompt
from .keyboards import get_reset_keyboard
from config import MODEL_NAME


def register_handlers(dp: Dispatcher, bot: Bot, ai_connector: AIConnector, dialog_history: DialogHistory, processing_users: set):
    @dp.message(CommandStart())
    async def handle_start_command(message: Message):
        user_id = message.from_user.id
        dialog_history.clear_context(user_id)
        
        start_message = (
            f"👋 Hi! I'm your local AI assistant.\n"
            f"The dialog has been reset. We can start over.\n\n"
            f"🤖 Model online: `{MODEL_NAME}`"
        )
        
        await message.answer(start_message, reply_markup=get_reset_keyboard())
        logging.info(f"User {user_id} started a new dialog.")

    @dp.callback_query(lambda c: c.data == 'reset_context')
    async def handle_reset_callback(callback: CallbackQuery):
        user_id = callback.from_user.id
        dialog_history.clear_context(user_id)
        await callback.answer("Context has been reset!")

        reset_message = (
            f"Dialog has been reset. You can start over.\n\n"
            f"🤖 Model online: `{MODEL_NAME}`"
        )

        await callback.message.answer(reset_message, reply_markup=get_reset_keyboard())
        logging.info(f"User {user_id} reset the context via button.")

    @dp.message(F.content_type.in_({
        ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT, 
        ContentType.AUDIO, ContentType.STICKER, ContentType.VOICE,
        ContentType.VIDEO_NOTE
    }))
    async def handle_unsupported_content(message: Message):
        await message.answer("Sorry, I can only work with text. 😔")


    @dp.message()
    async def handle_chat_message(message: Message):
        user_id = message.from_user.id
        user_text = message.text
        
        if not user_text:
            return

        if user_id in processing_users:
            logging.warning(f"User {user_id} sent a message while the previous one was being processed. Ignoring.")
            return

        logging.info(f"Received message from {user_id}: '{user_text}'")
        
        processing_users.add(user_id)
        try:
            await bot.send_chat_action(user_id, 'typing')

            dialog_history.add_message(user_id, "user", user_text)
            
            current_history = dialog_history.get_context(user_id)
            messages = create_main_prompt(current_history)
            
            ai_response = await ai_connector.get_response(messages)

            if ai_response:
                dialog_history.add_message(user_id, "assistant", ai_response)
                context_info = dialog_history.get_context_info(user_id)
                response_text = (
                    f"{ai_response}\n\n"
                    f"💾 Context: {context_info['messages']}/{context_info['max_messages']}"
                )
                await message.answer(response_text, reply_markup=get_reset_keyboard())
            else:
                await message.answer(
                    "😔 Couldn't get a response from the AI. Please try again later.",
                    reply_markup=get_reset_keyboard()
                )

        except Exception as e:
            logging.error(f"Error processing message from {user_id}: {e}", exc_info=True)
            await message.answer(
                "😔 An internal error occurred. Please try resetting the dialog.",
                reply_markup=get_reset_keyboard()
            )
        finally:
            processing_users.remove(user_id) 