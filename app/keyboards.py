from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, keyboard_button
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Профиль')],
    [KeyboardButton(text='Купить впн')],
    [ 
        KeyboardButton(text='Информация о токене'),
        KeyboardButton(text="Поддержка")
    ],
],
                          resize_keyboard =True,
                          input_field_placeholder="Понажимай на кнопки")


profile = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')]
],
                          resize_keyboard =True,
                          input_field_placeholder="Профиль")


# Инлайн-кнопка для покупки VPN
buy_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить 1 месяц / 150 руб", callback_data="buy_vpn_1_month")
    ]
])


main_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Статистика.')],
],
                          resize_keyboard =True,
                          input_field_placeholder="Понажимай на кнопки")











inlinebuttons = ["TEST", "TEST1", "TEST2", "TEST3", "TEST4", "TEST5", "TEST6", "TEST7", "TEST8", "TEST9", "TEST10", "TEST11", "TEST12", "TEST13", "TEST14", "TEST15", "TEST16", "TEST17", "TEST18", "TEST19", "TEST20", "TEST21", "TEST22", "TEST23", "TEST24", "TEST25", "TEST26", "TEST27", "TEST28", "TEST29", "TEST30", "TEST31", "TEST32", "TEST33", "TEST34", "TEST35", "TEST36", "TEST37", "TEST38", "TEST39", "TEST40", "TEST41", "TEST42", "TEST43", "TEST44", "TEST45", "TEST46", "TEST47", "TEST48", "TEST49", "TEST50", "TEST51", "TEST52", "TEST53", "TEST54", "TEST55", "TEST56", "TEST57", "TEST58", "TEST59", "TEST60", "TEST61", "TEST62", "TEST63", "TEST64", "TEST65", "TEST66", "TEST67", "TEST68", "TEST69", "TEST70", "TEST71", "TEST72", "TEST73", "TEST74", "TEST75", "TEST76", "TEST77", "TEST78", "TEST79", "TEST80", "TEST81", "TEST82", "TEST83", "TEST84", "TEST85", "TEST86", "TEST87", "TEST88", "TEST89", "TEST90", "TEST91", "TEST92", "TEST93", "TEST94", "TEST95", "TEST96", "TEST97", "TEST98", "TEST99", "TEST100", "TEST101", "TEST102", "TEST103", "TEST104", "TEST105", "TEST106", "TEST107", "TEST108", "TEST109", "TEST110", "TEST111", "TEST112", "TEST113", "TEST114", "TEST115", "TEST116", "TEST117", "TEST118", "TEST119", "TEST120", "TEST121", "TEST122", "TEST123", "TEST124", "TEST125", "TEST126", "TEST127", "TEST128", "TEST129", "TEST130", "TEST131", "TEST132", "TEST133", "TEST134", "TEST135", "TEST136", "TEST137", "TEST138", "TEST139", "TEST140", "TEST141", "TEST142", "TEST143", "TEST144", "TEST145", "TEST146", "TEST147", "TEST148", "TEST149", "TEST150", "TEST151", "TEST152", "TEST153", "TEST154", "TEST155", "TEST156", "TEST157", "TEST158", "TEST159", "TEST160", "TEST161", "TEST162", "TEST163", "TEST164", "TEST165", "TEST166", "TEST167", "TEST168", "TEST169", "TEST170", "TEST171", "TEST172", "TEST173", "TEST174", "TEST175", "TEST176", "TEST177", "TEST178", "TEST179", "TEST180", "TEST181", "TEST182", "TEST183", "TEST184", "TEST185", "TEST186", "TEST187", "TEST188", "TEST189", "TEST190", "TEST191", "TEST192", "TEST193", "TEST194", "TEST195", "TEST196", "TEST197", "TEST198", "TEST199", "TEST200", "TEST201", "TEST202", "TEST203", "TEST204", "TEST205", "TEST206", "TEST207", "TEST208", "TEST209", "TEST210", "TEST211", "TEST212", "TEST213", "TEST214", "TEST215", "TEST216", "TEST217", "TEST218", "TEST219", "TEST220", "TEST221", "TEST222", "TEST223", "TEST224", "TEST225", "TEST226", "TEST227", "TEST228", "TEST229", "TEST230", "TEST231", "TEST232", "TEST233", "TEST234", "TEST235", "TEST236", "TEST237", "TEST238", "TEST239", "TEST240", "TEST241", "TEST242", "TEST243", "TEST244", "TEST245", "TEST246", "TEST247", "TEST248", "TEST249", "TEST250", "TEST251", "TEST252", "TEST253", "TEST254", "TEST255", "TEST256", "TEST257", "TEST258", "TEST259", "TEST260", "TEST261", "TEST262", "TEST263", "TEST264", "TEST265", "TEST266", "TEST267", "TEST268", "TEST269", "TEST270", "TEST271", "TEST272", "TEST273", "TEST274", "TEST275", "TEST276", "TEST277", "TEST278", "TEST279", "TEST280", "TEST281", "TEST282", "TEST283", "TEST284", "TEST285", "TEST286", "TEST287", "TEST288", "TEST289", "TEST290", "TEST291", "TEST292", "TEST293", "TEST294", "TEST295", "TEST296", "TEST297", "TEST298", "TEST299", "TEST300"]

async def inline_buttons():
  keyboard = InlineKeyboardBuilder()
  for button in inlinebuttons:
    keyboard.add(InlineKeyboardButton(text=button, url="https://ya.ru/"))
  return keyboard.adjust(1).as_markup()