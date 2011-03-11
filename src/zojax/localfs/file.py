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
from zope.filerepresentation.interfaces import IWriteFile, IWriteDirectory,\
    IDirectoryFactory, IFileFactory
from z3c.proxy.container import ContainerLocationProxy
from zope.lifecycleevent import ObjectCreatedEvent
from zope.contenttype import guess_content_type
from zope.app.file.image import getImageInfo
from zope.app.file.interfaces import IFile
from zope.cachedescriptors.property import Lazy
"""

$Id$
"""
import os.path

from zope import interface, component
from zope.app.container.ordered import OrderedContainer
from zope.app.container.interfaces import IContainer, IReadContainer
from zope.schema.fieldproperty import FieldProperty

from zojax.content.type.item import PersistentItem, Item
from zojax.content.type.interfaces import IContentContainer
from zojax.richtext.field import RichTextProperty

from interfaces import ILocalFsFolder, ILocalFsFolderContent, ILocalFsFile


class LocalFsFile(Item):
    
    interface.implements(ILocalFsFile)
    
    data = FieldProperty(IFile['data'])
    
    def __init__(self, name, path, content_type, **kw):
        self.__name__ = name
        self.path = path
        self.contentType = content_type
        super(LocalFsFile, self).__init__(**kw)
    
    @property
    def data(self):
        try:
            return open(self.path)
        except (IOError, OSError), e:
            return ''

    def getSize(self):
        try:
            return os.path.getsize(self.path)
        except (IOError, OSError), e:
            return 0
        

class FileFactory(object):

    component.adapts(ILocalFsFolder)
    interface.implements(IFileFactory)

    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        if not content_type and data:
            content_type, width, height = getImageInfo(data)
        if not content_type:
            content_type, encoding = guess_content_type(name, '', '')
        res = LocalFsFile(name, os.path.join(self.context.path, name), content_type)
        res.__parent__ = self.context
        return res