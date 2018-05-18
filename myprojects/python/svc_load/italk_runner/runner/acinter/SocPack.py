# coding:utf-8
import struct
from functools import lru_cache
from Crypto.Cipher import AES
from acinter.DataStruct import encodePack_DS, decodePack_DS
from acinter.Glogger import Glogger
try:
    from aenum import Enum, unique
except ImportError:
    from enum import Enum, unique


class PackEntity:
    def __init__(self, sequenceID, commandID, sourceID, data):
        self.sequenceID = sequenceID  # 包序列号
        self.commandID = commandID  # 包命令
        self.sourceID = sourceID  # 发包用户的ID
        self.data = data  # 数据

# 创建封装消息命令字的枚举类型
# enum of command id that define a message type
@unique
class commandID(Enum):
    LoadBalancing = 0x00100011  # 负载均衡服务
    HeartBeatConfRequest = 0x0011000e  # 获取心跳配置
    HeartBeatConfNotify = 0x11000f  # 心跳配置获取通知
    HeartBeat = 0x00110010  # 客户端心跳
    ClientConnect = 0x00110011  # 客户端接入
    ClientLogin = 0x00110012  # 用户登录
    ClientLogout = 0x00110013  # 用户退出
    ForceClientLogout = 0x00110014  # 强制用户下线
    ClientLoginComplete = 0x00110015  # 用户登录完毕
    ChangeClientStatus = 0x00110016  # 变更个人状态
    EnterClass = 0x00130110  # 请求进入教室
    EnterClass_v3 = 0x00130112  # 请求进入教室v3
    EnterClass_v4 = 0x00130113  # 请求进入教室v4
    EnterClassNotify = 0x00130011  # 进入教室通知
    EnterClassComplete = 0x00130012  # 进入教室完成
    LeaveClass = 0x00130013  # 离开教室
    # LeaveClassNotify = 0x00130014  # 离开教室通知
    # ClassCloseNotify = 0x00130015  # 教室关闭通知
    # AVSDKListChangeNotify = 0x00130116  # 多SDK列表变更通知
    ClassChatMessage = 0x00130016  # 聊天消息
    ChangeTextbookPage = 0x0013001D # 更换教材演示文档的页码
    ClassHandUp = 0x00130120  # 举手请求上麦
    ClassHandDown = 0x00130121  # 请求下麦
    GetWhiteBoardData = 0x00130156  # 获取教材指定页的板书数据
    AddWhiteBoardData = 0x00130157  # 添加教材板书数据
    DeleteWhiteBoardData = 0x00130158  # 删除教材板书数据
    ModifyWhiteBoardData = 0x00130159  # 编辑教材板书数据
    CleanWhiteBoardData = 0x0013015A  # 清空教材板书数据
    GetPenColor = 0x0013015B    #获取画笔颜色
    #新增教材操作数据相关协议   by 尹志鑫 2017-04-10
    GetTextbookPage = 0x0013015F    #获取教材指定页的操作数据
    AddTextbookData = 0x00130151    #添加教材操作数据
    DeleteTextbookData = 0x00130152     #删除教材操作数据
    ModifyTextbookData = 0x00130153     #编辑教材操作数据
    ClearTextbookData = 0x00130154      #清空教材操作数据

    PushParticularMsgReq = 0x0019004E  # 请求发布通用用户push消息给客户端
    PushParticularMsgAck = 0x0019004F  # 请求发布通用用户push消息给客户端回应
    PushPublicMsgReq = 0x00190050  # 请求发布通用用户push消息
    PushPublicMsgAck = 0x00190051  # 请求发布通用用户push消息回应
    PushPubicMsgEdidtReq = 0x00190052  # 请求编辑已经发布的通用用户push消息
    PushPubicMsgEdidtAck = 0x00190053  # 请求编辑已经发布的通用用户push消息回应
    PushPubicMsgDeleteReq = 0x00190054  # 请求删除已经发布的通用用户push消息
    PushPubicMsgDeleteAck = 0x00190055  # 请求删除已经发布的通用用户push消息回应
    PushMsg = 0x00190056  # 下发通用用户push消息
    PushMsgRsp = 0x00190057  # 向服务端上报确认已收到的通用用户push消息
    PushMsgReq = 0x00190058  # 向服务端请求获取其他（更多）的通用用户push消息
    


class SocPack:
    __instance = None  # 单例
    #由于AES128加密的blockzize值为16字节，后续操作需要对被加密文本做填充操作
    #所以blocksize的默认值保持与AES一致，避免使用过程中引发错误
    blockSize = 16
    SocPack_sequence = 1  # 包序号
    head_size = 41  #包头固定长度
    cryptoKey = "{971E1D3A-042B-41da-8E97-181F8073D8E2}"  # AES秘钥
    logger = Glogger.getLogger()

    @classmethod
    def instance(cls):
        # if not cls.__instance:
        #     cls.__instance = SocPack()
        cls.__instance = SocPack()
        return cls.__instance

    # 封装发送包
    @classmethod
    def topackage(cls, data, cmdID, Source=0x00, Target=0x00):
        if data:
            databys = SocPack.instance().encodePro(data, cmdID)  # 封装包体数据
            databys = cls.encrypt(databys, cls.cryptoKey)  # 包体数据加密
        else:
            databys = b''
        result = cls._topackage(databys, cmdID, Source=0x00, Target=0x00)
        return result

    @classmethod
    @lru_cache(maxsize=2048)
    def _topackage(cls, databys, cmdID, Source=0x00, Target=0x00):
        body_size = len(databys)
        pack_size = cls.head_size + body_size
        gformat = ">HIIBIBBBhhQQh%dsB"
        gformat = gformat % (body_size)
        #测试中没有校验包序号，无需自增，同时方便启用缓存
        # cls.SocPack_sequence += 1
        cls.headFlag = 0xEA67
        cls.tailFlag = 0xEB
        result = struct.pack(
            gformat,
            cls.headFlag,
            pack_size,
            cls.SocPack_sequence,
            2,              # 包类型 0x20是（w2c）0x02是（c2s）
            int(cmdID),     # 协议命令字
            0,              # 会话类型 0x00未登陆、 0x01已登陆
            0,              # 信息即时类型0x00即时信息、0x01离线信息
            2,              # 加密方式
            13,             # 公钥序号
            15,             # 超时时长，默认15s
            int(Source),
            int(Target),
            0x00,           # Reserved
            databys,        # 协议数据部分
            cls.tailFlag
        )
        return result

    # 检查数据包
    @classmethod
    def checkPack(cls, byts):
        '''检查数据长度与协议号'''
        blen = len(byts)
        if blen < 41:
            return 0
        head, size = struct.unpack('>HI', byts[0:6])
        if blen < size:
            return 0
        return size

        # 检查包头，包尾部，包长度，是否正常,考虑到性能问题此处跳过
        if blen < size or head != cls.headFlag:
            return 0
        tailFlag = struct.unpack('>B', byts[size - 1:size])[0]
        if tailFlag != cls.tailFlag:
            return 0
        else:
            return size

    # 解析数据包
    @classmethod
    @lru_cache(maxsize=2048)
    def jiemiPack(cls, byts, size):
        # 根据协议定义解包，定义格式。‘%d’前是包头，数据长度为size-41，再加上包尾
        # gformat中的%ds最后被格式化为 比如32s 表达长度为32字节的string
        # 其他格式如 3h 则代表 hhh，所以gformat还以表示为：">H2IcI3c2h2Qh%dsc"
        gformat = ">HIIcIccchhQQh%dsc" % (size - cls.head_size)
        #unpack返回一个元组，每个元素对应gformat中相应的格式
        arr = struct.unpack(gformat, byts)
        # 根据消息内容格式将消息实体化对象
        temppack = PackEntity(
            arr[2], #Sequence包序列号
            arr[4], #协议命令字
            arr[10],    #Source源标识号   
            # data部分结合密钥进行解密计算
            cls.decrypt(arr[13], cls.cryptoKey) #包体数据
        )
        return temppack

    def _pad(self, s):
        '''
        当AES的加密模式为MODE_CBC时，被加密的文本长度必须为blocksize的倍数
        _pad通过简单算法以缺失的长度为值填充s刚好为blocksize的倍数
        '''
        return s + (self.blockSize - len(s) % self.blockSize) * chr(self.blockSize - len(s) % self.blockSize).encode()

    # AES解密截断操作
    def _unpad(self, s):
        if len(s) != 0:
            return s[:-ord(s[len(s) - 1:])]
        else:
            return None

    # aes-256加密
    @classmethod
    def encrypt(cls, message, passphrase):
        #用于加密的key说明:It must be 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes long
        passphrase = passphrase[0:32]
        s = chr(0).encode()
        value = [s for _ in range(16)]
        IV = struct.pack('c'* 16, *value)
        #mode为MODE_CBC时，IV为可选参数，默认为所有位为0的值，如上所示,所以该处不用传IV亦可
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return aes.encrypt(SocPack.instance()._pad(message))

    # aes-256解密
    @classmethod
    def decrypt(cls, message, passphrase):
        passphrase = passphrase[0:32]
        IV = struct.pack('cccccccccccccccc', chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(),
                         chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode(), chr(0).encode())
        aes = AES.new(passphrase, AES.MODE_CBC, IV)
        return SocPack.instance()._unpad(aes.decrypt(message))

    # 封装协议体的入口
    def encodePro(self, data, cmdID):
        # bys = None
        # if cmdID == commandID.ClientLogout:
        #     bys = b''
        # elif cmdID == commandID.ClientLoginComplete:
        #     bys = b''
        # elif cmdID == commandID.HeartBeat:
        #     bys = b''  # 封装  维持长连接的心跳
        # else:
        bys = encodePack_DS(cmdID, data)
        return bys

    def decodePro(self, byts, cmdID):
        packBody = decodePack_DS(cmdID, byts)
        return packBody


if __name__ == '__main__':
    print(commandID(1114130))