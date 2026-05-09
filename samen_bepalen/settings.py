from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "votes", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    ordering = ("-created_at",)