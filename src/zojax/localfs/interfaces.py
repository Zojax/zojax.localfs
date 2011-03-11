##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from zope.app.file.interfaces import IFile
"""

$Id$
"""
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zojax.content.type.interfaces import IItem, IContent, IContentType

_ = MessageFactory('zojax.localfs')


class ILocalFsFile(IItem, IFile):
    pass


class ILocalFsFolder(IItem):
    """ base """

    path = schema.TextLine(
        title = _(u'Local Fs Path'),
        description = _(u'Local Fs Path.'),
        required = True,)
    
    
class ILocalFsFolderContent(ILocalFsFolder):
    """ content """