from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ContactList, Subscriber, EmailTemplate, Campaign
from .forms import ContactListForm, SubscriberForm, EmailTemplateForm, CampaignForm


# --- Authentication Views ---

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    # Located in templates/campaigns/register.html
    return render(request, 'campaigns/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    # Located in templates/campaigns/login.html
    return render(request, 'campaigns/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# --- Dashboard View ---

@login_required
def dashboard(request):
    total_lists = ContactList.objects.filter(user=request.user).count()
    total_subscribers = Subscriber.objects.filter(contact_list__user=request.user).count()
    context = {
        'total_lists': total_lists,
        'total_subscribers': total_subscribers,
    }
    # Located in templates/campaigns/dashboard.html
    return render(request, 'campaigns/dashboard.html', context)


# --- Contact List Views ---

@login_required
def contact_lists(request):
    if request.method == 'POST':
        form = ContactListForm(request.POST)
        if form.is_valid():
            contact_list = form.save(commit=False)
            contact_list.user = request.user
            contact_list.save()
            return redirect('contact_lists')
    else:
        form = ContactListForm()

    lists = ContactList.objects.filter(user=request.user)
    # Located in templates/campaigns/contact_lists.html
    return render(request, 'campaigns/contact_lists.html', {'lists': lists, 'form': form})


@login_required
def contact_list_detail(request, pk):
    contact_list = get_object_or_404(ContactList, pk=pk, user=request.user)
    subscribers = contact_list.subscribers.all()
    # Located in templates/campaigns/contact_list_detail.html
    return render(request, 'campaigns/contact_list_detail.html', {
        'contact_list': contact_list,
        'subscribers': subscribers
    })


@login_required
def contact_list_delete(request, pk):
    contact_list = get_object_or_404(ContactList, pk=pk, user=request.user)
    if request.method == 'POST':
        contact_list.delete()
        return redirect('contact_lists')
    # Located in templates/campaigns/subscriber_confirm_delete.html
    return render(request, 'campaigns/subscriber_confirm_delete.html', {'object': contact_list, 'type': 'List'})


# --- Subscriber Views ---

@login_required
def subscriber_create(request, list_id):
    contact_list = get_object_or_404(ContactList, pk=list_id, user=request.user)
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.contact_list = contact_list
            subscriber.save()
            return redirect('contact_list_detail', pk=contact_list.pk)
    else:
        form = SubscriberForm()
    # Located in templates/campaigns/subscriber_form.html
    return render(request, 'campaigns/subscriber_form.html', {'form': form, 'contact_list': contact_list})


@login_required
def subscriber_update(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk, contact_list__user=request.user)
    if request.method == 'POST':
        form = SubscriberForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            return redirect('contact_list_detail', pk=subscriber.contact_list.pk)
    else:
        form = SubscriberForm(instance=subscriber)
    # Located in templates/campaigns/subscriber_form.html
    return render(request, 'campaigns/subscriber_form.html', {'form': form, 'contact_list': subscriber.contact_list})


@login_required
def subscriber_delete(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk, contact_list__user=request.user)
    list_pk = subscriber.contact_list.pk;
    if request.method == 'POST':
        subscriber.delete()
        return redirect('contact_list_detail', pk=list_pk)
    # Located in templates/campaigns/subscriber_confirm_delete.html
    return render(request, 'campaigns/subscriber_confirm_delete.html', {'object': subscriber, 'type': 'Subscriber'})


# --- Email Templates (V2) ---

@login_required
def template_list(request):
    templates = EmailTemplate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'campaigns/templates.html', {'templates': templates})


@login_required
def template_create(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.user = request.user
            template.save()
            return redirect('template_list')
    else:
        form = EmailTemplateForm()
    return render(request, 'campaigns/template_form.html', {'form': form, 'title': 'Create Template'})


@login_required
def template_update(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'campaigns/template_form.html', {'form': form, 'title': 'Edit Template'})


@login_required
def template_delete(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk, user=request.user)
    if request.method == 'POST':
        template.delete()
        return redirect('template_list')
    return render(request, 'campaigns/subscriber_confirm_delete.html', {'object': template, 'type': 'Template'})


# --- Campaigns (V2) ---

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'campaigns/campaigns.html', {'campaigns': campaigns})


@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, user=request.user)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(user=request.user)
    return render(request, 'campaigns/campaign_form.html', {'form': form, 'title': 'Create Campaign'})


@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    return render(request, 'campaigns/campaign_detail.html', {'campaign': campaign})


@login_required
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm(instance=campaign, user=request.user)
    return render(request, 'campaigns/campaign_form.html', {'form': form, 'title': 'Edit Campaign'})


@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST':
        campaign.delete()
        return redirect('campaign_list')
    return render(request, 'campaigns/subscriber_confirm_delete.html', {'object': campaign, 'type': 'Campaign'})


@login_required
def campaign_toggle_status(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if campaign.status == 'DRAFT':
        campaign.status = 'READY'
    elif campaign.status == 'READY':
        campaign.status = 'DRAFT'
    campaign.save()
    return redirect('campaign_detail', pk=campaign.pk)