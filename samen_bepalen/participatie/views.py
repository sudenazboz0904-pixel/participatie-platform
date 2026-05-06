from django.shortcuts import render, get_object_or_404, redirect
from .models import Proposal
from .forms import ProposalForm


def index(request):
    """
    Homepage: toont alle ingediende voorstellen, gesorteerd op meeste stemmen.
    """
    proposals = Proposal.objects.all().order_by('-votes')
    return render(request, 'participatie/index.html', {'proposals': proposals})


def vote(request, proposal_slug):
    """
    Stemmen op een voorstel. Verhoogt het aantal stemmen met 1 en stuurt terug naar homepage.
    Werkt alleen via een POST-verzoek (zodat mensen niet via de URL kunnen stemmen).
    """
    if request.method == 'POST':
        proposal = get_object_or_404(Proposal, slug=proposal_slug)
        proposal.votes += 1
        proposal.save()
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
            form.save()
            return redirect('index')
    else:
        form = ProposalForm()

    return render(request, 'participatie/submit.html', {'form': form})
