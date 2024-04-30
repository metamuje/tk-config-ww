# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook that gets executed every time an engine has been fully initialized.
"""

import os
import sgtk

Hook = sgtk.get_hook_baseclass()

class EngineInit(Hook):
    def execute(self, engine, **kwargs):
        """
        Executed when a Toolkit engine has been fully initialized.

        At this point, all apps and frameworks have been loaded,
        and the engine is fully operational.

        :param engine: Engine that has been initialized.
        :type engine: :class:`~sgtk.platform.Engine`
        """

        sg = engine.shotgun
        project_id = engine.context.project["id"]

        fields = ["sg_rez_env"]
        software_info = sg.find_one("Software", [["projects", "is", {"type": "Project", "id": project_id}]], fields)

        if software_info and 'sg_rez_env' in software_info:
            rez_env = software_info['sg_rez_env']
            print(f"rez_env: {rez_env}")

            cmd = f"rez-env {rez_env}"
            print(f"Executing command: {cmd}")
            os.system(cmd)
        else:
            print("No rez environment found for the project.")



        # print('*' * 80)
        # print(f"Toolkit engine '{engine.name}' has been initialized.")

        # if engine.context and engine.context.project:
        #     project_name = engine.context.project.get('name')
        #     print(f"Current project: {project_name}")
        # else:
        #     print("No project information available in the context.")

        # if engine.software_entity:
        #     software_name = engine.software_entity.get('name')
        #     print(f"Current software: {software_name}") 

        # print('*' * 80)

        # print('=' * 80)
        # sg = engine.context.project
        # print(sg)

        # ab = engine.context.project.get('name')
        # print(ab)

        # cf = engine.context.project.get('id')
        # print(cf)

        # print('=' * 80)