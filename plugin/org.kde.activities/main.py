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

import os
import dbus
import XlibGetWindowId
import KActivities

#######################################################################
# Function returns the window id for the current window               #
#######################################################################

def _getWindowId():
    try:
        wid = 0
        var = "v:windowid"
        varExists = vim.eval('exists("' + var + '")')

        if not varExists == "0":
            wid = vim.eval(var)
            if not wid == "0":
                return wid

    except:
        pass

    # Getting the window id for the current process - GVIM
    for wid in XlibGetWindowId.getWindowIdsForCurrentProcess():
        return wid

    # Falling back to testing the environment vatiable
    # if we are in a terminal - normal VIM
    try:
        widenv = os.getenv("WINDOWID")
        if widenv:
            wid = int(widenv)
            return wid

    # Otherwise, we must go without the window id
    except ValueError:
        pass

    return 0


#######################################################################
# Returns the url for the current file                                #
#######################################################################

def _urlForCurrentDocument(suf = ":p"):
    try:
        document = vim.eval('expand("<afile>' + suf + '")')

        if document is None or document == "":
            document = vim.eval('expand("%' + suf + '")')

        if not document.startswith("/"):
            document = "/" + document

        if os.path.exists(document):
            return document

        return None

    except:
        return None



#######################################################################
# Activities related methods                                          #
#######################################################################

kde_activities_resourceinstance = None


def kde_activities_ResourceInstance():
    global kde_activities_resourceinstance

    if kde_activities_resourceinstance is None:
        kde_activities_resourceinstance = KActivities.ResourceInstance(_getWindowId(), "gvim")

    return kde_activities_resourceinstance


def kde_activities_FocussedIn():
    document = _urlForCurrentDocument()

    if document is None:
        return;

    kde_activities_ResourceInstance().setUri(document)


def kde_activities_FocussedOut():
    pass


def kde_activities_Link():
    document = _urlForCurrentDocument()

    if document is not None:
        KActivities.LinkResourceToActivity(document)


def kde_activities_Unlink():
    document = _urlForCurrentDocument()

    if document is not None:
        KActivities.UnlinkResourceFromActivity(document)


def kde_activities_LinkDirectory():
    document = _urlForCurrentDocument(":p:h")

    if document is not None:
        KActivities.LinkResourceToActivity(document)


def kde_activities_UnlinkDirectory():
    document = _urlForCurrentDocument(":p:h")

    if document is not None:
        KActivities.UnlinkResourceFromActivity(document)


