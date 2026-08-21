from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign


@shared_task(bind=True)
def send_campaign_emails(self, campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return "Campaign not found"

    # Mark campaign as actively processing
    campaign.status = 'PROCESSING'
    campaign.save(update_fields=['status'])

    subscribers = campaign.contact_list.subscribers.all()
    template = campaign.template

    sent = 0
    failed = 0

    for subscriber in subscribers:
        try:
            # Replace placeholder {{name}} with subscriber name or fallback
            personalized_name = subscriber.name if subscriber.name else 'Subscriber'
            body = template.body.replace('{{name}}', personalized_name)
            subject = template.subject.replace('{{name}}', personalized_name)

            send_mail(
                subject=subject,
                message=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@campaigner.com'),
                recipient_list=[subscriber.email],
                fail_silently=False,
            )
            sent += 1
        except Exception:
            failed += 1

    # Update final campaign statistics and status
    campaign.sent_count = sent
    campaign.failed_count = failed
    campaign.status = 'COMPLETED' if failed == 0 else 'COMPLETED'
    campaign.save(update_fields=['status', 'sent_count', 'failed_count'])

    return f"Campaign #{campaign.id} completed. Sent: {sent}, Failed: {failed}"