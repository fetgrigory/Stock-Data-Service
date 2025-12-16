'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 04/12/2025
Ending //

'''
# Installing the necessary libraries

from sqladmin import ModelView
from src.db.models import Recipient, User, SmtpSetting


class RecipientAdmin(ModelView, model=Recipient):
    column_list = [Recipient.id, Recipient.email, Recipient.name]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]


class SmtpSettingAdmin(ModelView, model=SmtpSetting):
    column_list = [SmtpSetting.id,  SmtpSetting.server, SmtpSetting.port, SmtpSetting.username, SmtpSetting.password, SmtpSetting.sender]
