'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 04/12/2025
Ending //

'''
# Installing the necessary libraries

from sqladmin import ModelView
from src.db.models import Recipient


class RecipientAdmin(ModelView, model=Recipient):
    column_list = [Recipient.id, Recipient.email, Recipient.name]
