from django.utils import timezone
from django.contrib import admin

from app_poll.models import Vote, Question, Variant


class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'published_off', 'content')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type_question', 'correct_answer')
    list_display_links = ('text', 'correct_answer')
    search_fields = ('text', 'correct_answer',)

    def get_readonly_fields(self, request, obj=None):
        time_now = timezone.now()
        if obj and obj.vote.published < time_now and obj.vote.published_off > time_now:
            return ['vote', 'type_question', 'correct_answer', 'text']
        return self.readonly_fields


class VariantAdmin(admin.ModelAdmin):
    list_display = ('name_variant',)
    list_display_links = ('name_variant',)
    search_fields = ('name_variant',)

    def get_readonly_fields(self, request, obj=None):
        time_now = timezone.now()
        if obj and obj.question.vote.published < time_now and obj.question.vote.published_off > time_now:
            return ['question', 'name_variant']
        return self.readonly_fields


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Variant, VariantAdmin)
