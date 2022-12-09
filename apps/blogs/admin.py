import datetime

from apps.blogs.models import Blog, Author, Comment, Tag
from django.utils import timezone
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

admin.site.register(Blog)
admin.site.register(Tag)



class YesterdayListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Is yesterday ?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_yesterday'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset
        yesterday = timezone.now() - datetime.timedelta(days=1)
        if self.value() == 'Yes':
            return queryset.filter(datetime__gte=yesterday)
        else:
            return queryset.filter(datetime__lte=yesterday)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'birth_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'datetime', 'difference_time')
    list_filter = ('datetime', 'author', YesterdayListFilter)

    # TODO: Create custom user extend AbstractUser. Add method __str__    great
    # TODO: Add order/sort by datetime field                             great
    # TODO: Add filter by datetime field                                 great
    # TODO: Add custom filter when difference_time > 24h return True else return false great :)

    @admin.display(description='DifferenceTime')
    def difference_time(self, obj):
        return f"{int((timezone.now() - obj.datetime).seconds / 60)} minutes"

    def func(self, obj, queryset):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        if self.value() > yesterday:
            return queryset.filter(datetime__gte=yesterday)
        else:
            return queryset.filter(datetime__lte=yesterday)

    def get_ordering(self, request):
        return ["-datetime"]

    # def queryset(self, request, queryset):
    #     if self.value() == '24h':
    #         return queryset.filter(True
    #                                )
    #     else:
    #         return queryset.filter(False
    #                                )

# class Difference(admin.ModelAdmin):
#     list_display = ('name', 'difference_time')
