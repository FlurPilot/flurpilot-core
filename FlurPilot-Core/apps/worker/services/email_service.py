import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger("EmailService")

# Resend Integration
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logging.warning("[!] Resend not installed. Email alerts disabled.")
    logging.warning("   Install with: pip install resend")


class EmailService:
    """
    Email service for FlurPilot alerts and notifications.
    
    Uses Resend API for reliable transactional email delivery.
    Supports HTML and text emails, with templating for common alerts.
    
    Setup:
    1. Get API key from https://resend.com
    2. Verify your domain
    3. Set RESEND_API_KEY in environment
    """
    
    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None):
        """
        Initialize email service.
        
        Args:
            api_key: Resend API key (or from RESEND_API_KEY env)
            from_email: Default sender email (or from RESEND_FROM_EMAIL env)
        """
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.from_email = from_email or os.getenv("RESEND_FROM_EMAIL", "alerts@flurpilot.de")
        
        if not RESEND_AVAILABLE:
            logger.warning("Resend SDK not available")
            return
            
        if self.api_key:
            resend.api_key = self.api_key
            logger.info("[OK] Email service initialized")
        else:
            logger.warning("[!] RESEND_API_KEY not set. Emails will be logged but not sent.")
    
    async def send_alert(self, to: str, subject: str, message: str, 
                        alert_type: str = "info", metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Send an alert email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            message: Alert message (plain text or HTML)
            alert_type: Type of alert (info, warning, error, critical)
            metadata: Additional metadata to include
            
        Returns:
            Email ID if sent successfully, None otherwise
        """
        if not self.api_key or not RESEND_AVAILABLE:
            logger.info(f"[EMAIL LOG] To: {to}, Subject: {subject}")
            logger.info(f"[EMAIL LOG] Message: {message[:100]}...")
            return None
        
        # Build HTML email with styling based on alert type
        html_content = self._build_alert_template(subject, message, alert_type, metadata)
        
        try:
            params = {
                "from": self.from_email,
                "to": [to],
                "subject": f"[FlurPilot] {subject}",
                "html": html_content,
                "text": message  # Plain text fallback
            }
            
            response = resend.Emails.send(params)
            email_id = response.get("id")
            
            logger.info(f"[OK] Alert sent: {email_id}")
            return email_id
            
        except Exception as e:
            logger.error(f"[X] Failed to send alert: {e}")
            return None
    
    async def send_error_alert(self, to: str, error_message: str, 
                              context: Dict[str, Any] = None) -> Optional[str]:
        """
        Send an error alert with detailed context.
        
        Args:
            to: Recipient email
            error_message: Error description
            context: Additional context (e.g., {'parcel_id': '123', 'operation': 'analyze'})
        """
        subject = "[ERROR] System Error Alert"
        
        # Build detailed message
        message = f"""Error: {error_message}

Timestamp: {datetime.now().isoformat()}
"""
        
        if context:
            message += "\nContext:\n"
            for key, value in context.items():
                message += f"  {key}: {value}\n"
        
        return await self.send_alert(to, subject, message, alert_type="error", metadata=context)
    
    async def send_daily_summary(self, to: str, stats: Dict[str, Any]) -> Optional[str]:
        """
        Send daily summary email with system statistics.
        
        Args:
            to: Recipient email
            stats: Dictionary with stats like:
                {
                    'parcels_processed': 150,
                    'documents_found': 45,
                    'errors': 2,
                    'cost': 12.50
                }
        """
        subject = "[SUMMARY] Daily System Summary"
        
        message = f"""Daily Summary for {datetime.now().strftime('%Y-%m-%d')}

Parcels Processed: {stats.get('parcels_processed', 0)}
Documents Found: {stats.get('documents_found', 0)}
Errors: {stats.get('errors', 0)}
Estimated Cost: ${stats.get('cost', 0):.2f}
"""
        
        return await self.send_alert(to, subject, message, alert_type="info", metadata=stats)
    
    async def send_security_alert(self, to: str, alert_details: str) -> Optional[str]:
        """
        Send security-related alert.
        
        Args:
            to: Recipient email
            alert_details: Security alert description
        """
        subject = "[SECURITY] Security Alert"
        return await self.send_alert(to, subject, alert_details, alert_type="critical")
    
    def _build_alert_template(self, title: str, message: str, 
                             alert_type: str, metadata: Dict[str, Any] = None) -> str:
        """
        Build HTML email template with appropriate styling.
        """
        # Color schemes for different alert types
        colors = {
            "info": {"bg": "#e3f2fd", "border": "#2196f3", "text": "#1565c0"},
            "warning": {"bg": "#fff3e0", "border": "#ff9800", "text": "#e65100"},
            "error": {"bg": "#ffebee", "border": "#f44336", "text": "#c62828"},
            "critical": {"bg": "#fce4ec", "border": "#e91e63", "text": "#880e4f"}
        }
        
        color = colors.get(alert_type, colors["info"])
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: {color['bg']}; border-left: 4px solid {color['border']}; padding: 15px; margin-bottom: 20px;">
            <h2 style="color: {color['text']}; margin: 0;">{title}</h2>
        </div>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
            <p style="margin: 0; white-space: pre-wrap;">{message}</p>
        </div>
        
        {self._build_metadata_section(metadata)}
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
            <p>FlurPilot Automated Alert System<br>
            Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _build_metadata_section(self, metadata: Dict[str, Any]) -> str:
        """Build metadata section for email."""
        if not metadata:
            return ""
        
        html = '<div style="margin-top: 20px; padding: 15px; background-color: #fafafa; border-radius: 5px;">'
        html += '<h3 style="margin-top: 0; color: #555;">Additional Information</h3>'
        html += '<table style="width: 100%; border-collapse: collapse;">'
        
        for key, value in metadata.items():
            html += f"""
            <tr>
                <td style="padding: 5px; border-bottom: 1px solid #eee; font-weight: bold; width: 30%;">{key}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">{value}</td>
            </tr>
            """
        
        html += '</table></div>'
        return html


# Singleton instance
_email_service = None

def get_email_service() -> EmailService:
    """Get or create singleton email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


# Convenience functions
async def send_alert(to: str, subject: str, message: str, **kwargs):
    """Send alert using singleton service."""
    service = get_email_service()
    return await service.send_alert(to, subject, message, **kwargs)

async def send_error_alert(to: str, error_message: str, **kwargs):
    """Send error alert using singleton service."""
    service = get_email_service()
    return await service.send_error_alert(to, error_message, **kwargs)


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test():
        service = EmailService()
        
        # Test without API key (logs only)
        print("Testing email service (dry run)...")
        
        await service.send_alert(
            to="admin@flurpilot.de",
            subject="Test Alert",
            message="This is a test alert message.",
            alert_type="info",
            metadata={"test": "value", "timestamp": "2024-01-01"}
        )
        
        print("\nTest complete!")
    
    asyncio.run(test())
