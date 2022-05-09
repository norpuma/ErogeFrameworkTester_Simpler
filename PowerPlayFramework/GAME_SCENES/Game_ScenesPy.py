import uuid

GLOBAL_DEBUG_FLAG = False

class ABSTRACT_Game_Scene(object):
    READY_TO_START = "READY_TO_START"
    PREPARE_FOR_SCENE = "PREPARE_FOR_SCENE"
    PRESENT_START = "PRESENT_START"
    UPDATE_DUE_TO_CONTEXT = "UPDATE_DUE_TO_CONTEXT"
    PRESENT_UPDATE = "PRESENT_UPDATE"
    UPDATE_DUE_TO_PLAYER_INPUT = "UPDATE_DUE_TO_PLAYER_INPUT"
    SHOULD_END = "SHOULD_END"
    PRESENT_END = "PRESENT_END"
    FINISHED = "FINISHED"
    states = [
        READY_TO_START,
        PREPARE_FOR_SCENE,
        PRESENT_START,
        UPDATE_DUE_TO_CONTEXT,
        PRESENT_UPDATE,
        UPDATE_DUE_TO_PLAYER_INPUT,
        SHOULD_END,
        PRESENT_END,
        FINISHED,
    ]
    def __init__(self, scene_id = None):
        if scene_id is not None:
            self.scene_id = scene_id
        else:
            self.scene_id = uuid.uuid4()
        self.status = ABSTRACT_Game_Scene.READY_TO_START
    
        self.should_run_function = None

        self.before_run_function = None
        self.scene_start_presentation = None

        self.scene_update_function = None
        self.scene_player_input_processing_function = None
        self.scene_update_presentation = None

        self.after_run_function = None
        self.scene_end_presentation = None
    
    def should_run(self):
        if self.should_run_function is not None:
            return self.should_run_function(self)
        else:
            return False
    
    def run(self):
        if GLOBAL_DEBUG_FLAG:
            print("----> STATUS is: ", self.status)
        if self.status is ABSTRACT_Game_Scene.FINISHED:
            return
        elif self.status is ABSTRACT_Game_Scene.READY_TO_START:
            self.status = ABSTRACT_Game_Scene.PREPARE_FOR_SCENE
        elif self.status is ABSTRACT_Game_Scene.PREPARE_FOR_SCENE:
            self.status = ABSTRACT_Game_Scene.PRESENT_START
            if self.before_run_function is not None:
                self.before_run_function(self)
        elif self.status is ABSTRACT_Game_Scene.PRESENT_START:
            self.status = ABSTRACT_Game_Scene.UPDATE_DUE_TO_CONTEXT
            if self.scene_start_presentation is not None:
                self._present(self.scene_start_presentation)

        elif self.status is ABSTRACT_Game_Scene.UPDATE_DUE_TO_CONTEXT:
            self.status = ABSTRACT_Game_Scene.PRESENT_UPDATE
            if self.scene_update_function is not None:
                self.scene_update_function(self)
        elif self.status is ABSTRACT_Game_Scene.PRESENT_UPDATE:
            self.status = ABSTRACT_Game_Scene.UPDATE_DUE_TO_PLAYER_INPUT
            if self.scene_update_presentation is not None:
                self._present(self.scene_update_presentation)
        elif self.status is ABSTRACT_Game_Scene.UPDATE_DUE_TO_PLAYER_INPUT:
            self.status = ABSTRACT_Game_Scene.UPDATE_DUE_TO_CONTEXT
            if self.scene_player_input_processing_function is not None:
                self._get_player_input(self.scene_player_input_processing_function)

        elif self.status is ABSTRACT_Game_Scene.SHOULD_END:
            self.status = ABSTRACT_Game_Scene.PRESENT_END
            if self.after_run_function is not None:
                self.after_run_function(self)
        elif self.status is ABSTRACT_Game_Scene.PRESENT_END:
            self.status = ABSTRACT_Game_Scene.FINISHED
            if self.scene_end_presentation is not None:
                self._present(self.scene_end_presentation)
    
    def interrupt_scene(self, gracefully = True, context = None):
        if gracefully:
            self.status = ABSTRACT_Game_Scene.SHOULD_END
        else:
            self.status = ABSTRACT_Game_Scene.FINISHED

