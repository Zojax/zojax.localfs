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
from zope.event import notify
from zope.location.location import LocationProxy
from zope.cachedescriptors.property import Lazy
from zojax.theme.friendly.contenttypecategory.interfaces import IContentTypeCategory
from zojax.contenttype.image.image import Image
from zojax.localfs.interfaces import ILocalFsFolderDynamic
"""

$Id$
"""
import os.path

from zope import interface, component
from zope.app.container.ordered import OrderedContainer
from zope.app.container.interfaces import IContainer, IReadContainer
from zope.schema.fieldproperty import FieldProperty

from zojax.content.type.item import PersistentItem, Item
from zojax.content.type.interfaces import IContentContainer,\
    IUnremoveableContent, IContentType
from zojax.richtext.field import RichTextProperty

from interfaces import ILocalFsFolder, ILocalFsFolderContent, ILocalFsConfiglet

class LocalFsFolderBase(Item):
    interface.implements(ILocalFsFolder, IContentContainer, IReadContainer)
    
    abspath = None    
    
    def __init__(self, abspath=None, name=None, **kw):
        if abspath:
            self.abspath = abspath
        if name:
            self.__name__ = name
        super(LocalFsFolderBase, self).__init__(**kw)
    
    def keys(self):
        """Return the keys of the mapping object.
        """
        try:
            return os.listdir(self.abspath)
        except (OSError, IOError), e:
            return []

    def __iter__(self):
        """Return an iterator for the keys of the mapping object.
        """
        return iter(self.keys())
    
    def __contains__(self, name):
        return self.keys().__contains__(name)

    def values(self):
        """Return the values of the mapping object.
        """
        return [self[i] for i in self.keys()] 

    def items(self):
        """Return the items of the mapping object.
        """
        return [(i, self[i]) for i in self.keys()] 

    def __len__(self):
        """Return the number of items.
        """
        return len(self.keys())
    
    def __getitem__(self, name):
        if name not in self.keys():
            raise KeyError(name)
        filename = os.path.join(self.abspath, name)
        if os.path.isdir(filename):
            factory = IDirectoryFactory(self)
            newdir = factory(name)
            return newdir
        
        # Find the extension
        nm, ext = os.path.splitext(name)
            
        factory = IFileFactory(self)

        try:
            f = open(filename)
        except (IOError, OSError), e:
            f = ''
        newfile = factory(name, '', f)
        #notify(ObjectCreatedEvent(newfile))
        newfile.__parent__ = self
        newfile.__name__ = name
        return newfile

    def __setitem__(self, name, value):
        raise NotImplementedError()
    
    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
    

class LocalFsFolderDynamic(LocalFsFolderBase):
    
    interface.implements(ILocalFsFolderDynamic)

    @property
    def title(self):
        return self.__name__
    

class LocalFsFolder(LocalFsFolderBase, PersistentItem):
    interface.implements(ILocalFsFolderContent)
    
    path = FieldProperty(ILocalFsFolderContent['path'])
    
    @property
    def abspath(self):
        basePath = component.getUtility(ILocalFsConfiglet, context=self).basePath
        path = self.path
        while path.startswith('/'):
            path = path[1:]
        if basePath:
            return os.path.join(basePath, path)
        return path
    
    
class DirectoryFactory(object):
    """`IContainer` to `IDirectoryFactory` adapter that clones

    This adapter provides a factory that creates a new empty container
    of the same class as it's context.
    """

    component.adapts(ILocalFsFolder)
    interface.implements(IDirectoryFactory)

    def __init__(self, context):
        self.context = context

    def __call__(self, name):
        
        # We remove the security proxy so we can actually call the
        # class and return an unproxied new object.  (We can't use a
        # trusted adapter, because the result must be unproxied.)  By
        # registering this adapter, one effectively gives permission
        # to clone the class.  Don't use this for classes that have
        # exciting side effects as a result of instantiation. :)
        
        res = LocalFsFolderDynamic(abspath=os.path.join(self.context.abspath, name), name=name)
        res.__parent__ = self.context
        return res
