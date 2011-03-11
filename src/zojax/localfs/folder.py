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
"""

$Id$
"""
import os.path

from zope import interface, component
from zope.app.container.ordered import OrderedContainer
from zope.app.container.interfaces import IContainer, IReadContainer
from zope.schema.fieldproperty import FieldProperty

from zojax.content.type.item import PersistentItem
from zojax.content.type.interfaces import IContentContainer
from zojax.richtext.field import RichTextProperty

from interfaces import ILocalFsFolder, ILocalFsFolderContent


class LocalFsFolderBase(object):
    interface.implements(ILocalFsFolder, IContentContainer, IReadContainer)
    
    path = FieldProperty(ILocalFsFolder['path'])
    
    def __init__(self, path=None, name=None, **kw):
        self.path = path
        self.__name__ = name
        super(LocalFsFolderBase, self).__init__(**kw)
    
    def keys(self):
        """Return the keys of the mapping object.
        """
        return os.listdir(self.path)

    def __iter__(self):
        """Return an iterator for the keys of the mapping object.
        """
        return iter(self.keys())

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
        filename = os.path.join(self.path, name)
        if os.path.isdir(filename):
            factory = IDirectoryFactory(self)
            newdir = factory(name)
            return newdir
        
        # Find the extension
        nm, ext = os.path.splitext(name)
            
        factory = component.queryAdapter(self, IFileFactory, ext)
        if factory is None:
            factory = IFileFactory(self)

        newfile = factory(name, '', open(filename))
        #notify(ObjectCreatedEvent(newfile))
        return newfile


class LocalFsFolder(LocalFsFolderBase, PersistentItem):
    interface.implements(ILocalFsFolderContent)
    
    
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

        res = LocalFsFolder(path=os.path.join(self.context.path, name), name=name)
        res.__parent__ = self.context