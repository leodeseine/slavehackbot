# Slavehackbot
Hello, this tool will help you to be rich on Slavehack2.

My favourite use is:
* Create an account
* Bot with it 1 day
* Buy CPU with all the money
* Stop the bot
* Change Bot IP
* With the main account, upload a miner on the bot
* Create a ne account and repeat !

> You will win 1,500,000$ a day this way, per account

# Configuration
1. Connect to https://www.slavehack2.com/
2. Connect the account you want to bot with
3. Open developpers tools to get your cookie number and csrf (network tab)
![slavehackbot](https://preview.ibb.co/hZcb8K/Capture_d_e_cran_2018_08_21_a_20_10_40.png)
4. Get the CSRF and the Cookie (for the cookie, do not copy the 'Slavehack=')
5. Edit configuration.ini

> Bot is configured to play mission 1-10, no others !
> When you are level 1 you can only start mission 1-5
> I advise to configure MIN_MISSION to 1 and MAX_MISSION to 5, always

# Installation
You need Python3 to use this bot.

module requests must also be installed

`pip3 install requests`

Clone the directory where you want


# Use the bot
1. Edit the file: configuration.ini
2. Be sure that the bot has no mission started
3. Be sure that the bot is not connected to a remote target
4. Launch a terminal/cmd
5. Go to bot directory
6. `Python3 slave_botv2.py`

# Don't forget a VPN !
And never use your main account on the same network as your bot ! stay safe, be rich (as they say ;))

# TODO List
- [x] Connect to slavehack2
- [x] Erase remote logs (bot IP only)
- [x] Erase local logs (all)
- [x] Play mission (delete one)
- [x] format harddrive (every 15 seconds default) when people get detected on bot computer
- [x] Ransomware detection (every 60s default)
- [x] Transfer money to BTC, then pay ransomware (when detected)
- [ ] proxy http requests
- [ ] play local commands when needed

