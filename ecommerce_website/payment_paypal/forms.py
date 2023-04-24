from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html


class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self, *args, **kwargs):

        if not args and not kwargs:
            form_open = u'''<form action="%s" method="post" class='rounded-1 paypal-form'>''' % (
                self.get_login_url())
            form_close = u'</form>'
            image_elm = u'''<input type="image" src="" class="paypal-image paypal-image">'''
            submit_elm = u'''<button type="submit" class="paypal-submit-btn"></button>'''
            return format_html(form_open+self.as_p()+image_elm+submit_elm+form_close)
        else:
            return super().render(*args, **kwargs)
