import logging

from aiogram import Bot, Dispatcher, executor, types

from net import *  # Import architecture
from functions import *  # Import functions

# Set API_TOKEN. You must have your own.
API_TOKEN = ''

# Configure logging.
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize the net.
style_model = Net(ngf=128)
style_model.load_state_dict(torch.load('21styles.model'), False)

# Initializing the flag to distinguish between images content and style.
flag = True
# Initializing flags to check for images.
content_flag = False
style_flag = False


def transform(content_root, style_root, im_size):
    """Function for image transformation."""
    content_image = tensor_load_rgbimage(content_root, size=im_size,
                                         keep_asp=True).unsqueeze(0)
    style = tensor_load_rgbimage(style_root, size=im_size).unsqueeze(0)
    style = preprocess_batch(style)
    style_v = Variable(style)
    content_image = Variable(preprocess_batch(content_image))
    style_model.setTarget(style_v)
    output = style_model(content_image)
    tensor_save_bgrimage(output.data[0], 'result.jpg', False)

    # Clear the RAM.
    del content_image
    del style
    del style_v
    del output
    torch.cuda.empty_cache()


@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    """Test function."""
    await message.answer(text='It works!')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """
    Outputs a small instruction when the corresponding command is received.
    """
    await message.answer(text="Hi, "
                              "I'll help you move the style from one photo "
                              "to another. To do this, first send me an image"
                              " with the content (if you suddenly want to "
                              "change it, use the /cancel command and then "
                              "send a new image), and then send me the image"
                              " that you want to transfer the style from."
                              " After that, I will send you a picture with"
                              " the transferred style. When the server is"
                              " heavily loaded, this can take up to 30 seconds,"
                              " but it usually only takes 5-10 seconds.")


@dp.message_handler(content_types=['photo'])
async def photo_processing(message):
    """
    Triggered when the user sends an image and saves it for further processing.
    """

    global flag
    global content_flag
    global style_flag

    # The bot is waiting for a picture with content from the user.
    if flag:
        await message.photo[-1].download('content.jpg')
        await message.answer(text='I got the first one.'
                                  ' Now send me a photo with style or use '
                                  'the /cancel command to choose '
                                  'a different content image.')
        flag = False
        content_flag = True  # Now the bot knows that the content image exists.

    # The bot is waiting for a picture with style from the user.
    else:
        await message.photo[-1].download('style.jpg')
        await message.answer(text='I got the second one. Now use the /continue'
                                  ' command or the /cancel command to change'
                                  ' the image style.')
        flag = True
        style_flag = True  # Now the bot knows that the style image exists.


@dp.message_handler(commands=['cancel'])
async def photo_processing(message: types.Message):
    """Allows the user to select a different image with content or style."""

    global flag
    global content_flag

    # Let's make sure that there is something to cancel.
    if not content_flag:
        await message.answer(text="You haven't uploaded the content image yet.")
        return

    if flag:
        flag = False
    else:
        flag = True
    await message.answer(text='Successfully!')


@dp.message_handler(commands=['creator'])
async def creator(message: types.Message):
    """Displays information about the bot's Creator."""
    link = 'https://github.com/t0efL/Style-Transfer-Telegram-Bot'
    await message.answer(text=f'I have been created by toefL.\
                              \nMy code is here: {link}')


@dp.message_handler(commands=['continue'])
async def contin(message: types.Message):
    """Preparing for image processing."""

    # Let's make sure that the user has added both images.
    if not (content_flag * style_flag):  # Conjunction
        await message.answer(text="You haven't uploaded both images yet.")
        return

    # Adding answer options.
    res = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
    res.add(types.KeyboardButton(text="Low"))
    res.add(types.KeyboardButton(text="Medium"))
    res.add(types.KeyboardButton(text="High"))

    await message.answer(text="Okay, now it's time to choose the quality"
                              " (resolution) of the future image. The better "
                              "the quality, the slower the processing time."
                              " If you want to start all over again at this"
                              " step, just send me the content image again,"
                              " and then the style image.", reply_markup=res)


@dp.message_handler(lambda message: message.text in ("Low", "Medium", "High"))
async def processing(message: types.Message):
    """Image processing depending on the selected quality."""

    if message.text == 'Low':
        image_size = 256
    elif message.text == 'Medium':
        image_size = 300
    else:
        image_size = 350

    await message.answer(text='Processing has started and will take some time. '
                              'Wait for a little bit.',
                         reply_markup=types.ReplyKeyboardRemove())
    transform('content.jpg', 'style.jpg', image_size)
    with open('result.jpg', 'rb') as file:
        await message.answer_photo(file, caption='Done!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
