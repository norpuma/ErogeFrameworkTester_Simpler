import uuid

GLOBAL_DEBUG_FLAG = False

class Object(object):
    pass

class Game_Scene(object):
    def __init__(self, scene_id = None):
        if scene_id is not None:
            self.scene_id = scene_id
        else:
            self.scene_id = uuid.uuid4()
    
        self.prepare_scene_and_create_context_function = None
        self.scene_start_presentation = None

        self.scene_update_function = None
        self.scene_player_input_processing_function = None
        self.scene_update_presentation = None

        self.resume_after_scene_switch_function = None

        self.after_run_function = None
        self.scene_end_presentation = None

class ABSTRACT_Active_Scene_Reference(object):
    READY_TO_START = "READY_TO_START"
    PRESENT_START = "PRESENT_START"
    UPDATE_DUE_TO_CONTEXT = "UPDATE_DUE_TO_CONTEXT"
    PRESENT_UPDATE = "PRESENT_UPDATE"
    UPDATE_DUE_TO_PLAYER_INPUT = "UPDATE_DUE_TO_PLAYER_INPUT"
    SHOULD_END = "SHOULD_END"
    PRESENT_END = "PRESENT_END"
    FINISHED = "FINISHED"
    WAITING_FOR_NEXT_SCENE = "WAITING_FOR_NEXT_SCENE"
    states = [
        READY_TO_START,
        PRESENT_START,
        UPDATE_DUE_TO_CONTEXT,
        PRESENT_UPDATE,
        UPDATE_DUE_TO_PLAYER_INPUT,
        SHOULD_END,
        PRESENT_END,
        FINISHED,
        WAITING_FOR_NEXT_SCENE,
    ]
    def __init__(self, referred_scene, previous_context):
        self.referred_scene = referred_scene
        self._prepare_scene_and_create_context(previous_context)

    def _prepare_scene_and_create_context(self, previous_context):
        if previous_context is None:
            previous_context = Object()
        new_context = None
        if self.referred_scene.prepare_scene_and_create_context_function is not None:
            new_context = self.referred_scene.prepare_scene_and_create_context_function(self, previous_context)
        if new_context is None:
            new_context = previous_context
        self.scene_context = new_context
        self.status = ABSTRACT_Active_Scene_Reference.READY_TO_START

    def run(self):
        if GLOBAL_DEBUG_FLAG:
            print("----> STATUS is: ", self.status)
        if self.status is ABSTRACT_Active_Scene_Reference.FINISHED:
            return
        elif self.status is ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE:
            raise Exception("ABSTRACT_Active_Scene_Reference: run(): Trying to run scene {0} when it is in status {1}.".format(self.scene_id, ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE))
        elif self.status is ABSTRACT_Active_Scene_Reference.READY_TO_START:
            self.status = ABSTRACT_Active_Scene_Reference.PRESENT_START
        elif self.status is ABSTRACT_Active_Scene_Reference.PRESENT_START:
            self.status = ABSTRACT_Active_Scene_Reference.UPDATE_DUE_TO_CONTEXT
            if self.referred_scene.scene_start_presentation is not None:
                self._present(self.referred_scene.scene_start_presentation)

        elif self.status is ABSTRACT_Active_Scene_Reference.UPDATE_DUE_TO_CONTEXT:
            self.status = ABSTRACT_Active_Scene_Reference.PRESENT_UPDATE
            if self.referred_scene.scene_update_function is not None:
                self.referred_scene.scene_update_function(self, self.scene_context)
        elif self.status is ABSTRACT_Active_Scene_Reference.PRESENT_UPDATE:
            self.status = ABSTRACT_Active_Scene_Reference.UPDATE_DUE_TO_PLAYER_INPUT
            if self.referred_scene.scene_update_presentation is not None:
                self._present(self.referred_scene.scene_update_presentation)
        elif self.status is ABSTRACT_Active_Scene_Reference.UPDATE_DUE_TO_PLAYER_INPUT:
            self.status = ABSTRACT_Active_Scene_Reference.UPDATE_DUE_TO_CONTEXT
            if self.referred_scene.scene_player_input_processing_function is not None:
                self._get_player_input(self.referred_scene.scene_player_input_processing_function)

        elif self.status is ABSTRACT_Active_Scene_Reference.SHOULD_END:
            self.status = ABSTRACT_Active_Scene_Reference.PRESENT_END
            if self.referred_scene.after_run_function is not None:
                self.referred_scene.after_run_function(self, self.scene_context)
        elif self.status is ABSTRACT_Active_Scene_Reference.PRESENT_END:
            self.status = ABSTRACT_Active_Scene_Reference.FINISHED
            if self.referred_scene.scene_end_presentation is not None:
                self._present(self.referred_scene.scene_end_presentation)
    
    def interrupt_scene(self, gracefully = True, context = None):
        if gracefully:
            self.status = ABSTRACT_Active_Scene_Reference.SHOULD_END
        else:
            self.status = ABSTRACT_Active_Scene_Reference.FINISHED

    def set_scene_switch(self, next_scene_id):
        self.next_scene_id = next_scene_id
        self.next_status_before_switch = self.status
        self.status = ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE

    def resume_after_scene_switch(self, returning_context):
        self.status = self.next_status_before_switch
        self.next_status_before_switch = None
        returned_scene_id = self.next_scene_id
        if self.referred_scene.resume_after_scene_switch_function is not None:
            self.referred_scene.resume_after_scene_switch_function(self.scene_context, returned_scene_id, returning_context)
