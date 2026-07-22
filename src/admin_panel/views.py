from sqladmin import ModelView
from src.recipients.models import Recipient
from src.auth.models import User
from src.email.models import SmtpSetting


class RecipientAdmin(ModelView, model=Recipient):
    column_list = [Recipient.id, Recipient.email, Recipient.name]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]


class SmtpSettingAdmin(ModelView, model=SmtpSetting):
    column_list = [SmtpSetting.id,  SmtpSetting.server, SmtpSetting.port, SmtpSetting.username, SmtpSetting.password, SmtpSetting.sender]
