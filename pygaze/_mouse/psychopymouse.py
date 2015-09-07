# -*- coding: utf-8 -*-
#
# This file is part of PyGaze - the open-source toolbox for eye tracking
#
#	PyGaze is a Python module for easily creating gaze contingent experiments
#	or other software (as well as non-gaze contingent experiments/software)
#	Copyright (C) 2012-2013  Edwin S. Dalmaijer
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>

from pygaze.libtime import clock
from pygaze import settings
from pygaze._mouse.basemouse import BaseMouse
# we try importing the copy_docstr function, but as we do not really need it
# for a proper functioning of the code, we simply ignore it when it fails to
# be imported correctly
try:
	from pygaze._misc.misc import copy_docstr
except:
	pass
	
import pygaze
from pygaze._misc.misc import pos2psychopos, psychopos2pos

import psychopy.event

class PsychoPyMouse(BaseMouse):

	# See _mouse.basemouse.BaseMouse

	def __init__(self, mousebuttonlist=settings.MOUSEBUTTONLIST,
		timeout=settings.MOUSETIMEOUT, visible=False):

		# See _mouse.basemouse.BaseMouse

		# try to copy docstring (but ignore it if it fails, as we do
		# not need it for actual functioning of the code)
		try:
			copy_docstr(BaseMouse, PsychoPyMouse)
		except:
			# we're not even going to show a warning, since the copied
			# docstring is useful for code editors; these load the docs
			# in a non-verbose manner, so warning messages would be lost
			pass

		# create mouse object
		self.mouse = psychopy.event.Mouse(visible=False,win=psychopy.visual.openWindows[SCREENNR])
		
		# set mouse characteristics
		self.set_mousebuttonlist(mousebuttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible=visible)


	def set_mousebuttonlist(self, mousebuttonlist=None):

		# See _mouse.basemouse.BaseMouse
		
		if mousebuttonlist == None or mousebuttonlist == []:
			self.mbuttonlist = None
		else:
			self.mbuttonlist = []
			for mbutton in mousebuttonlist:
				self.mbuttonlist.append(mbutton)


	def set_timeout(self, timeout=None):

		# See _mouse.basemouse.BaseMouse

		self.timeout = timeout


	def set_visible(self, visible=True):

		# See _mouse.basemouse.BaseMouse

		self.visible = visible
		self.mouse.setVisible(self.visible)


	def set_pos(self, pos=(0,0)):

		# See _mouse.basemouse.BaseMouse

		self.mouse.setPos(newPos=pos2psychopos(pos))


	def get_pos(self):

		# See _mouse.basemouse.BaseMouse

		return psychopos2pos(self.mouse.getPos())


	def get_clicked(self, mousebuttonlist='default', timeout='default'):

		# See _mouse.basemouse.BaseMouse

		# set buttonlist and timeout
		if mousebuttonlist == 'default':
			mousebuttonlist = self.mbuttonlist
		if timeout == 'default':
			timeout = self.timeout
		# starttime
		starttime = clock.get_time()
		time = clock.get_time()
		# wait for mouse clicks
		while timeout == None or time - starttime <= timeout:
			time = clock.get_time()
			pressed = self.mouse.getPressed()
			if sum(pressed) > 0:
				for b in range(0,len(pressed)):
					if pressed[b] == 1:
						if mousebuttonlist == None or b+1 in mousebuttonlist:
							return b+1, self.get_pos(), time
		# in case of timeout
		return None, None, time


	def get_pressed(self):

		# See _mouse.basemouse.BaseMouse

		return self.mouse.getPressed()
