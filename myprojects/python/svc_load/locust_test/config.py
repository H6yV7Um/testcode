#coding: utf-8

#class mapping
CLASS_MAPPING = {
    0: '1V1 class test',
    1: 'other class test',
    5: '1v5 class test',
    12: 'public class test'
}

#operation mapping
OPERATION_MAPPING = {
    1: "login",
    2: "enter_class",
    18: 'do_receive_pushed_message',
    #teacher operation
    3: "do_chat_in_classroom",
    4: "do_change_textbook_page",
    5: "do_add_textbook",
    6: "do_modify_textbook",
    7: "do_delete_textbook",
    8: "do_clear_textbook",
    9: "do_add_white_board",
    10: "do_get_white_board",
    11: "do_modify_white_board",
    12: "do_delete_white_board",
    13: "do_clear_white_board",
    #student operation
    14: "do_get_pen_color",
    15: "do_hand_up",
    16: "do_hand_down",
    17: "do_chat_in_classroom"
}

LOGIN_OP_CODE = 1
ENTER_OP_CODE = 2
PUSH_OP_CODE = 18

#用户角色标记
STUDENT_FLAG = 0
STATIC_STUDENT_FLAG = 2
TEACHER_FLAG = 1

