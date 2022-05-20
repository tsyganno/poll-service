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


class VariantAdmin(admin.ModelAdmin):
    list_display = ('name_variant',)
    list_display_links = ('name_variant',)
    search_fields = ('name_variant',)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Variant, VariantAdmin)
