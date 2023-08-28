from django.contrib import messages
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth import get_permission_codename
from django.utils.translation import gettext_lazy as _
# Register your models here.


class AdminAccessFilter(admin.SimpleListFilter):
    title = _('IS STAFF')
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        return [
            ('staff', _('Staff Member')),
            ('not_staff', _('Non Staff Member'))
        ]

    def queryset(self, request, queryset):
        """
        :param request:
        :param queryset:
        :return: a filtered queryset provided in query string
        """

        if self.value() == 'staff':
            return CustomUser.objects.filter(is_staff=True)
        elif self.value() == 'not_staff':
            return CustomUser.objects.filter(is_staff=False)


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_filter = [AdminAccessFilter, 'is_staff', 'is_active']

    actions = ['call_action']
    date_hierarchy = "birth_date"
    exclude = ['gender']
    empty_value_display = "unknown"
    ordering = ["birth_date"]
    search_fields = ["first_name", "birth_date"]

    def get_search_results(self, request, queryset, search_term):
        queryset, duplicates = super().get_search_results(
            request=request,
            queryset=queryset,
            search_term=search_term
        )
        queryset |= CustomUser.objects.filter(first_name=search_term)
        return queryset, duplicates

    @admin.display(description="Name")
    def upper_case_name(obj):
        return f"{obj.first_name} {obj.last_name}".upper()

    @admin.display(description='Birthday')
    def born_in_2023(self):
        return str(self.birth_date).split('-')[0] == '2023'

    list_display = [upper_case_name, born_in_2023]
    list_display_links = [upper_case_name]

    @admin.action(description="Another Action")
    def another_action(self, request, queryset):
        print("Another action is called")

    @admin.action(description="Call An Action")
    def call_action(self, request, queryset):
        queryset.filter(gender='m')
        print('action called')
        self.message_user(
            request,
            "Action has been called.",
            messages.SUCCESS,
        )

    def has_calling_permission(self, request):
        """Does the user have the calling permission?"""
        opts = self.opts
        codename = get_permission_codename("calling", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))
    pass


admin.site.add_action(UserAdmin.another_action, "Another")
