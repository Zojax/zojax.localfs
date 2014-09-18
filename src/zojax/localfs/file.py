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
"""

$Id$
"""
import os.path

from zope import interface, component
from zope.app.file.image import getImageInfo
from zope.contenttype import guess_content_type
from zope.filerepresentation.interfaces import IFileFactory

from zojax.content.type.item import Item
from zojax.filefield.data import DownloadResultFly, File as OrigFile

from interfaces import ILocalFsFolder, ILocalFsFile



class FileMixin(object):

    def show(self, *kv, **kw):
        res = self._show(*kv, **kw)
        if res != '':
            return DownloadResultFly(self)
        return res


class File(FileMixin, OrigFile):
    pass


class LocalFsFile(Item):

    interface.implements(ILocalFsFile)

    data = None

    def __init__(self, name, abspath, content_type, **kw):
        self.__name__ = name
        self.abspath = abspath
        self.contentType = content_type
        super(LocalFsFile, self).__init__(**kw)

    @property
    def data(self):
        try:
            f = File()
            f.data = open(self.abspath).read()
            f.mimeType = self.contentType
            f.filename = self.__name__
            f.size = self.size
            #f.modified =
            return f
        except (IOError, OSError), e:
            return ''

    @property
    def size(self):
        try:
            return os.path.getsize(self.abspath)
        except (IOError, OSError), e:
            return 0

    @property
    def title(self):
        return self.__name__

    @property
    def disposition(self):
        # return self.data.previewIsAvailable and 'inline' or 'attachment'
        # canDownload = contentDisposition='attachment'
        # canPreview = contentDisposition='inline'
        return 'attachment'

    @property
    def canDownload(self):
        return True

    @property
    def canPreview(self):
        return False

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
        res = LocalFsFile(
            name, os.path.join(self.context.abspath, name), content_type)
        res.__parent__ = self.context
        return res
