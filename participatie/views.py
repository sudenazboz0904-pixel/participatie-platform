from django.shortcuts import render, get_object_or_404, redirect
from .models import Proposal, LiveUpdate
from .forms import ProposalForm
from .services.theme_classifier import classify_theme


def home(request):
    return render(request, 'participatie/home.html')


def index(request):
    proposals = Proposal.objects.all().order_by('-votes')[:3]
    al_gestemd = request.session.get('gestemd_op', [])
    return render(request, 'participatie/index.html', {
        'voorstellen': proposals,
        'al_gestemd': al_gestemd,
    })


def gbg_live(request):
    """
    Pagina voor GBG Live updates: toont alle gepubliceerde live updates.
    """
    live_updates = LiveUpdate.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'participatie/gbg_live.html', {'live_updates': live_updates})


def vote(request, proposal_slug):
    if request.method == 'POST':
        gestemd_op = request.session.get('gestemd_op', [])
        if proposal_slug not in gestemd_op:
            vote_type = request.POST.get('vote_type')
            proposal = get_object_or_404(Proposal, slug=proposal_slug)
            if vote_type == 'eens':
                proposal.votes_for += 1
            elif vote_type == 'oneens':
                proposal.votes_against += 1
            else:
                return redirect('index')
            proposal.save()
            gestemd_op.append(proposal_slug)
            request.session['gestemd_op'] = gestemd_op
    return redirect('index')


def submit(request):
    """
    Pagina om een nieuw voorstel in te dienen.
    - Bij GET: toon het lege formulier
    - Bij POST: verwerk het formulier en sla het voorstel op
    """
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.theme = classify_theme(proposal.title, proposal.description)
            proposal.save()
            return redirect('index')
    else:
        form = ProposalForm()

    return render(request, 'participatie/submit.html', {'form': form})

