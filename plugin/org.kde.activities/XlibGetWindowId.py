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

import os, sys, Xlib
from Xlib import X, display, Xatom

# Doing dirty things to stop Xlib from
# writing to stdout
# Xlib.display.Display()
#     Xlib.protocol.request.QueryExtension
old_stdout = sys.stdout
sys.stdout = open("/dev/null", "w")
display    = Xlib.display.Display()
screen     = display.screen()
sys.stdout.close()
sys.stdout = old_stdout

def _processWindow(win, atom, processId, level = 0):
    result = set()

    response = win.get_full_property(atom, Xatom.CARDINAL)

    found = False

    # Testing whether the response was valid
    # and whether we found a proper process id
    if response != None:
        for pid in response.value:
            if pid == processId:
                result.add(win.id)
                found = True

    # If we have found the window, we don't
    # search its children
    if not found:
        for child in win.query_tree().children:
            result |= _processWindow(child, atom, processId, level + 1)

    return result

# Gets the window IDs that belong to the specified process
def getWindowIds(processId):

    root = screen.root
    tree = root.query_tree()
    wins = tree.children
    atom = display.intern_atom("_NET_WM_PID", 1)

    # recursively searches the window tree
    # for the one that has a desired pid
    result = set()

    for win in wins:
        result |= _processWindow(win, atom, processId)

    return result

# Gets the window IDs that belong to the current process
def getWindowIdsForCurrentProcess():
    return getWindowIds(os.getpid())

# winidspec = getWindowIds(5168)
# winidcurr = getWindowIdsForCurrentProcess()
# print winidspec, winidcurr

