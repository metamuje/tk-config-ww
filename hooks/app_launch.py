# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
App Launch Hook

This hook is executed to launch the applications.
"""

import os
import sgtk

Hook = sgtk.get_hook_baseclass()

class AppLaunch(Hook):
    """
    Hook to run an application.
    """
    
    def execute(
        self, app_path, app_args, version, engine_name, software_entity=None,  **kwargs
    ):
        """
        The execute function of the hook will be called to start the required application

        :param app_path: (str) The path of the application executable
        :param app_args: (str) Any arguments the application may require
        :param version: (str) version of the application being run if set in the
            "versions" settings of the Launcher instance, otherwise None
        :param engine_name (str) The name of the engine associated with the
            software about to be launched.
        :param software_entity: (dict) If set, this is the Software entity that is
            associated with this launch command.

        :returns: (dict) The two valid keys are 'command' (str) and 'return_code' (int).
        """

        #Get the Shotgun API instance
        sg = sgtk.platform.current_engine().shotgun 
       # Get the project ID from the current context
        project_id = sgtk.platform.current_engine().context.project["id"]

        # 프로젝트에 대한 Software 엔티티 정보 조회
        fields = ["sg_rez_env", "sg_rez_excute", "sg_dcc_version"]
        software_info = sg.find("Software", [["projects", "is", {"type": "Project", "id": project_id}]], fields)
        
        # Check if software info is found
        if not software_info:
            print("No software info found")
            return {"command": "No software info found", "return_code": 1}
        
        # Check if rez environment and execute are found
        for software in software_info:
            rez_dcc_version = software.get("sg_dcc_version")
            if rez_dcc_version == version:
                print("rez_dcc_version: %s" % rez_dcc_version)
                rez_env = software.get("sg_rez_env")
                rez_excute = software.get("sg_rez_excute")
                break
            
        if sgtk.util.is_linux():
            # print("app_path: %s" % app_path)
            # print("app_args: %s" % app_args)
            # print("version: %s" % version)
            # print("engine_name: %s" % engine_name)
            # print(software_entity)
            #cmd = "%s %s &" % (app_path, app_args)
            cmd = "rez-env %s -- %s %s" % (rez_env, rez_excute, app_args)

        elif sgtk.util.is_macos():
            # If we're on OS X, then we have two possibilities: we can be asked
            # to launch an application bundle using the "open" command, or we
            # might have been given an executable that we need to treat like
            # any other Unix-style command. The best way we have to know whether
            # we're in one situation or the other is to check the app path we're
            # being asked to launch; if it's a .app, we use the "open" command,
            # and if it's not then we treat it like a typical, Unix executable.
            if app_path.endswith(".app"):
                # The -n flag tells the OS to launch a new instance even if one is
                # already running. The -a flag specifies that the path is an
                # application and supports both the app bundle form or the full
                # executable form.
                cmd = 'open -n -a "%s"' % (app_path)
                if app_args:
                    cmd += " --args %s" % app_args
            else:
                cmd = "%s %s &" % (app_path, app_args)

        else:
            # on windows, we run the start command in order to avoid
            # any command shells popping up as part of the application launch.
            cmd = 'start /B "App" "%s" %s' % (app_path, app_args)

        # run the command to launch the app
        exit_code = os.system(cmd)

        return {"command": cmd, "return_code": exit_code}

####################################################


'''
# 버전별로 설정하는 것이 아니라 desk-top가 실행 되었을때 rez가 통으로 연결되고 아이콘을 클릭 할 때마다 rez-env가 실행되는 것이 좋다.
# 이렇게 하면 버전 관리가 쉬워지고 사용자 입장에서도 편리하다. 그래서 버전 체크 코드는 삭제한다.
        if tank.util.is_linux():
            # on linux, we just run the executable directly
            program = app_path.split("/")[-1]
            if program == "Nuke13.2":
                version = "13.2.2"
            elif program == "Nuke13.0":
                version = "13.0.1"
            elif program == "Nuke12.2":
                version = "12.2.2"
            elif program == "Nuke11.2":
                version = "11.2.5"
            cmd = "rez-env nuke-%s -- %s %s &" % (version, program, app_args)
            #cmd = "%s %s &" % (app_path, app_args)
            print(cmd)

        elif tank.util.is_macos():
            # If we're on OS X, then we have two possibilities: we can be asked
            # to launch an application bundle using the "open" command, or we
            # might have been given an executable that we need to treat like
            # any other Unix-style command. The best way we have to know whether
            # we're in one situation or the other is to check the app path we're
            # being asked to launch; if it's a .app, we use the "open" command,
            # and if it's not then we treat it like a typical, Unix executable.
            if app_path.endswith(".app"):
                # The -n flag tells the OS to launch a new instance even if one is
                # already running. The -a flag specifies that the path is an
                # application and supports both the app bundle form or the full
                # executable form.
                cmd = 'open -n -a "%s"' % (app_path)
                if app_args:
                    cmd += " --args %s" % app_args
            else:
                cmd = "%s %s &" % (app_path, app_args)

        else:
            # on windows, we run the start command in order to avoid
            # any command shells popping up as part of the application launch.
            cmd = 'start /B "App" "%s" %s' % (app_path, app_args)

        # run the command to launch the app
        exit_code = os.system(cmd)

        return {"command": cmd, "return_code": exit_code}
'''    



