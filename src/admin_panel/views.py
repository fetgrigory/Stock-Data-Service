from sqladmin import ModelView

from src.email.models import SmtpSetting
from src.user.models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
    ]


class SmtpSettingAdmin(ModelView, model=SmtpSetting):
    column_list = [
        SmtpSetting.id,
        SmtpSetting.server,
        SmtpSetting.port,
        SmtpSetting.username,
        SmtpSetting.password,
        SmtpSetting.sender,
        SmtpSetting.ssl_port,
        SmtpSetting.timeout,
    ]
