# Style-Transfer-Telegram-Bot
**Style Transfer Telegram Bot based on GAN. [ENG]**

What is Style Transfer Telegram Bot?
------------------------------------
Style Transfer Telegram Bot is my final project for the course [Deep Learning School by MIPT](https://en.dlschool.org/).

![alt text](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/bot_picture.jpg)

The goal was to create a telegram bot based on a GAN network that can transfer the style from one image to another. It was also necessary to deploy the bot to the server, so that the bot could run smoothly and not fall asleep.

The Bot itself: `@STransferBot` (Telegram)

It is possible that you found the bot by tag and found it not working. The reason most likely was that I stopped supporting the bot some time after it was created, so as not to waste the power of the server I selected (more on this later).

Network
-------
I chose [MSG-Net](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer) by [zhanghang1989](https://github.com/zhanghang1989) as the network that performs style transfer. I took a fully pre-trained model with ready-made weights and immediately made predictions based on it, without additional training for each new image. This made the response process noticeably faster, but it had a slight impact on the quality. The network has shown quite good results. In this repository all the network code is placed in a separate module called [net.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/net.py). I haven't changed the network architecture much, except to [fix an error when loading weights](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer/pull/37). Weights are [here](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/21styles.model). All additional functions for image processing are included in the module [functions.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/functions.py).

Bot
---
I chose [aiogram](https://docs.aiogram.dev/en/latest/index.html) as the main framework for writing the bot.

You can install it by the following command:

`$ pip install -U aiogram`

The main advantage of this framework over others is asynchrony. This allows processing requests from multiple users simultaneously. This framework supports webhooks as well as others, but I use regular polling instead, because I chose [AWS](https://aws.amazon.com/?nc1=h_ls) as the platform for deploying the bot, which allows the bot to work without falling asleep.

The entire code of the bot itself is located in the module [main.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/main.py).

I also decided to add a little protection to the bot. If the user suddenly does not follow the instructions or calls commands in the wrong order, the bot will remind the user what to do.

Setup and manual
----------------
I set up the bot via `@BotFather`, and there I got a unique token for my bot.
Thanks to BotFather's capabilities, I was able to create a more comfortable environment for working with the bot. Here's what it looks like:

![alt text](https://i.paste.pics/9FNRL.png?trs=b3c34831295e8536e18a14e9781531fc90ffaddafe24b85c5d67a98a23b69e3c)

![alt text](https://i.paste.pics/9FNR3.png?trs=b3c34831295e8536e18a14e9781531fc90ffaddafe24b85c5d67a98a23b69e3c)

![alt text](https://i.paste.pics/9FNQ5.png)

![alt text](https://i.paste.pics/9FNQR.png?trs=b3c34831295e8536e18a14e9781531fc90ffaddafe24b85c5d67a98a23b69e3c)

**Before running my code, make sure that you get your own token from BotFather and specify it in the file main.py.**

Deploy
------
Heroku and AWS are most often used as the main platforms for deploying the bot. Less often - Google Cloud Platform and Pythonanywhere.

Results
-------
To see the results, you can write to the bot yourself. Here I decided not to show them, because the network generating them is still not written by me. You can view them in the [original repository](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer).
