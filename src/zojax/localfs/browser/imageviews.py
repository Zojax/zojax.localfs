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

class ImageDownload(object):

    def show(self):
        try:
            return self.context.data.showFly(
                self.request,
                filename=self.context.__name__,
                contentDisposition='inline')
        except:
            return u''


class ImagePreview(object):

    def show(self):
        try:
            return self.context.data.showPreviewFly(
                self.request,
                filename=self.context.__name__,
                contentDisposition='inline')
        except:
            return u''