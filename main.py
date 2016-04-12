#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from sandbox import *

u"""
Should call at project directory and use relative derived data path.
Project name is extracted from *.xcodeproj
Target name must match project name

usage:
`simrun setup [identifier] `
`simrun start`
-- develop --
`simrun reload`
"""

class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'TODO description '
        arguments = [
            (['-i', '--identifier'], dict(action='store', help='simulator device identifier'))
            # TODO os type and device type
        ]

    @expose()
    def setup(self, help='指定のidentifier + (os + device type: TODO) でdeviceを作る。'):
        identifier = self.app.pargs.identifier

        udid = Device.create_if_not_exists(identifier)
        print("export %s=%s" % (ENV_KEY_FOR_UDID, udid))


class DeviceController(CementBaseController):
    class Meta:
        label = 'start'
        arguments = [
        ]

    @expose()
    def start(self):
        device = Device.get_current()
        device.launch_device()
        device.install_app()
        device.launch_app()

    @expose()
    def reload(self):
        device = Device.get_current()
        device.install_app()
        device.launch_app()

    # can't close window (background shutdown only ;< )
    # @expose()
    # def stop(self):
    #     device = Device.get_current()
    #     device.shutdown()


class App(CementApp):
    class Meta:
        label = 'app'
        base_controller = 'base'
        handlers = [BaseController, DeviceController]

if __name__ == '__main__':
    with App() as app:
        app.run()
