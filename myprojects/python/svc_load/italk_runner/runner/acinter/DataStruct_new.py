from construct import *


endic_DS = {}
dedic_DS = {}
head_struct = Struct(
    HeadFlag=Const(Int16ub, 0XEA67),
    PacketSize=Int32ub,
    Sequence=Const(Int32ub, 0),
    PacketType=Const(Int8ub, 2),
    CommandID=Int32ub,
    SessionType=Const(Int8ub, 0),
    OfflineAct=Const(Int8ub, 0),
    CryptType=Const(Int8ub, 2),
    PubKeyIndex=Const(Int16ub, 13),
    Timeout=Const(Int16ub, 15),
    Source=Const(Int64ub, 0),
    Target=Const(Int64ub,0),
    Reserved=Const(Int16ub, 0),
    Body=CString(encoding="utf8"),
    TailFlag=Const(Int8ub, 0XEB)
)

endic_DS[0x00100011] = Struct(
    FailedServerNum=Int32ub,
    ServerIP=Int8ub,
    IsManualSetting=Int8ub,
    ISPIdx=Int32ub,
    LocationCode=Int32ub
)
dedic_DS[0x00100011] = Struct(
    RspCode=Int32ub,
    AccServerIPNum=Int32ub,
    
)