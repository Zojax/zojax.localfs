##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""

from zope import interface, component

from zojax.content.actions.action import Action
from zojax.content.actions.contentactions import EditContentAction, \
    ContentAction

from ..interfaces import ILocalFsFile, ILocalFsFolder



class EditLocalFsFileContentAction(EditContentAction):
    interface.implements(ILocalFsFile, interface.Interface)

    def isAvailable(self):
        return False


class EditLocalFsFileContentContextAction(Action):
    component.adapts(ILocalFsFile, interface.Interface)

    def isAvailable(self):
        return False


class EditLocalFsFolderContentContextAction(Action):
    component.adapts(ILocalFsFolder, interface.Interface)

    def isAvailable(self):
        return False


class LocalFsFileExternalEditAction(ContentAction):
    component.adapts(ILocalFsFile, interface.Interface)

    def isAvailable(self):
        return False


class LocalFsFileUnlockAction(ContentAction):
    component.adapts(ILocalFsFile, interface.Interface)

    def isAvailable(self):
        return False
