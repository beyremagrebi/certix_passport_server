import json
import logging
import smtplib
from email.message import EmailMessage
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import current_app


logger = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    pass


class EmailService:
    @staticmethod
    def _send_smtp(
        *,
        recipient: str,
        subject: str,
        html_content: str,
    ) -> None:
        host = current_app.config.get("SMTP_HOST")
        username = current_app.config.get("SMTP_USERNAME")
        password = current_app.config.get("SMTP_PASSWORD")
        sender = current_app.config.get("EMAIL_FROM_ADDRESS")
        port = current_app.config["SMTP_PORT"]

        if not host or not username or not password or not sender:
            raise EmailDeliveryError(
                "SMTP is not configured. Set SMTP_HOST, SMTP_USERNAME, "
                "SMTP_PASSWORD, and EMAIL_FROM_ADDRESS."
            )

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = recipient
        message.set_content("Please use an HTML-capable email client to view this message.")
        message.add_alternative(html_content, subtype="html")

        try:
            if current_app.config["SMTP_USE_SSL"]:
                with smtplib.SMTP_SSL(host, port, timeout=10) as client:
                    client.login(username, password)
                    client.send_message(message)
                return

            with smtplib.SMTP(host, port, timeout=10) as client:
                client.ehlo()
                if current_app.config["SMTP_USE_TLS"]:
                    client.starttls()
                    client.ehlo()
                client.login(username, password)
                client.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            logger.exception("%s delivery failed.", subject)
            raise EmailDeliveryError(
                f"{subject} could not be sent through SMTP."
            ) from exc

    @staticmethod
    def _send(
        *,
        recipient: str,
        recipient_name: str,
        subject: str,
        html_content: str,
        log_description: str,
    ) -> None:
        provider = current_app.config["EMAIL_PROVIDER"]

        if provider == "console":
            logger.warning("%s for %s: %s", log_description, recipient, html_content)
            return

        if provider == "smtp":
            EmailService._send_smtp(
                recipient=recipient,
                subject=subject,
                html_content=html_content,
            )
            return

        if provider != "brevo":
            raise EmailDeliveryError("Unsupported email provider.")

        api_key = current_app.config.get("EMAIL_API_KEY")
        sender = current_app.config.get("EMAIL_FROM_ADDRESS")
        if not api_key or not sender:
            raise EmailDeliveryError(
                "Email provider is not configured. Set EMAIL_API_KEY and "
                "EMAIL_FROM_ADDRESS."
            )

        payload = json.dumps(
            {
                "sender": {
                    "email": sender,
                    "name": current_app.config["EMAIL_FROM_NAME"],
                },
                "to": [{"email": recipient, "name": recipient_name}],
                "subject": subject,
                "htmlContent": html_content,
            }
        ).encode("utf-8")
        request = Request(
            "https://api.brevo.com/v3/smtp/email",
            data=payload,
            headers={
                "accept": "application/json",
                "api-key": api_key,
                "content-type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=10) as response:
                if response.status < 200 or response.status >= 300:
                    raise EmailDeliveryError("Email provider rejected the message.")
        except (HTTPError, URLError, TimeoutError) as exc:
            logger.exception("%s delivery failed.", log_description)
            raise EmailDeliveryError(
                f"{log_description} could not be sent."
            ) from exc

    @staticmethod
    def send_confirmation_email(
        *,
        recipient: str,
        recipient_name: str,
        confirmation_url: str,
    ) -> None:
        EmailService._send(
            recipient=recipient,
            recipient_name=recipient_name,
            subject="Confirm your Certix Passport email",
            html_content=(
                f"<p>Hello {recipient_name},</p>"
                "<p>Confirm your email address by clicking the link below:</p>"
                f'<p><a href="{confirmation_url}">Confirm email address</a></p>'
                "<p>This link expires soon and can only be used once.</p>"
            ),
            log_description="Email confirmation link",
        )

    @staticmethod
    def send_password_reset_email(
        *,
        recipient: str,
        recipient_name: str,
        reset_url: str,
    ) -> None:
        EmailService._send(
            recipient=recipient,
            recipient_name=recipient_name,
            subject="Reset your Certix Passport password",
            html_content=(
                f"<p>Hello {recipient_name},</p>"
                "<p>Reset your password by clicking the link below:</p>"
                f'<p><a href="{reset_url}">Reset password</a></p>'
                "<p>This link expires soon and can only be used once.</p>"
            ),
            log_description="Password reset link",
        )
