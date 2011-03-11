##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
from zope.size.interfaces import ISized
"""File views.

$Id$
"""
from zope.app.file.browser import file


class FileView(file.FileView):

    def show(self):
        res = super(FileView, self).show()
        contentDisposition = 'inline'
        self.request.response.setHeader(
            'Content-Disposition','%s; filename="%s"'%(
                contentDisposition, self.context.__name__.encode('utf-8')))
        return res
    
    def size(self):
        return ISized(self.context).sizeForDisplay()

    