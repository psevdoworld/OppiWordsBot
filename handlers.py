from aiogram.utils import executor
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.types.message import ContentTypes

from bot.ilt import tasks

from bot.app.setlanguage import setlanguage
from bot.app.delete import delete
from bot.app.subscribe import subscribe
from bot.app.show import show
from bot.app.generic import generic
from bot.app.admin import admin
from bot.app.addtext import addtext
from bot.app.wordlist import wordlist
from bot.app.addwords import addwords
from bot.app.learn import reading, speaking, writing, control, syntaxis, texts, summary
from bot.app.core import dp, user_state

#
# help - get help
# start - start the bot and get help
# subscribe - activate paid features of the bot and check your subscription status
# setlanguage - specify a language you want to learn. You can switch between languages or add new ones any time
# addtext - add a text which you want to learn
# addwords - add words to learn
# wordlist - add a list of words (you will have to add definitions after adding the list)
# learn - learn the words you added
# test - test the words you learned
# show - show all added words in alphabetical order
# delete - delete a word form your dictionary
# settings - specify your language
# stop - cancel everything and restart
#


posts_cb = CallbackData('post', 'data', 'action')


# Test independent loop
@dp.message_handler(commands=['notify'])
async def send_notifications_to_users(message: types.Message):
    await admin.send_notifications_to_users(message)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await generic.start_message(message)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await generic.help_message(message)


@dp.message_handler(commands=['stop', 'finish', 'restart'])
async def stop_message(message: types.Message):
    await generic.stop_message(message)

# SETTINGS =========================================================
@dp.message_handler(commands=['settings'])
async def settings_message(message: types.Message):
    await generic.settings_message(message)


@dp.message_handler(lambda message: user_state(message.from_user.id, message.message_id))
async def set_user_language_message(message: types.Message):
    await generic.set_user_language_message(message)


@dp.callback_query_handler(posts_cb.filter(action=["def_source"]))
async def def_source_action(query: types.CallbackQuery, callback_data: dict):
    await generic.def_source_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["def_source_finish"]))
async def def_source_finish_action(query: types.CallbackQuery):
    await generic.def_source_finish_action(query)


# SUBSCRIBE =========================================================

# TODO: one week free; specify number of months; discounted 1 year subscription
# TODO: limit free use?
@dp.message_handler(commands=['subscribe'])
async def start_message(message: types.Message):
    await subscribe.subscribe_command(message)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await subscribe.checkout(pre_checkout_query)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await subscribe.got_payment(message)


# SHOW WORDS ========================================================
@dp.message_handler(commands=['show'])
async def show_command(message: types.Message):
    await show.show_command(message)


# ADDING TEXT========================================================
@dp.message_handler(commands=['addtext'])
async def add_text_command(message: types.Message):
    await addtext.add_text_command(message)


@dp.message_handler(lambda message: user_state(message.from_user.id, "text_added"))
async def add_text(message: types.Message):
    await addtext.add_text(message)


# LEARNING TEXT ====================================================
@dp.message_handler(lambda message: user_state(message.from_user.id, "summarization"))
async def summarization_message(message: types.Message):
    await texts.summarization_message(message)


@dp.callback_query_handler(posts_cb.filter(action=["text_summary"]))
async def do_text_summary_action(query: types.CallbackQuery):
    await summary.do_text_summary_action(query)


@dp.callback_query_handler(posts_cb.filter(action=["text_words"]))
async def do_text_summary_action(query: types.CallbackQuery):
    await summary.do_text_words_action(query)


# ADDING LIST ======================================================
@dp.message_handler(commands=['wordlist'])
async def wordlist_command(message: types.Message):
    await wordlist.wordlist_command(message)


@dp.callback_query_handler(posts_cb.filter(action=["topn"]))
async def topn_action(query: types.CallbackQuery, callback_data: dict):
    await wordlist.topn_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["smart"]))
async def smart_action(query: types.CallbackQuery, callback_data: dict):
    await wordlist.smart_action(query, callback_data)


@dp.message_handler(lambda message: user_state(message.from_user.id, "topn"))
async def adding_word_to_list(message):
    await wordlist.adding_word_to_list(message)


async def adding_list_words(message, query, list_name):
    await wordlist.adding_list_words(message, query, list_name)


@dp.callback_query_handler(posts_cb.filter(action=["next_word_from_list"]))
async def next_word_action(query: types.CallbackQuery, callback_data: dict):
    await wordlist.next_word_action(query, callback_data)


# DELETING =======================================================

@dp.message_handler(commands=['delete'])
async def delete_command(message: types.Message):
    await delete.delete_command(message)


@dp.message_handler(lambda message: user_state(message.from_user.id, "delete"))
async def deleting_word(message):
    await delete.deleting_word(message)


@dp.callback_query_handler(posts_cb.filter(action=["delete"]))
async def delete_action(query: types.CallbackQuery, callback_data: dict):
    await delete.delete_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["delete_list"]))
async def delete_list_action(query: types.CallbackQuery, callback_data: dict):
    await delete.delete_list_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["del_list_keep_words"]))
async def del_list_keep_words_action(query: types.CallbackQuery, callback_data: dict):
    await delete.del_list_keep_words(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["del_list_del_words"]))
async def del_list_del_words_action(query: types.CallbackQuery, callback_data: dict):
    await delete.del_list_del_words_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["keep"]))
async def keep_action(query: types.CallbackQuery, callback_data: dict):
    await delete.keep_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["keep_list"]))
async def keep_list_action(query: types.CallbackQuery, callback_data: dict):
    await delete.keep_list_action(query)


# ==========================================================================================
# Learning

# Checking prerequisites and collecting data
@dp.message_handler(commands=['learn', 'test'])
async def start_learning_message(message):
    await control.start_learning_message(message)


@dp.callback_query_handler(posts_cb.filter(action=["start_learning"]))
async def learning(query: types.CallbackQuery, callback_data: dict):
    await control.learning(query, callback_data)


# Reading errors loop, end of the learning loop if no more words to learn
@dp.callback_query_handler(posts_cb.filter(action=["mc_correct", "reading_errors"]))
async def do_reading_errors(query: types.CallbackQuery, callback_data: dict):
    await reading.do_reading_errors(query, callback_data)


# The learning loop, reading task 1
@dp.callback_query_handler(posts_cb.filter(action=["do_learning"]))
async def do_learning(session):
    await reading.do_learning(session)


@dp.message_handler(lambda message: user_state(message.from_user.id, tasks[1]))
async def type_in_message(message):
    await writing.type_in_message(message)


# reading task 1 answer "I remember"
@dp.callback_query_handler(posts_cb.filter(action=["I_remember"]))
async def i_remember(query: types.CallbackQuery, callback_data: dict):
    await reading.i_remember(query, callback_data)


# reading task showing definition, adding word to the error list
@dp.callback_query_handler(posts_cb.filter(action="show"))
async def callback_show_action(query: types.CallbackQuery, callback_data: dict):
    await reading.callback_show_action(query, callback_data)


# Forgot and I knew that!
@dp.callback_query_handler(posts_cb.filter(action=["forgot", "i_knew"]))
async def callback_forgot_action(query: types.CallbackQuery, callback_data: dict):
    await reading.callback_forgot_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["mc_wrong"]))
async def callback_mc_action(query: types.CallbackQuery, callback_data: dict):
    await reading.callback_mc_action(query, callback_data)


# SENTENCES =======================================================================
@dp.callback_query_handler(posts_cb.filter(action=["unscramble"]))
async def unscramble_message(query: types.CallbackQuery, callback_data: dict):
    await syntaxis.unscramble_message(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["restart_unscramble"]))
async def restart_unscramble_message(query: types.CallbackQuery, callback_data: dict):
    await syntaxis.restart_unscramble_message(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["next_unscramble"]))
async def next_unscramble_message(query: types.CallbackQuery):
    await syntaxis.next_unscramble_message(query)


# VOICE processing ===============================================================

@dp.message_handler(content_types=ContentTypes.VOICE)
async def voice_message(message: types.Message):
    await speaking.voice_message(message)


@dp.callback_query_handler(posts_cb.filter(action=['voice_skip']))
async def voice_skip_action(query: types.CallbackQuery):
    await speaking.voice_skip_action(query)


# ==========================================================================================
# Selecting a language to learn

@dp.message_handler(commands=['setlanguage'])
async def setlanguage_command_message(message: types.Message):
    await setlanguage.setlanguage_command_message(message)


# TODO Make sure I need it. It might be reduntant
@dp.callback_query_handler(posts_cb.filter(action=["setlanguage"]))
async def setlanguage_action(query: types.CallbackQuery, callback_data: dict):
    await setlanguage.setlanguage_action(query, callback_data)


@dp.message_handler(lambda message: user_state(message.from_user.id, "setlanguage"))
async def setlanguage_message(message):
    await setlanguage.setlanguage_message(message)


# ==========================================================================================
# Adding new words

# Getting the command, setting s.status ="/addwords"
@dp.message_handler(commands=['addwords'])
async def addwords_message(message):
    await addwords.addwords_message(message)


@dp.callback_query_handler(posts_cb.filter(action=["skip_list"]))
async def skip_list_action(query: types.CallbackQuery, callback_data: dict):
    await addwords.skip_list_action(query, callback_data)


# Getting a new word typed in by a user and getting definitions
@dp.callback_query_handler(posts_cb.filter(action=["wiktionary_search"]))
async def wiktionary_search_action(query: types.CallbackQuery, callback_data: dict):
    await addwords.wiktionary_search_action(query, callback_data)


@dp.message_handler(lambda message: user_state(message.from_user.id, "/addwords"))
async def wiktionary_search(message):
    await addwords.wiktionary_search(message)


# Adding selected definition
@dp.callback_query_handler(posts_cb.filter(action=["meaning"]))
async def callback_add_meaning_action(query: types.CallbackQuery, callback_data: dict):
    await addwords.callback_add_meaning_action(query, callback_data)


@dp.callback_query_handler(posts_cb.filter(action=["add_user_definition"]))
async def callback_add_user_definition_action(query: types.CallbackQuery, callback_data: dict):
    await addwords.callback_add_user_definition_action(query, callback_data)


@dp.message_handler(lambda message: user_state(message.from_user.id, "adding_user_definition"))
async def adding_words(message):
    await addwords.adding_words(message)


@dp.callback_query_handler(posts_cb.filter(action=["finish_adding_meanings"]))
async def finish_adding_meanings_action(query: types.CallbackQuery, callback_data: dict):
    await addwords.finish_adding_meanings_action(query, callback_data)


# SUBSCRIBE ====================================================


# UNKNOWN input
# ===============================================================

@dp.callback_query_handler()
async def unknow_query_handler(query: types.CallbackQuery):
    await generic.unknow_query_handler(query)


@dp.message_handler()
async def text_message(message):
    await generic.text_message(message)


if __name__ == '__main__':
    # print(sys.argv[1:])
    executor.start_polling(dp, skip_updates=True)