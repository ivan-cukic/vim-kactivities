"
" Copyright (c) 2012, 2013, 2014, 2015 Ivan Cukic <ivan.cukic(at)kde.org>
"
" This library is free software; you can redistribute it and/or
" modify it under the terms of the GNU Library General Public
" License version 2 as published by the Free Software Foundation.
"
" This library is distributed in the hope that it will be useful,
" but WITHOUT ANY WARRANTY; without even the implied warranty of
" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
" Library General Public License for more details.
"
" You should have received a copy of the GNU Library General Public License
" along with this library; see the file COPYING.LIB.  If not, write to
" the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
" Boston, MA 02110-1301, USA.
"

if exists("loaded_KDE_ACTIVITIES")
    finish
endif

if (v:progname == "ex")
   finish
endif

let loaded_KDE_ACTIVITIES = 1

python import sys
python import vim
python sys.path.insert(0, vim.eval('expand("<sfile>:h")'))

pyfile <sfile>:h/main.py

" autocmd BufAdd      * :python kde_activities_Opened()
" autocmd BufRead     * :python kde_activities_Opened()
" autocmd BufFilePost * :python kde_activities_Opened()
"
" autocmd BufDelete   * :python kde_activities_Closed()
" autocmd BufFilePre  * :python kde_activities_Closed()

autocmd BufLeave    * :python kde_activities_FocussedOut()
autocmd BufEnter    * :python kde_activities_FocussedIn()

command LinkToActivity              :python kde_activities_Link()<CR>
command UnlinkFromActivity          :python kde_activities_Unlink()<CR>
command LinkDirectoryToActivity     :python kde_activities_LinkDirectory()<CR>
command UnlinkDirectoryFromActivity :python kde_activities_UnlinkDirectory()<CR>

menu Plugin.Activities.Link\ current\ file :LinkToActivity<CR>
menu Plugin.Activities.Link\ containing\ directory     :LinkDirectoryToActivity<CR>
menu Plugin.Activities.Unlink\ current\ file :UnlinkFromActivity<CR>
menu Plugin.Activities.Unlink\ containing\ directory     :UnlinkDirectoryFromActivity<CR>
