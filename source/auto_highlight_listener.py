import bpy
from typing import Any, cast

_HIGHLIGHT_INTERVAL = 0.25
_last_active_by_workspace = {}

def _highlight_active_object():
    window_manager = bpy.context.window_manager
    if window_manager is None:
        return _HIGHLIGHT_INTERVAL

    active_keys = set()
    for window in window_manager.windows:
        workspace = window.workspace
        key = (window.as_pointer(), workspace.as_pointer())
        active_keys.add(key)

        active_object = window.view_layer.objects.active
        active_id = active_object.as_pointer() if active_object is not None else None
        if _last_active_by_workspace.get(key) == active_id:
            continue
        #end if
        _last_active_by_workspace[key] = active_id

        if active_object is None or window.screen is None:
            continue
        #end if

        for area in window.screen.areas:
            if area.type != 'OUTLINER':
                continue
            #end if

            region = next((item for item in area.regions if item.type == 'WINDOW'), None)
            if region is None:
                continue
            #end if
            try:
                override = cast(Any, bpy.context.temp_override(window=window, area=area, region=region))
                with override:
                    bpy.ops.outliner.show_active()
                #end with
            except RuntimeError:
                pass
            #end try

            break
        #end for
    #end for

    for key in set(_last_active_by_workspace) - active_keys:
        del _last_active_by_workspace[key]
    #end for

    return _HIGHLIGHT_INTERVAL
#end _highlight_active_object

def start_auto_highlight_listener():
    if not bpy.app.timers.is_registered(_highlight_active_object):
        bpy.app.timers.register(_highlight_active_object, first_interval=_HIGHLIGHT_INTERVAL, persistent=True)
#end start_auto_highlight_listener

def stop_auto_highlight_listener():
    if bpy.app.timers.is_registered(_highlight_active_object):
        bpy.app.timers.unregister(_highlight_active_object)
    #end if
    _last_active_by_workspace.clear()
#end stop_auto_highlight_listener
