# coding:utf-8
import struct
from functools import lru_cache
try:
    from aenum import Enum, unique
except ImportError:
    from enum import Enum, unique

endic_DS = {}
# 消息的封装定义
dedic_DS = {}
# 消息的解析定义
# _dataTf_DS ='';
_key_DS = ''
_tf_DS = ''
_ti_DS = -1


# _formatMapEncode = ['c','i','I','h','H','q','Q','str'];用于封装的结构体，所允许的值类型
# _formatMapDEcode =
# ['c','i','I','h','H','q','Q','str','i_count','I_count','h_count','H_count'];用于解封的结构体，所允许的值类型,
# 不能使用*数组类型

# 负载均衡
endic_DS[0x00100011] = (
    "FailedServerNum_,_I",
    "ServerIP_,_B",
    "IsManualSetting_,_B",
    "ISPIdx_,_I",
    "LocationCode_,_I"
)
dedic_DS[0x00100011] = (
    "RspCode_,_I",
    "AccServerIPNum_,_I_count",
    "Server_,_Server",
    "HttpServerIPNum_,_H_count",
    "HttpServer_,_HttpServer"
)

dedic_DS['Server'] = (
    "AccIP_,_I",
    "AccPortNum_,_I_count",
    "AccPort_,_H"
)
dedic_DS['HttpServer'] = (
    "ProtoType_,_c",
    "HttpIP_,_I",
    "HttpPorNum_,_c_count",
    "HttpPort_,_H"
    )

# 获取心跳配置
dedic_DS[0x0011000E] = (
    "Interval_,_H",
    "C2STimeout_,_H",
    "S2CSwitch_,_c",
    "S2CTimeout_,_H"
)

# 客户端心跳设置通知
dedic_DS[0x0011000F] = (
    "Interval_,_H",
    "S2CSwitch_,_c",
    "S2CTimeout_,_H"
)

# 客户端接入
endic_DS[0x00110011] = (
    "ClientType_,_I",
    "ClientVer_,_str",
    "ClientFlag_,_str",
    "ClientOSFlag_,_c"
)

dedic_DS[0x00110011] = (
    "RspCode_,_I",
    "SessionKeyLength_,_I_count",
    "SessionKey_,_c",
    "UpgradeInfo_,_str",
    "ClientInternetIP_,_I",
    "ClientPilotTips_,_str",
    "NetworkCommitInterval_,_I"
)

# 用户登录
endic_DS[0x00110012] = (
    "AccountType_,_B",
    "Account_,_str",
    "AuthTicketLength_,_i",
    "AuthTicket_,_c*",
    "DefaultStatus_,_B",
    "ExternPassword_,_str"
)
dedic_DS[0x00110012] = (
    "RspCode_,_I",
    "UID_,_Q",
    "UserName_,_str",
    "ServerTime_,_Q",
    "LastLoginTime_,_Q",
    "UserRight_,_Q",
    "DefaultStatus_,_c"
)

# 变更个人状态
endic_DS[0x00110016] = [
    "Status_,_c"
]
dedic_DS[0x00110016] = [
    "Status_,_c"
]

# 1v1聊天消息文字
endic_DS[0x0012001C] = (
    "MessageID_,_Q",
    "ClientType_,_c",
    "SentTime_,_I",
    "ChatMessage_,_str",
    "Option_,_str"
)
# 1v1聊天文字转发接受确认
dedic_DS[0x0012001D] = (
    "RspCode_,_c"
)
# 1v1聊天消息文字接受确认
endic_DS[0x00120020] = (
    "MessageID_,_Q",
    "AcvCode_,_H"
)

# 进入教室v2
endic_DS[0x00130110] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "UserSwitchFlag_,_I",
    "UserName_,_str",
    "AVSDKNum_,_I",
    "AVSDK_,_c*"
)

dedic_DS[0x00130110] = (
    "RspCode_,_I",
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "SchoolName_,_str",
    "ClassName_,_str",
    "StartTime_,_I",
    "Status_,_c",
    "MsgMode_,_c",
    "SwitchFlag_,_Q",
    "OperatonFlag_,_Q",
    "OwnerID_,_Q",
    "OwnerIn_,_c",
    "OwnerName_,_str",
    "TeacherID_,_Q",
    "TeacherIn_,_c",
    "TeacherName_,_str",
    "AssistantNum_,_I_count",
    "Assistants_,_Assistant",
    "StudentNum_,_I_count",
    "Students_,_Student"
)

dedic_DS["Assistant"] = (
    "AssistID_,_Q",
    "UserName_,_str",
    "Identity_,_c",
    "UserRight_,_c",
    "UserSwitchFlag_,_c",
    "ClientType_,_c",
    "Reserved_,_c",
)

dedic_DS["Student"] = (
    "StudentID_,_Q",
    "UserName_,_str",
    "Identity_,_c",
    "UserRight_,_c",
    "UserSwitchFlag_,_c",
    "ClientType_,_c",
    "Reserved_,_c",
)
# 进入教室v3
endic_DS[0x00130112] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "UserSwitchFlag_,_I",
    "UserName_,_str",
    "AVSDKNum_,_I",
    "AVSDK_,_c*",
    "UserCusData_,_str"
)
# 进入教室v4
endic_DS[0x00130113] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_I",
    "UserRole_,_c",
    "Reserved_1_,_c",
    "Reserved_2_,_c",
    "Reserved_3_,_c",
    "UserSwitchFlag_,_I",
    "UserName_,_str",
    "AVSDKNum_,_I",
    "AVSDK_,_c*",
    "UserCusData_,_str"
)

# 变更演示文档页码
endic_DS[0x0013001D] = (
    "CID_,_Q",
    "Type_,_c",
    "TotalPagePrefix_,_c",
    "TotalPage_,_c",
    "CurrentPagePrefix_,_c",
    "CurrentPage_,_c"
)
dedic_DS[0x0013001D] = (
    "RspCode_,_I",
    "CID_,_Q",
    "Type_,_c",
    "TotalPage_,_H",
    "CurrentPage_,_H"
)

# 1v1文本消息
endic_DS[0x00130016] = (
    "CID_,_Q",
    "SentTime_,_Q",
    "Option_,_str",
    "Text_,_str"
)

dedic_DS[0x00130016] = (
    "CID_,_Q",
    "SentTime_,_Q",
    "Option_,_str",
    "Text_,_str"
)
# 进入教室通知
dedic_DS[0x00130011] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "UID_,_Q",
    "UserName_,_str",
    "UserIdentity_,_c",
    "UserRight_,_c",
    "UserSwitchFlag_,_Q",
    "ClientType_,_c",
    "UserRole_,_c",
    "MediaID_,_I",
    "UserCusData_,_str",
    "Time_,_Q"
)
# 进入教室完成
endic_DS[0x00130012] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q"
)

# 离开教室
endic_DS[0x00130013] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q"
)
# 离开教室通知
dedic_DS[0x00130014] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "UserID_,_Q",
    "UserName_,_str",
    "UserIdentity_,_c",
    "UserSwitchFlag_,_Q",
    "Time_,_Q"
)

# 教室关闭通知
dedic_DS[0x00130015] = (
    "SID_,_Q",
    "CID_,_Q",
    "CourseID_,_Q",
    "Reason_,_H"
)

# 强制用户下线
endic_DS[0x00110014] = (
    "reasion,_I",
)

# 白板数据
endic_DS[0x00130017] = (
    "CID_,_Q",
    "SentTime_,_I",
    "MD5Length_,_I",
    "BackgroundMD5_,_c*",
    "ItemOperate_,_c",
    "ItemNum_,_I",
    "ItemNumber_,_ItemNum"
)
endic_DS["ItemNum"] = (
    "ItemClientSeq_,_I",
    "ItemServerSeq_,_I",
    "ItemDataLength_,_I",
    "ItemData_,_c*"
)
dedic_DS[0x00130017] = (
    "CID_,_Q",
    "SentTime_,_I",
    "MD5Length_,_I_count",
    "BackgroundMD5_,_c*",
    "ItemOperate_,_c",
    "ItemNum_,_I_count",
    "ItemNumber_,_ItemNum"
)
dedic_DS["ItemNum"] = (
    "ItemClientSeq_,_I",
    "ItemServerSeq_,_I",
    "ItemDataLength_,_I_count",
    "ItemData_,_c*"
)
# 举手消息
endic_DS[0x00130120] = [
    "CID_,_Q"
]
dedic_DS[0x00130120] = (
    "RspCode_,_I",
    "CID_,_Q"
)
# 放手消息
endic_DS[0x00130121] = [
    'CID_,_Q'
]
dedic_DS[0x00130121] = (
    "RspCode_,_I",
    'CID_,_Q'
)

# 获取AV SDK分配比例
dedic_DS[0x00130101] = (
    "RspCode_,_I",
    "SDKRatioNum_,_I_count",
    "VecSDKRatio_,_SDKRatio"
)
dedic_DS["SDKRatio"] = (
    "Type_,_c",
    "Ratio_,_H",
    "MaxUsedNum_,_I",
    "UsedNum_,_I"
)

# 获取教室（公开课，小班课）使用的AV SDK
endic_DS[0x00130104] = (
    "ClassType_,_c",
)
dedic_DS[0x00130104] = (
    "RspCode_,_I",
    "ClassType_,_c",
    "AVSDK_,_c"
)

# 设置1v1教室的sdk比例
endic_DS[0x00130107] = (
    "RuleID_,_c",
    "ResetAll_,_c",
    "SDKRatioNum_,_I_count",
    "SerSDKs_,_SerSDK"
)
endic_DS["SerSDK"] = (
    "Type_,_c",
    "RatioPefix_,_c",
    "Ratio_,_c",
    "MaxUsedNum_,_I"
)
dedic_DS[0x00130107] = (
    "RspCode_,_I",
)

# 获取1v1教室的sdk比例
endic_DS[0x00130108] = (
    "RuleID_,_c",
)
dedic_DS[0x00130108] = (
    "RspCode_,_I",
    "RuleID_,_c",
    "SDKRatioNum_,_I_count",
    "CurSerSDKs_,_CurSerSDK"
)
dedic_DS["CurSerSDK"] = (
    "Type_,_c",
    "Ratio_,_H",
    "MaxUsedNum_,_I",
    "UsedNum_,_I"
)

# 确认sdk列表
endic_DS[0x00130114] = (
    "CID_,_Q",
    "OkSDK_,_c",
    "SDKNum_,_I",
    "VecSDK_,_c*"
)
# sdk列表变更
endic_DS[0x00130115] = (
    "CID_,_Q",
    "OkSDK_,_c",
    "SDKNum_,_I",
    "VecSDK_,_c*"
)
dedic_DS[0x00130115] = (
    "RspCode_,_I",
    "CID_,_Q"
)
# sdk列表变化通知
dedic_DS[0x00130116] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "OkSDK_,_c",
    "SDKNum_,_I_count",
    "VecSDKs_,_sdk"
)
dedic_DS["sdk"] = [
    "VecSDK_,_B"
]

# 更改sdk请求
endic_DS[0x00130117] = (
    "CID_,_Q",
    "SDKID_,_c",
    "Req_,_c"
)
# 更改sdk请求通知
dedic_DS[0x00130118] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "sdkid_,_c",
    "Req_,_c"
)
# 更改sdk请求响应
endic_DS[0x00130119] = (
    "CID_,_Q",
    "SDKID_,_c",
    "Rsp_,_c"
)
# 更改sdk请求响应通知
dedic_DS[0x0013011A] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "SDKID_,_c",
    "Rsp_,_c"
)
# 获取教室使用的AVSDK
endic_DS[0x0013011B] = (
    "CID_,_Q",
)
dedic_DS[0x0013011B] = (
    "CID_,_Q",
    "SDKID_,_c"
)

# sdk列表变更版本2
endic_DS[0x0013011C] = (
    "CID_,_Q",
    "SDKNum_,_c",
    "VecSDK_,_c*"
)
dedic_DS[0x0013011C] = (
    "RspCode_,_I",
    "CID_,_Q"
)
# sdk列表变化通知版本2
dedic_DS[0x0013011D] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "SDKNum_,_c_count",
    "VecSDKs_,_sdk"
)
# 变更发言列表
endic_DS[0x00130122] = (
    "CID_,_Q",
    "OpType_,_c",
    "TargetUID_,_Q"
)
dedic_DS[0x00130122] = (
    "RspCode_,_I",
    "CID_,_Q",
    "OpType_,_c",
    "TargetUID_,_Q"
)

# 发言列表变更通知
dedic_DS[0x00130123] = (
    "CID_,_Q",
    "OpType_,_c",
    "TargeUID_,_Q",
    "AllowSpqakNum_,_H",
    "LineUserNum_,_I_count",
    "LineUserNumer_,_LineUserNum"
)
dedic_DS["LineUserNum"] = (
    "LineUserID_,_Q",
)

# 用户硬件状态更改
endic_DS[0x00130141] = (
    "CID_,_Q",
    "DeviceStatus_,_str"
)
dedic_DS[0x00130141] = (
    "RspCode_,_I",
)
# 用户硬件状态通知
dedic_DS[0x00130142] = (
    "CID_,_Q",
    "DeciveNum_,_H",
    "DeciveStatus_,_str",
    "InitFlag_,_c"
)
# 更新教材
endic_DS[0x00130145] = (
    "CID_,_Q",
    "TextbookData_,_str"
)
dedic_DS[0x00130145] = (
    "RspCode_,_I",
    "CID_,_Q",
    "UID_,_Q"
)
# 更换教材通知
endic_DS[0x00130146] = (
    "RspCode_,_I",
    "CID_,_Q",
    "SourceUID_,_Q"
)
dedic_DS[0x00130146] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "TextbookData_,_str"
)
# 发送教材相关的通用通知
endic_DS[0x00130147] = (
    "CID_,_Q",
    "Type_,_c",
    "NotifyData_,_str"
)
dedic_DS[0x00130147]= (
    "RspCode_,_I",
    "CID_,_Q",
    "Type_,_c",
    "NotifyData_,_str"
)
# 下发教材相关的通用通知
dedic_DS[0x00130148] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "Type_,_c",
    "NotifyData_,_str"
)
# 设置教材的通用设置
endic_DS[0x0013014A] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Setting_,_str"
)
dedic_DS[0x0013014A] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Setting_,_str"
)
# 下发教材的通用通知
dedic_DS[0x0013014B] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Setting_,_str"
)
# 设置教材的当前页码
endic_DS[0x0013014C] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"CurPagePerfix_,_c",
    "CurPage_,_H",
    "Reserved_,_str"
)
dedic_DS[0x0013014C] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "CurPage_,_H",
    "Reserved_,_str"
)
# 下发教材当前页码通知
dedic_DS[0x0013014D] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "CurPage_,_H",
    "Reserved_,_str"
)
# 设置教材当前页的滚动条位置
endic_DS[0x0013014E] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"PagePerfix_,_c",
    "Page_,_H",
    "PosX_,_str",
    "PosY_,_str"

)
dedic_DS[0x0013014E] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "PosX_,_str",
    "PosY_,_str"
)
# 下发教材当前页的滚动条位置通知
dedic_DS[0x0013014F] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "PosX_,_str",
    "PosY_,_str"
)
# 下发教材白板数据通知
dedic_DS[0x00130155] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "Operate_,_c",
    "GraphicNum_,_H_count",
    "GraphicItmes_,_Graphic"
)
dedic_DS["Graphic"] = (
    "ServerSeq_,_I",
    "SourceUID_,_Q",
    "GraphicStrData_,_str",
    "GraphicByteDataLen_,_H_count",
    "GraphicByteDatas_,_GraphicByteData"
)

# 获取教材指定页的板书数据
endic_DS[0x00130156] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"PagePerfix_,_c",
    "Page_,_H",
    "BeginSeq_,_I"
)
dedic_DS[0x00130156] = dedic_DS[0x00130155]
# 添加教材板书数据
endic_DS[0x00130157] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"PagePerfix_,_c",
    "Page_,_H",
    #"GraphicNumfix_,_c",
    "GraphicNum_,_H",
    "GraphicDataItems_,_GraphicAdd"
)
endic_DS["GraphicAdd"] = (
    "ClientSeq_,_I",
    "GraphicStrData_,_str",
    #"GraphicByteDataLenPerfix_,_c",
    "GraphicByteDataLen_,_I",
    "GraphicByteData_,_I*"
)
dedic_DS[0x00130157] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "GraphicNum_,_H_count",
    "GraphicDataItems_,_GraphicAdd2"
)
dedic_DS["GraphicAdd2"] = (
    "ServerSeq_,_I",
    "ClientSeq_,_I",
    "GraphicStrData_,_str",
    "GraphicByteDataLen_,_H_count",
    "GraphicByteDatas_,_GraphicByteData"
)
dedic_DS["GraphicByteData"] = (
    "GraphicByteData_,_c",
    )
# 删除教材板书数据
endic_DS[0x00130158] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"PagePerfix_,_c",
    "Page_,_H",
    #"GraphicNumfix_,_c",
    "GraphicNum_,_H",
    "GraphicServerSeq_,_I*"
)
dedic_DS[0x00130158] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "GraphicNum_,_H_count",
    "GraphicServerSeqs_,_GraphicServerSeq"
)
dedic_DS["GraphicServerSeq"] = (
    "GraphicServerSeq_,_I",
)
# 编辑板书数据
endic_DS[0x00130159] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "GraphicNum_,_H",
    "Graphic_,_GraphicModify"
)
endic_DS["GraphicModify"] = (
    "ServerSeq_,_I",
    "GraphicStrData_,_str",
    "GraphicByteDataLen_,_H",
    "GraphicByteData_,_c*"
)
dedic_DS[0x00130159] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "GraphicNum_,_H_count",
    "GraphicDataItems_,_GraphicModify2"
)
dedic_DS["GraphicModify2"] = dedic_DS["GraphicAdd2"]
# 清空教材板书数据
endic_DS[0x0013015A] = (
    "CID_,_Q",
    #"TextbookIDPerfix_,_c",
    "TextbookID_,_H",
    "TextbookType_,_c",
    #"PagePerfix_,_c",
    "Page_,_H",
)
dedic_DS[0x0013015A] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
)
# 万人教室在线人数通知
dedic_DS[0x00130165] = (
    "CID_,_Q",
    "UserNum_,_I"
)

# 请求指定用户做网络测试
endic_DS[0x00140018] = (
    "Host_,_str",
    "TimeLen_,_I",
    "UserNum_,_I",
    "UserID_,_Q*",
    "Reserved_,_I"
)
dedic_DS[0x00140018] = (
    "RspCode_,_I",
)
# 用户网络测试通知
dedic_DS[0x00140011] = (
    "Host_,_str",
    "TimeLen_,_I",
    "Reserved_,_I"
)
# 用户网络测试数据结果
endic_DS[0x00140012] = (
    "TestResult_,_str",
    "Reserved_,_I"
)
# 用户通用统计数据结果
endic_DS[0x0014001A] = (
    "KeyType_,_str",
    "StrData_,_str",
    "StrResvd_,_str",
    "Reserved_,_I"
)

# 群组服务
# 1获取群组列表
dedic_DS[0x00180020] = (
    "RspCode_,_I",
    "GroupNum_,_H_count",
    "GroupN_,_GroupNum"
)
dedic_DS["GroupNum"] = (
    "GID_,_Q",
    "InfoVer_,_I",
    "MemberListVer_,_I",
    "Status_,_c",
    "Name_,_str",
    "MsgSetting_,_c"
)
# 2获取群信息
endic_DS[0x00180021] = [
    "GID_,_Q"
]
dedic_DS[0x00180021] = (
    "RspCode_,_I",
    "GID_,_Q",
    "OwnerUID_,_Q",
    "InfoVer_,_I",
    "MemberListVer_,_I",
    "Status_,_c",
    "Name_,_str",
    "Type_,_I",
    "VIPFlag_,_c",
    "Level_,_c",
    "AuthType_,_c",
    "Brief_,_str",
    "Notice_,_str"
)
# 3群组信息变更通知
dedic_DS[0x00180022] = (
    "GID_,_Q",
    "InfoVer_,_I",
    "Status_,_c"
)
# 4获取群组成员列表
endic_DS[0x00180023] = [
    "GID_,_Q"
]
dedic_DS[0x00180023] = (
    "RspCode_,_I",
    "GID_,_Q",
    "MemberListVer_,_I",
    "MemberNum_,_I_count",
    "MemberNumber_,_MemberNum04"
)
dedic_DS["MemberNum04"] = (
    "UID_,_Q",
    "Status_,_I",
    "Right_,_c",
    "CardSetting_,_c",
    "CardInfoVer_,_I",
    "Nickname_,_str",
    "Identity_,_c",
    "Gender_,_c",
    "Tel_,_str",
    "Email_,_str",
    "Comment_,_str"
)
# 5群组成员列表变更通知
dedic_DS[0x00180024] = (
    "GID_,_Q",
    "MemberListVer_,_I"
)
# 6同步群组成员列表（群组不存在时创建群组）
endic_DS[0x0018002F] = (
    "GID_,_Q",
    "Name_,_str",
    "MemberNum_,_I_count",
    "MemberNumber01_,_MemberNum06"
)
endic_DS["MemberNum06"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)
dedic_DS[0x0018002F] = (
    "GID_,_Q",
    "RspCode_,_I"
)
# 7创建群组
endic_DS[0x00180030] = (
    "Name_,_str",
    "Type_,_I",
    "VIPFlag_,_c",
    "AuthType_,_c",
    "Brief_,_str",
    "Notice_,_str",
    "MemberNum_,_I",
    "MemberNumber02_,_MemberNum07"
)
endic_DS["MemberNum07"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)
dedic_DS[0x00180030] = (
    "RspCode_,_I",
    "GID_,_Q",
    "Name_,_str",
    "Type_,_I",
    "VIPFlag_,_c",
    "AuthType_,_c",
    "Brief_,_str",
    "Notice_,_str",
    "MemberNum_,_I_count",
    "MemberNumber03_,_MemberNum07"
)
dedic_DS["MemberNum07"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)
# 8新增群组通知
dedic_DS[0x00180031] = (
    "GID_,_Q",
    "OperateType_,_c"
)
# 9解散（删除）群组
endic_DS[0x00180032] = [
    "GID_,_Q"
]
dedic_DS[0x00180032] = (
    "GID_,_Q",
    "RspCode_,_I",
    "Name_,_str"
)
# 10删除群组通知
dedic_DS[0x00180033] = (
    "GID_,_Q",
    "OperateType_,_c",
    "Name_,_str"
)

# 11添加群组成员
endic_DS[0x00180036] = (
    "GID_,_Q",
    "AddMemberNum_,_I",
    "AddMemberNumber01_,_AddMemberNum"
)
endic_DS["AddMemberNum"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)
dedic_DS[0x00180036] = (
    "RspCode_,_I",
    "GID_,_Q",
    "MemberListVer_,_I",
    "AddMemberNum_,_I_count",
    "AddMemberNumber02_,_AddMemberNum"
)
dedic_DS["AddMemberNum"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)
# 12添加群组成员通知
dedic_DS[0x00180037] = (
    "AddType_,_c",
    "GID_,_Q",
    "InviteUID_,_Q",
    "MemberListVer_,_I",
    "AddMemberNum_,_I_count",
    "AddMemberNumber03_,_AddMemberNum"
)
dedic_DS["AddMemberNum"] = (
    "UID_,_Q",
    "Identity_,_c",
    "Nickname_,_str"
)

# 13删除群组成员
endic_DS[0x00180038] = (
    "GID_,_Q",
    "DelMemberNum_,_I",
    "DelMemberNum01_,_DelMemberNum"
)
endic_DS["DelMemberNum"] = [
    "UID_,_Q"
]

dedic_DS[0x00180038] = (
    "RspCode_,_I",
    "GID_,_Q",
    "MemberListVer_,_I",
    "DelMemberNum_,_I_count",
    "DelMemberNum02_,_DelMemberNum"
)
dedic_DS["DelMemberNum"] = [
    "UID_,_Q"
]

# 14删除群组成员通知
dedic_DS[0x00180039] = (
    "AdminUID_,_Q",
    "GID_,_Q",
    "MemberListVer_,_I",
    "MemberNum_,_I_count",
    "MemberNum04_,_MemberNum14"
)
dedic_DS["MemberNum14"] = (
    "UID_,_Q",
    "NickName_,_str"
)
# 15群组成员在线状态变更通知
dedic_DS[0x0018003a] = (
    "GID_,_Q",
    "UID_,_Q",
    "Status_,_c"
)
# 管理员下发自定义消息
endic_DS[0x0018003F] = (
    "GID_,_Q",
    "SourceUID_,_Q",
    "Sequence_,_I",
    "Type_,_c",
    "Option_,_str",
    "ChatMsg_,_str"
)
dedic_DS[0x0018003F] = (
    "GID_,_Q",
    "Sequence_,_I",
    "Status_,_c",
    "MsgID_,_Q",
    "SendTime_,_I"
)
# 16发送聊天消息
endic_DS[0x00180040] = (
    "GID_,_Q",
    "Sequence_,_I",
    "SendTime_,_I",
    "Type_,_c",
    "Option_,_str",
    "ChatMsg_,_str"
)
# 17发送聊天消息回执
dedic_DS[0x00180041] = (
    "GID_,_Q",
    "Sequence_,_I",
    "Status_,_c",
    "MsgID_,_Q",
    "SendTime_,_I",
)
# 18下发聊天消息
dedic_DS[0x00180042] = (
    "GID_,_Q",
    "MsgID_,_Q",
    "SourceUID_,_Q",
    "SendTime_,_I",
    "Type_,_c",
    "Option_,_str",
    "ChatMsg_,_str"
)
# 19下发聊天消息回执
endic_DS[0x00180043] = (
    "GID_,_Q",
    "MsgID_,_Q"
)
# 20下发离线聊天消息
dedic_DS[0x00180044] = (
    "GID_,_Q",
    "MsgNum_,_I_count",
    "MsgNumber_,_OfflineMsgNum"
)
dedic_DS["OfflineMsgNum"] = (
    "MsgID_,_Q",
    "SourceUID_,_Q",
    "SendTime_,_I",
    "Type_,_c",
    "Option_,_str",
    "ChatMsg_,_str"
)
# 获取聊天消息记录
endic_DS[0x00180045] = (
    "GID_,_Q",
    "Direction_,_c",
    "BeginMsgID_,_Q",
    "MsgNum_,_I"
)
dedic_DS[0x00180045] = (
    "GID_,_Q",
    "Direction_,_c",
    "BeginMsgID_,_Q",
    "MsgNum_,_I_count",
    "MsgNumbers_,_MsgNum"
)
dedic_DS["MsgNum"] = (
    "MsgID_,_Q",
    "SourceUID_,_Q",
    "SendTime_,_I",
    "Type_,_c",
    "Option_,_str",
    "ChatMsg_,_str"
)
# 发送进入群日志
endic_DS[0x00180050] = (
    "GID_,_Q",
)
# 发送离开群日志
endic_DS[0x00180051] = (
    "GID_,_Q",
)
# 添加群聊天消息敏感词
endic_DS[0x00180055] = (
    "WordNum_,_I",
    "Word_,_str*"
)
dedic_DS[0x00180055] = (
    "RspCode_,_I",
    "WordNum_,_I"
)
# 删除群聊天消息敏感词
endic_DS[0x00180056] = (
    "WordNum_,_I",
    "Word_,_str*"
)
dedic_DS[0x00180056] = (
    "RspCode_,_I",
    "WordNum_,_I"
)
# 清空群聊天消息敏感词
dedic_DS[0x00180057] = (
    "RspCode_,_I",
)
# 获取第三方SDK Token
endic_DS[0x001F0010] = (
    "SDKType_,_c",
    "UID_,_str",
    "ExtContent_,_str"
)
dedic_DS[0x001F0010] = (
    "RspCode_,_I",
    "SDKType_,_c",
    "UID_,_str",
    "TokenLen_,_H",
    #"Token_,_c*"  # 这个解不出来……+_+
)

#发送教室通用Notice
endic_DS[0x001300F0] = (
    "CID_,_Q",
    "Notice_,_str",
    "TargetUIDNum_,_H",
    "TargeUID_,_Q*"
    )
dedic_DS[0x001300F0] = (
    "RspCode_,_I",
    "CID_,_Q",
    "Notice_,_str",
    "TargetUIDNum_,_H_count",
    "TargetUIDs_,_TargetUIDArray"
    )
dedic_DS["TargetUIDArray"] = (
    "TargetUID_,_Q",
    )

#下发教室通用Notice
dedic_DS[0x001300F1] = (
    "CID_,_Q",
    "SourceUID_,_Q",
    "Notice_,_str"
    )

#添加教室通用Storage
endic_DS[0x001300F3] = (
    "CID_,_Q",
    "ItemNum_,_H",
    "Items_,_ItemList"
    )
endic_DS["ItemList"] = (
    "Key_,_str",
    "Value_,_str"
    )
dedic_DS[0x001300F3] = (
    "RspCode_,_I",
    "CID_,_Q",
    "ItemNum_,_H_count",
    "Items_,_ItemList"
    )
dedic_DS["ItemList"] = endic_DS["ItemList"]

#删除教室通用Storage
endic_DS[0x001300F4] = (
    "CID_,_Q",
    "KeyNum_,_H",
    "Keys_,_KeyList"
    )
endic_DS["KeyList"] = (
    "Key_,_str",
    )
dedic_DS[0x001300F4] = (
    "RspCode_,_I",
    "CID_,_Q",
    "KeyNum_,_H_count",
    "Keys_,_KeyList"
    )
dedic_DS["KeyList"] = endic_DS["KeyList"]

#获取教室通用Storage
endic_DS[0x001300F5] = (
    "CID_,_Q",
    "KeyNum_,_H",
    "Keys_,_KeyList"
    )

dedic_DS[0x001300F5] = (
    "RspCode_,_I",
    "CID_,_Q",
    "ItemNum_,_H_count",
    "Items_,_NewItemList"
    )
dedic_DS["NewItemList"] = (
    "Key_,_str",
    "Value_,_str",
    "OwnerUID_,_Q"
    )

#下发教室ConsistentStorage通知
dedic_DS[0x001300F8] = (
    "CID_,_Q",
    "Operate_,_c",
    "ItemNum_,_H_count",
    "Items_,_NewItemList"
    )

#添加教室通用ConsistentStorage
endic_DS[0x001300F9] = (
    "CID_,_Q",
    "ItemNum_,_H",
    "Items_,_ItemList"
    )

dedic_DS[0x001300F9] = (
    "RspCode_,_I",
    "CID_,_Q",
    "ItemNum_,_H_count",
    "Items_,_ItemList"
    )

#删除教室通用ConsistentStorage
endic_DS[0x001300FA] = (
    "CID_,_Q",
    "KeyNum_,_H",
    "Keys_,_KeyList"
    )

dedic_DS[0x001300FA] = (
    "RspCode_,_I",
    "CID_,_Q",
    "KeyNum_,_H_count",
    "Keys_,_KeyList",
    )

#获取教室通用ConsistentStorage
endic_DS[0x001300FB] = (
    "CID_,_Q",
    "KeyNum_,_H",
    "Keys_,_KeyList"
    )

dedic_DS[0x001300FB] = dedic_DS[0x001300F8]

#获取画笔颜色:0x0013015C
endic_DS[0x0013015B] = (
    "CID_,_Q",
    )
dedic_DS[0x0013015B] = (
    "RspCode_,_I",
    "CID_,_Q",
    "Color_,_I"
    )

#---新增教材操作数据相关协议   by：尹志鑫 2017-04-10----
#下发教材操作数据通知：0x00130150  
dedic_DS[0x00130150] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "Operate_,_c",
    "OpDataNum_,_H_count",
    "OpDatas_,_OpDataList"
    )   
dedic_DS["OpDataList"] = (
    "ServerSeq_,_I",
    "SourceUID_,_Q",
    "OpStrData_,_str",
    "OpByteDataLen_,_H_count",
    "OpByteDatas_,_OpByteData"
    )
dedic_DS['OpByteData'] = (
    "OpByteData_,_c",
    )

#获取教材指定页的操作数据：0x0013015F
endic_DS[0x0013015F] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "BeginSeq_,_I"
    )

#添加教材操作数据：0x00130151
endic_DS[0x00130151] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H",
    "OpDatas_,_AddDataList"
    )
endic_DS["AddDataList"] = (
    "ClientSeq_,_I",
    "OpStrData_,_str",
    "OpByteDataLen_,_H",
    "OpByteData_,_c*"
    )

dedic_DS[0x00130151] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H_count",
    "OpDatas_,_AddDataList"
    )
dedic_DS["AddDataList"] = (
    "ServerSeq_,_I",
    "ClientSeq_,_I",
    "OpStrData_,_str",
    "OpByteDataLen_,_H_count",
    "OpByteDatas_,_OpByteData"
    )

#删除教材操作数据：0x00130152
endic_DS[0x00130152] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H",
    "OpDataServerSeq_,_I*"
    )
dedic_DS[0x00130152] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H_count",
    "OpDataServerSeq_,_OpDataServerSeq"
    )
dedic_DS["OpDataServerSeq"] = (
    "OpDataServerSeq_,_I",
    )

#编辑教材操作数据：0x00130153
endic_DS[0x00130153] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H",
    "OpDatas_,_ModiDataList"
    )
endic_DS["ModiDataList"] = (
    "ClientSeq_,_I",
    "OpStrData_,_str",
    "OpByteDataLen_,_H",
    "OpByteData_,_c*"
    )
dedic_DS[0x00130153] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H",
    "OpDataNum_,_H_count",
    "OpDatas_,_ModiDataList"
    )
dedic_DS["ModiDataList"] = (
    "ServerSeq_,_I",
    #"ClientSeq_,_I",
    "OpStrData_,_str",
    "OpByteDataLen_,_H_count",
    "OpByteDatas_,_OpByteData"
    )


#清空教材操作数据：0x00130154
endic_DS[0x00130154] = (
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H"
    )
dedic_DS[0x00130154] = (
    "RspCode_,_I",
    "CID_,_Q",
    "TextbookID_,_H",
    "TextbookType_,_c",
    "Page_,_H"
    )

#H5Debug发送消息：0x00110130
endic_DS[0x00110130] = (
    "Type_,_B",
    "UserIDNum_,_I",
    "VecUserID_,_Q*",
    "LogMessage_,_str",
    "Reserved_,_I"
    )
dedic_DS[0x00110130] = (
    "RspCode_,_I",
    )

#H5Debug发送消息通知：0x00110131
dedic_DS[0x00110131] = (
    "Type_,_B",
    "LogMessage_,_str",
    "SendID_,_Q",
    "Reserved_,_I"
    )

#H5Debug反馈消息：0x00110133
endic_DS[0x00110133] = (
    "Type_,_B",
    "UserID_,_Q",
    "LogMessage_,_str",
    "Reserved_,_I"
    )
dedic_DS[0x00110133] = (
    "RspCode_,_I",
    )

#H5Debug反馈消息通知：0x00110134
dedic_DS[0x00110134] = (
    "Type_,_B",
    "LogMessage_,_str",
    "SendID_,_Q",
    "Reserved_,_I"
    )

# 请求发布通用用户push消息给客户端
endic_DS[0x0019004E] = (
    "MsgID_,_Q",
    "TargetUIDNum_,_H",
    "TargetUIDs_,_Q*"
)
endic_DS["TargetUIDArray"] = (
    "TargetUID_,_Q",
)
# 请求发布通用用户push消息给客户端回应
dedic_DS[0x0019004F] = (
    "RspCode_,_I",
    "MsgID_,_Q"
)
# 请求发布通用用户push消息
endic_DS[0x00190050] = (
    "MsgID_,_Q",
    "BeginTime_,_Q",
    "EndTime_,_Q",
    "Content_,_str",
    "Ext_,_str"
)
# 请求发布通用用户push消息回应
dedic_DS[0x00190051] = (
    "RspCode_,_I",
    "MsgID_,_Q",
    "Ext_,_str"
)
# 请求编辑已经发布的通用用户push消息
endic_DS[0x00190052] = (
    "MsgID_,_Q",
    "BeginTime_,_Q",
    "EndTime_,_Q",
    "Content_,_str",
    "Ext_,_str"
)
# 请求编辑已经发布的通用用户push消息回应
dedic_DS[0x00190053] = (
    "RspCode_,_I",
    "MsgID_,_Q",
    "Ext_,_str"
)
# 请求删除已经发布的通用用户push消息
endic_DS[0x00190054] = (
    "MsgIDNum_,_c",
    "MsgIDs_,_MsgID"
)
endic_DS['MsgID'] = (
    "MsgID_,_Q"
)
# 请求删除已经发布的通用用户push消息回应
endic_DS[0x00190055] = (
    "RspCode_,_I",
    "MsgIDNum_,_c",
    "MsgIDs_,_MsgID"
)
#下发通用用户push消息
dedic_DS[0x00190056] = (
    "HasMoreMsg_,_c",
    "MsgNum_,_c_count",
    "MsgList_,_PushMsg",
    "Reserved_,_str"
)
dedic_DS['PushMsg'] = (
    "MsgSeq_,_Q",
    "MsgID_,_Q",
    "BeginTime_,_Q",
    "EndTime_,_Q",
    "Content_,_str",
    "Ext_,_str"
)

#向服务端上报确认已收到的通用用户push消息
endic_DS[0x00190057] = (
    "MsgNum_,_B",
    "MsgSeqList_,_Q*"
)



# 将数据data封装成字节流
def encodePack_DS(cmd, data, fangxiang='>'):
    byts = b''
    if cmd in endic_DS.keys():
        structArr_DS = endic_DS[cmd]  # 获取结构
        # 循环解析结构中的每一个字段
        i = 0
        j = len(structArr_DS)
        while i < j:
            i, t_byts = _writePack_DS(data, structArr_DS, i, fangxiang)
            byts += t_byts
    # 移除结构体的所有键值对
    return byts


def _writePack_DS(data, structArr, i, fangxiang):
    struct_field = structArr[i]
    _ti_DS = struct_field.find("_,_")
    tempByts = b''
    if _ti_DS > -1:
        _key_DS = struct_field[0:_ti_DS]  # 获得变量名
        _tf_DS = struct_field[_ti_DS + 3:]  # 获得解析方法的标识
        _tf_DS = _tf_DS.replace(' ', '')
        if len(_tf_DS) == 1:
            # 简单命令,简单处理
            fmt = fangxiang + _tf_DS
            tempByts += struct.pack(fmt, data[_key_DS])
            i += 1
        elif len(_tf_DS) == 2 and _tf_DS[1] == "*":
            # 基元数据类型数组
            for o in data[_key_DS]:
                tempByts += struct.pack(fangxiang + _tf_DS[0], o)
            i += 1
        else:
            if _tf_DS == 'str':
                # utf8字符串
                fangxiang += 'i%dsc'
                fangxiang = fangxiang % len(data[_key_DS])
                tempByts += struct.pack(fangxiang,
                                        len(data[_key_DS]) + 1, data[_key_DS], b'\0')
                i += 1
            # 20161125 add by yuyong_id：增加字符串元类数据类型的解析
            # ==============================================
            elif _tf_DS == 'str*':
                # utf8字符串数组
                fangxiang += 'i%dsc'
                for o in data[_key_DS]:
                    tempByts += struct.pack(fangxiang %
                                            len(o), len(o) + 1, o, b'\0')
                i += 1
            # ==============================================
            elif _tf_DS in endic_DS.keys():
                # 循环写入对象数组
                for o in data[_key_DS]:
                    tempByts += encodePack_DS(_tf_DS, o, fangxiang)
                i += 1
            else:
                raise Exception('无效的结构命令字符串%s,%s' % (_tf_DS, _key_DS))
    else:
        raise Exception('jiegouticuowu:%s' % struct_field)
    return i, tempByts


# 将字节流读成数据data,连同位移_tempPosition_DS，一同返回
@lru_cache(maxsize=2048)
def decodePack_DS(cmd, byts, fangxiang='>', _tempPosition_DS=0):
    # data = None
    # if cmd in dedic_DS.keys():
    data = {}
    if isinstance(cmd, Enum):
        cmd = cmd.value
    structArr_DS = dedic_DS[cmd]  # 获取结构
    # 循环解析结构中的每一个字段
    i = 0
    j = len(structArr_DS)
    while i < j:
        i, _tempPosition_DS = _readPack_DS(
            byts, _tempPosition_DS, structArr_DS, i, fangxiang, data)
    # 移除结构体的所有键值对
    return data, _tempPosition_DS


def _readPack_DS(byts, pos, structArr, i, fangxiang, data):
    _ti_DS = structArr[i].find("_,_")
    tpos = 0  # 记录位移
    if _ti_DS > -1:
        _key_DS = structArr[i][0:_ti_DS]  # 获得变量名
        _tf_DS = structArr[i][_ti_DS + 3:]  # 获得解析方法的标识
        _tf_DS = _tf_DS.replace(' ', '')

        #print "_key_DS = ", _key_DS
        #print "_ft_DS = ", _tf_DS
        if len(_tf_DS) == 1:
            # 简单命令,简单处理
            tpos = pos + _get_tf_DSLen(_tf_DS)
            try:
                data[_key_DS] = struct.unpack(fangxiang + _tf_DS, byts[pos:tpos])
            except Exception as err:
                print(err)
                raise TypeError("Invalid unpack value:%s %s %s" % (_tf_DS, pos, tpos))
            data[_key_DS] = data[_key_DS][0]
            i += 1
            pos = tpos
        else:
            if "_count" in _tf_DS:
                # 需要做循环体处理
                _tf_DS = _tf_DS[0:_tf_DS.index("_count")]
                tpos = pos + _get_tf_DSLen(_tf_DS)
                # 获取循环总数
                tcount = struct.unpack(fangxiang + _tf_DS, byts[pos:tpos])
                tcount = tcount[0]
                data[_key_DS] = tcount
                i += 1
                pos = tpos
                # 开始循环
                ti = 0
                _ti_DS = structArr[i].find("_,_")
                _key_DS = structArr[i][0:_ti_DS]  # 获得变量名
                _tf_DS = structArr[i][_ti_DS + 3:]  # 获得解析方法的标识
                _tf_DS = _tf_DS.replace(' ', '')

                data[_key_DS] = []
                tdata = None

                # 当tcount为unit8的数值时，转换正常int，以适应下面比较循环语句
                # Try transform unit8 value into unit16 value
                try:
                    tcount = ord(tcount)
                except TypeError:
                    pass

                while ti < tcount:
                    pos, tdata = _readDataByByts(byts, pos, fangxiang, _tf_DS)
                    data[_key_DS].append(tdata)
                    ti += 1
                i += 1

            elif _tf_DS == 'str':
                # 字符串处理
                pos, tdata = _readDataByByts(byts, pos, fangxiang, _tf_DS)
                data[_key_DS] = tdata
                i += 1
            elif _tf_DS == 'str*':
                # utf8字符串数组
                fangxiang += 'i%dsc'
                for o in data[_key_DS]:
                    tempByts += struct.pack(fangxiang %
                                            len(o), len(o) + 1, o, b'\0')
                i += 1
            else:
                #print _tf_DS,_key_DS
                raise Exception('无效的结构命令字符串%s,%s' % (_tf_DS, _key_DS))
    else:
        raise Exception('结构体定义错误%s' % structArr[i])
    return i, pos


def _get_tf_DSLen(tf):
    if tf.lower() == 'i':
        return 4
    elif tf.lower() == 'c':
        return 1
    elif tf.lower() == 'b':
        return 1
    elif tf.lower() == 'h':
        return 2
    elif tf.lower() == 'q':
        return 8
    else:
        raise Exception('无法确定长度的类型:%s' % tf)


def _readDataByByts(byts, pos, fangxiang, _tf_DS):
    tpos = 0
    data = None
    if _tf_DS == 'str':
        # utf8字符串
        tpos = pos + 4
        tlength = struct.unpack(fangxiang + 'I', byts[pos:tpos])  # 读取字符串长度
        tlength = tlength[0]
        pos = tpos
        fangxiang += '%ds'
        # (tlength-1)是为了去除最后一个字符\0
        fangxiang = fangxiang % (tlength - 1)
        tpos = pos + tlength - 1
        if pos < tpos:
            try:
                data = struct.unpack(fangxiang, byts[pos:tpos])
            except Exception as err:
                print(err)
                data = ""
            data = data[0]
        else:
            data = ''
        pos = tpos + 1
    elif len(_tf_DS) == 1:
        # 简单类型处理
        tpos = pos + _get_tf_DSLen(_tf_DS)
        data = struct.unpack(fangxiang + _tf_DS, byts[pos:tpos])
        data = data[0]
        pos = tpos
    elif _tf_DS in dedic_DS.keys():
        # 读取一个对象
        data, pos = decodePack_DS(_tf_DS, byts, fangxiang, pos)
    #print "sub return", pos, data

    return pos, data
