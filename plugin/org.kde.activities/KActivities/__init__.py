#
# Copyright (c) 2012, 2013, 2014, 2015 Ivan Cukic <ivan.cukic(at)kde.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.
#

import dbus
import vim

class Event:
    Accessed = 0    # resource was accessed, but we don't know for how long it will be open/used

    Opened = 1      # resource was opened
    Modified = 2    # previously opened resource was modified
    Closed = 3      # previously opened resource was closed

    FocussedIn = 4  # resource get the keyboard focus
    FocussedOut = 5 # resource lost the focus

RegisterResourceEvent      = lambda app, winid, uri, event: ()
RegisterResourceMimeType   = lambda uri, mime: ()
RegisterResourceTitle      = lambda uri, title: ()

try:
    ActivityManager_Events  = dbus.SessionBus().get_object('org.kde.ActivityManager', '/ActivityManager/Resources')
    ActivityManager_Linking = dbus.SessionBus().get_object('org.kde.ActivityManager', '/ActivityManager/Resources/Linking')

    RegisterResourceEvent      = ActivityManager_Events.get_dbus_method('RegisterResourceEvent',       'org.kde.ActivityManager.Resources')
    RegisterResourceMimeType   = ActivityManager_Events.get_dbus_method('RegisterResourceMimeType',    'org.kde.ActivityManager.Resources')
    RegisterResourceTitle      = ActivityManager_Events.get_dbus_method('RegisterResourceTitle',       'org.kde.ActivityManager.Resources')
except:
    vim.command('echom "KDE Activity manager is not running, disabling the integration plugin."')

# Crappy Python D-Bus binding does not support overloaded methods

def LinkResourceToActivity(resource):
    unique = dbus.SessionBus().call_blocking(
            'org.kde.ActivityManager',                   # bus name
            '/ActivityManager/Resources/Linking',        # object path
            'org.kde.ActivityManager.ResourcesLinking',  # dbus iface
            'LinkResourceToActivity',                    # method
            'sss',                                       # signature
            ("", resource, ":current")                   # args
            )

def UnlinkResourceFromActivity(resource):
    unique = dbus.SessionBus().call_blocking(
            'org.kde.ActivityManager',                   # bus name
            '/ActivityManager/Resources/Linking',        # object path
            'org.kde.ActivityManager.ResourcesLinking',  # dbus iface
            'UnlinkResourceFromActivity',                # method
            'sss',                                       # signature
            ("", resource, ":current")                   # args
            )

class ResourceInstance:
    _wid         = None
    _application = None
    _resourceUri = None
    _mimetype    = None
    _title       = None

    def __init__(self, wid, application, resourceUri = None, mimetype = None, title = None):
        self._wid         = wid
        self._application = application
        self._resourceUri = resourceUri
        self._mimetype    = mimetype
        self._title       = title

        if (resourceUri != None):
            RegisterResourceEvent(application, wid, resourceUri, Event.Opened)

        if (title != None):
            self.setTitle(title)

        if (mimetype != None):
            self.setMimetype(mimetype)


    def __del__(self):
        RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.Closed)

    def notifyModified(self):
        RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.Modified)

    def notifyFocusedIn(self):
        RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.FocussedIn)

    def notifyFocusedOut(self):
        RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.FocussedOut)

    def setUri(self, newUri):
        if self._resourceUri is not None:
            RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.Closed)

        self._resourceUri = newUri

        if self._resourceUri is not None:
            RegisterResourceEvent(self._application, self._wid, self._resourceUri, Event.Opened)

    def setMimetype(self, mimeType):
        RegisterResourceMimeType(self._resourceUri, self._mimetype)

    def setTitle(self, title):
        RegisterResourceTitle(self._resourceUri, self._title)

    def uri(self):
        return self._resourceUri

    def mimetype(self):
        return self._mimetype

    def title(self):
        return self._title

    def winId(self):
        return seld._wid

