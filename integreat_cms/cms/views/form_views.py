"""
This module contains form views for our models that don't need custom handling.
"""
from django.contrib import messages
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
)
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.edit import ModelFormMixin, BaseCreateView, BaseUpdateView

from .media import MediaContextMixin
from .mixins import (
    ModelTemplateResponseMixin,
    ModelConfirmationContextMixin,
)


# pylint: disable=too-many-ancestors
class CustomModelFormMixin(
    PermissionRequiredMixin,
    ModelTemplateResponseMixin,
    ModelFormMixin,
    ModelConfirmationContextMixin,
    MediaContextMixin,
):
    """
    This mixin handles error messages in form views of subclasses of
    :class:`~integreat_cms.cms.forms.custom_model_form.CustomModelForm`
    """

    #: The suffix to append to the auto-generated candidate template name.
    template_name_suffix = "_form"

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.

        :return: The permissions that are required for views inheriting from this Mixin
        :rtype: ~collections.abc.Iterable
        """
        # If the form is submitted via POST, require the change permission
        if self.request.method == "POST":
            return (f"cms.change_{self.model._meta.model_name}",)
        # If the form is just retrieved, require the view permission
        return (f"cms.view_{self.model._meta.model_name}",)

    @property
    def model(self):
        """
        Return the model class of this form mixin

        :return: The corresponding Django model
        :rtype: ~django.db.models.Model
        """
        return self.form_class._meta.model

    def get_context_data(self, **kwargs):
        r"""
        Returns a dictionary representing the template context
        (see :meth:`~django.views.generic.base.ContextMixin.get_context_data`).

        :param \**kwargs: The given keyword arguments
        :type \**kwargs: dict

        :return: The template context
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context.update({"current_menu_item": f"{self.model._meta.model_name}s"})
        return context

    def get_success_url(self):
        """
        Determine the URL to redirect to when the form is successfully validated

        :return: The url to redirect on success
        :rtype: str
        """
        return reverse(
            f"edit_{self.object._meta.model_name}",
            kwargs={"slug": self.object.slug},
        )

    def form_valid(self, form):
        """
        Saves the form instance, sets the current object for the view, and redirects to :meth:`get_success_url`.

        :param form: The valid form instance
        :type form: ~django.forms.ModelForm

        :return: A redirection to the success url
        :rtype: ~django.http.HttpResponseRedirect
        """
        if not form.has_changed():
            # Add "no changes" messages
            messages.info(self.request, _("No changes made"))
        elif self.object:
            messages.success(
                self.request,
                _('{} "{}" was successfully saved').format(
                    self.object._meta.verbose_name, self.object
                ),
            )
        else:
            messages.success(
                self.request,
                _('{} "{}" was successfully created').format(
                    form.instance._meta.verbose_name, form.instance
                ),
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Renders a response, providing the invalid form as context.

        :param form: The invalid form instance
        :type form: ~django.forms.ModelForm

        :return: The rendered invalid form
        :rtype: ~django.http.HttpResponse
        """
        form.add_error_messages(self.request)
        return super().form_invalid(form)


class CustomCreateView(CustomModelFormMixin, BaseCreateView):
    """
    A view that displays a form for creating a region object, redisplaying the form with validation errors (if
    there are any) and saving the object.
    """


class CustomUpdateView(CustomModelFormMixin, BaseUpdateView):
    """
    A view that displays a form for editing an existing region object, redisplaying the form with validation errors
    (if there are any) and saving changes to the object. This uses a form automatically generated from the object's
    model class (unless a form class is manually specified).
    """