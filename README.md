# HexMail - Secure Email Bot for Discord

## Overview
**HexMail** is a secure and efficient Discord bot that enables users to send and receive emails directly within their Discord servers. Designed with gamers, streamers, and Discord communities in mind, HexMail bridges the gap between email communication and Discord, offering convenience and security.

---

## Features
- **Send Emails**: Compose and send emails directly from Discord channels.
- **Receive Emails**: Get email notifications and messages delivered straight to your Discord inbox.
- **Secure Communication**: Built with encryption and authentication to ensure email security.
- **Customizable Settings**: Configure email notifications, sender accounts, and other preferences.
- **Multi-User Support**: Allows multiple users to link their email accounts in a shared server.
- **Ease of Use**: Simple commands and an intuitive setup process.

---

## Technologies Used
HexMail is built using:

- **Programming Language**: Python
- **Discord API**: For Discord bot integration.
- **Email Libraries**: (e.g., smtplib, imaplib) for email handling.
- **Database**: MongoDB or SQLite for storing user configurations and email logs.
- **Security**: OAuth2 for authentication and encryption protocols for secure communication.

---

## Getting Started

### Prerequisites
- A Discord account.
- Admin privileges on the server where the bot will be deployed.
- An email account (e.g., Gmail, Outlook) to link with HexMail.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hexmail.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hexmail
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     DISCORD_TOKEN=your_discord_bot_token
     CLIENT_ID=your_discord_client_id
     CLIENT_SECRET=your_discord_client_secret
     EMAIL_HOST=email_provider_host
     EMAIL_PORT=email_provider_port
     EMAIL_USER=your_email_address
     EMAIL_PASS=your_email_password
     ```
5. Start the bot:
   ```bash
   python bot.py
   ```

6. Invite the bot to your Discord server using the OAuth2 URL:
   ```
   https://discord.com/oauth2/authorize?client_id=your_client_id&permissions=8&scope=bot
   ```

---

## Usage

### Basic Commands
- `.ping` : Bot tells you its latency in ms.
- `.new_auth` : Bot sends you a authorization link in your DM.
- `.summery` : Bot send general info about your account in your DM.
- `.recent` : Bot sends most recent email in your DM.
- `.recent last <N>` : Bot sends last "N" recent email in your DM.
- `.search <Keywords>` : Bot gives you the result after the search

### Example Workflow
1. Link your email account using `!hexmail setup`.
2. Send an email with `!hexmail send recipient@example.com Hello World This is a test message!`.
3. Check incoming emails using `!hexmail inbox`.

---

## Contributing
We welcome contributions to improve HexMail! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes.
4. Submit a pull request for review.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements
- [Discord API](https://discord.com/developers/docs/intro) for enabling Discord bot functionality.
- Python libraries like [smtplib](https://docs.python.org/3/library/smtplib.html) for email integration.

---

## Disclaimer
This bot is intended for personal and community use. Ensure you comply with Discord's terms of service and email provider policies.

---

