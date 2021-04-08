<p align="center">
<img src="media/nepalstonks.png" width="35%" height="auto"><br>
<strong>
A telegram channel that informs about the upcoming stocks, issues, and investment opportunities that are announced inside Nepal.
</strong>
</p>

### Screenshots

<span align="center">
<img src="media/one.jpg" width="49%" height="auto">
<img src="media/two.jpg" width="49%" height="auto">
</span><br>

### Overview

A channel that publishes stocks related to `IPOs`, `FPOs`, `Mutual Funds`, `Right Shares` & `Debentures`. It is backed by a `telegram-bot` that does all the heavy lifting. It fetches the latest issues from an API and sends them directly to this telegram channel. An automated `github-action` runs it every day at an appointed time to check if there are any new issues available. As an automation-loving guy, I just saved myself many clicks of `sharesansar` or other similar portals we get these information from.

### Prerequisites

- Python 3 or higher
- Github Account
- Telegram Account
- SQLite Database

### Used Tools & Technologies

- SQLite: A database for storing stocks
- SQLAlchemy: SQL toolkit and object-relational mapper for Python
- Github Actions: CI/CD that makes it easy to automate all your software workflows

### Environment Variables

- `CHANNEL` = 'The telegram channel you want to send updates e.g @nepstonks'
- `BOT_TOKEN` = 'Bot Token generated from @botfather on telegram'
- `BOT_USERNAME` = 'Bot username generated from @botfather on telegram'
- `API_URL` = 'URL from where stocks are fetched (POST REQUEST)'
- `ORIGIN` = 'Origin needed for header when POST request is sent'
- `ORIGIN` = 'Origin needed for header from where it was referred'
- `PDF_URL` = 'URL that stores the uploaded PDF'

### Run & Setups

- [Install & activate virtual environment in the project root folder](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
- Add `.env` file in this folder & add all the environment variables with values given <a href="https://github.com/sidbelbase/nepstonks#environment-variables">here</a>
- Run `python -m pip install -r requirements.txt`
- Run `python app.py`

### Links

<strong><a target="_blank" href="https://t.me/nepstonks">telegram channel > t.me/nepstonks</a></strong><br>

Inspired from <a target="_blank" href="https://github.com/amitness/auto-investment">auto-investment.</a> Feel free to fork or star to your liking.

### Made with ❤️ in Nepal.
