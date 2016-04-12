#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import json
import os
import subprocess
import time

import sys


def exit_with_message(msg):
    sys.stderr.write(msg)
    exit(1)

ENV_KEY_FOR_UDID = "simrun_CURRENT_UDID"


class Utility:
    @staticmethod
    def execute(command, format=None):
        if type(command) == str:
            command = command.split(" ")
        ret = subprocess.check_output(command).decode('ascii')
        if ret is not None:
            ret = ret.strip()

        if format == "json":
            return json.loads(ret)
        else:
            return ret

    @staticmethod
    def get_udid():
        udid = os.environ[ENV_KEY_FOR_UDID]
        if udid is None or len(udid) == 0:
            exit_with_message("no udid set.")
        return udid


class Project:
    @staticmethod
    def get_name():
        projs = glob.glob("*.xcodeproj")
        if len(projs) == 0:
            exit_with_message("cannot find project file.")
        elif len(projs) > 1:
            exit_with_message("multiple project file found.:", projs)
        else:
            return projs[0].replace(".xcodeproj", "")

    @staticmethod
    def get_app_path():
        project_name = Project.get_name()
        target_name = project_name  # project = target

        build_config = "Debug-iphonesimulator"
        app_path = "DerivedData/%s/Build/Products/%s/%s.app" % (project_name, build_config, target_name)
        return app_path

    @staticmethod
    def get_bundle_identifier():
        app_path = Project.get_app_path()
        cmd = ['defaults', 'read', app_path + '/Info', 'CFBundleIdentifier']
        return Utility.execute(cmd).strip()


class Xcrun:
    @staticmethod
    def get_device(identifier):
        device_list = Utility.execute("xcrun simctl list -j", format='json')['devices']

        matches = []
        for runtime in device_list.keys():
            for device in device_list[runtime]:
                if device['name'] == identifier:
                    matches.append(device)
        return matches

    @staticmethod
    def get_device_by_udid(udid):
        device_list = Utility.execute("xcrun simctl list -j", format='json')['devices']
        for runtime in device_list.keys():
            for device in device_list[runtime]:
                if device['udid'] == udid:
                    return device


    @staticmethod
    def create_device(identifier, device_type='iPhone 6s', runtime='com.apple.CoreSimulator.SimRuntime.iOS-9-3'):
        created_udid = Utility.execute("xcrun simctl create".split() + [identifier, device_type, runtime])
        #print("create new device:%s as (%s %s)" % (created_udid, device_type, runtime))
        return created_udid

    @staticmethod
    def wait_until_booted(udid):
        while True:
            device = Xcrun.get_device_by_udid(udid)
            if device is None:
                exit_with_message("no device:%s" % udid)
            if device['state'] != 'Booted':
                # print("not booted. wait..")
                time.sleep(0.5)
            else:
                break

    @staticmethod
    def shutdown(udid):
        Utility.execute("xcrun simctl shutdown %s" % udid)


class Device:
    @classmethod
    def create_if_not_exists(cls, identifier):
        u"""
        指定のidentifier + (os + device type: TODO) でdeviceを作る。
        """
        devices = Xcrun.get_device(identifier)
        current_udid = None
        if len(devices) == 0:
            current_udid = Xcrun.create_device(identifier)
        elif len(devices) > 1:
            exit_with_message("multiple devices for identifier")
        else:
            device = devices[0]
            current_udid = device['udid']
        return current_udid


    @classmethod
    def get_current(cls):
        udid = Utility.get_udid()
        device = cls(udid)
        return device

    def __init__(self, udid):
        self.udid = udid

    def launch_device(self):
        device_info = Xcrun.get_device_by_udid(self.udid)
        if device_info is None:
            exit_with_message("no device:%s" % self.udid)
        if device_info['state'] == 'Booted':
            exit_with_message("already started?")
        app_path = '/Applications/Xcode.app/Contents/Developer/Applications/Simulator.app'
        Utility.execute(["open", "-n", app_path, "--args", "-CurrentDeviceUDID", self.udid])
        Xcrun.wait_until_booted(self.udid)

    def install_app(self):
        app_path = Project.get_app_path()
        ret = Utility.execute("xcrun simctl install %s %s" % (self.udid, app_path))
        return ret

    def launch_app(self):
        bundle_identifier = Project.get_bundle_identifier()
        Utility.execute("xcrun simctl launch %s %s" % (self.udid, bundle_identifier))

    def shutdown(self):
        Xcrun.shutdown(self.udid)


def main():
    pass

if __name__ == '__main__':
    main()
