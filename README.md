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

The main advantage of this framework over others is asynchrony. This allows processing requests from multiple users simultaneously. This framework supports webhooks as well as others, but I use regular polling instead, because I chose [AWS](https://aws.amazon.com/?nc1=h_ls) as the platform for deployment the bot, which allows the bot to work without falling asleep.

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

### Services
Heroku and AWS are most often used as the main platforms for deployment the bot. Less often - Google Cloud Platform and Pythonanywhere.

In the end, I chose AWS. This is due to the fact that AWS allocates the most RAM. Other services, including heroku, allocate much less RAM to the user. But this is not the only difference. On heroku, the bot eventually falls asleep, this is fixed by webhooks, but it makes it harder to work. Also, there is no direct access to the GPU on heroku, but we are not particularly interested in this, since I still only put the CPU part of PyTorch (still in order to save memory). If you write simple bots, then you should probably pay attention to heroku, it is much easier to use, there are many tutorials on it on the Internet. But to deploy bots with built-in ML/DL models, you need services like AWS that give you more RAM.

You should understand that now we are talking about free features of various services. If you are willing to pay for the deployment of your bot, then the situation will be different.

### Custom setup
[Here](https://github.com/hse-aml/natural-language-processing/blob/master/AWS-tutorial.md) is a pretty good tutorial for AWS.

I did everything according to it until "Connect to your instance using SSH. If you have problems connecting to the instance, try following this troubleshooting guide." point. Except that instead of a server based on Ubuntu 16.04, I used a server based on Ubuntu 20.04 . In fact, this is an important point, if you do not do the same, then nothing will work for you.

I connected to the server using PuTTY. I downloaded the files via WinSCP. [Here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html) are instructions for both of these items.


Then through the PuTTY console I installed PIP using these following commands(At the same time updating the package list):

`$ sudo apt update`

`$ sudo apt install python3-pip`

Next I ran the following code to install all the necessary packages(All information about packages and their versions is contained in the file [requirements.txt](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/requirements.txt)):

`$ pip3 install -r requirements.txt`

After that i created Swap Space. [Here](https://linuxize.com/post/how-to-add-swap-space-on-ubuntu-18-04/) are the instructions.

As a result, I launched the bot with the following command:

`$ python3 main.py`

To make your bot work even when you close the console, write `screen` to the console before running this command (use Ctrl+C if you have already started it), and then use Ctrl+A+D.

### How do I check logs?
What to do if, after closing the console, you want to view the program logs or restart/terminate the program? To do this, you had to write `screen` to the console in advance and use Ctrl+A+D (as I said above). Now it's time to use the following command:

`$ screen -list`

You will see a list of saved screens. See which one has the detached status, and copy the ID of this screen, which consists of several digits (usually 4 or 5) located at the beginning. To access it, use the following command by inserting the number you just copied:

`$ screen -r <THAT NUMBER>`

After that, you will see your previous session in the console where the program was running. If during this time, the program has managed to issue warnings or errors, you will see this and will be able to restart or terminate the program.


### Additional files
This repository also contains files [runtime.txt](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/runtime.txt) and [Procfile](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/Procfile). They will be useful if you still want to try to upload the bot to heroku. After watching a couple of tutorials on this topic, you will understand why they are needed.

Results
-------
To see the results, you can write to the bot yourself. Here I decided not to show them, because the network generating them is still not written by me. You can view them in the [original repository](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer).
