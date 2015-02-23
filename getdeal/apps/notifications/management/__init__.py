from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import get_models, signals
import models as notification


def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("new_like", _("Mention j'aime"), _(" a aimé le deal "), default=2)

signals.post_syncdb.connect(create_notice_types, dispatch_uid=notification)
