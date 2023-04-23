from aiogram import Router, F, types
from aiogram.filters import Text

from states import LoginStateGroup
from keyboards import subjects_inline_kb, detail_inline_kb
from utils.assistants import get_subject
from utils.sql import get_user_token

router = Router()


@router.message(LoginStateGroup.login, Text('Посмотреть свои баллы'))
async def cmd_marks_check(message: types.Message):
    kb = await subjects_inline_kb.get(message.from_user.id)
    pg = Paginator(data=kb, size=5, dp=router)
    await message.answer('Выберите предмет из списка', reply_markup=pg())


@router.callback_query(LoginStateGroup.login, Text('go_back'))
async def back_to_list(callback: types.CallbackQuery):
    kb = await subjects_inline_kb.get(callback.from_user.id)
    pg = Paginator(data=kb, size=5, dp=router)
    await callback.message.edit_text(text='Выберите предмет из списка', inline_message_id=callback.inline_message_id,
                                     reply_markup=pg())
    await callback.answer()


@router.callback_query(LoginStateGroup.login, lambda callback: callback.data.isnumeric())
async def show_weeks(callback: types.CallbackQuery):
    kb = await detail_inline_kb.get()
    subject = await get_subject(await get_user_token(callback.from_user.id), int(callback.data))

    res = f'<b>{subject["SubjectName"]["RU"]}</b>\n\n'

    res += 'Первый рейтинг:\n'
    for week in subject['FirstRatingWeeks']:
        res += f'{week["WeekNumber"]} неделя: <b>{week["Point"]}</b>\n'
    res += f'Рейтинговый контроль: <b>{subject["FirstRatingPoint"]}</b>\n\n'

    res += 'Второй рейтинг:\n'
    for week in subject['SecondRatingWeeks']:
        res += f'{week["WeekNumber"]} неделя: <b>{week["Point"]}</b>\n'
    res += f'Рейтинговый контроль: <b>{subject["SecondRatingPoint"]}</b>\n\n'
    res += f'Экзамен: <b>{subject["ExamPoint"]}</b>\n'
    res += f'Итоговые баллы: {subject["TotalPoint"]}\n'
    res += f'Оценка: <b>{subject["Mark"]}</b>'

    await callback.message.edit_text(text=res, parse_mode='html', inline_message_id=callback.inline_message_id,
                                     reply_markup=kb.as_markup())
    await callback.answer()
