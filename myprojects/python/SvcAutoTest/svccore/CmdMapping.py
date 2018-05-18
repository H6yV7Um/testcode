from enum import Enum, unique


@unique
class CommandMapping(Enum):
    '''
    服务协议名称与协议号的枚举映射, 服务名称必须与pb文件中定义的类名称一致
    '''
    HeartBeat = 0x00310010  #心跳ping
    HeartBeatRsp = 0x00310011   #心跳pong
    PbLoadBalancing = 0x00300010    #pb负载均衡服务
    PbLoadBalancingRsp = 0x00300011 #pb负载均衡服务响应
    LoadBalancing = 0x00300012  #websocket负载均衡服务
    LoadBalancingRsp = 0x00300013 #websocket负载均衡服务负载均衡响应
    GetHeartBeatConf = 0x00310012   #获取心跳配置
    GetHeartBeatConfRsp = 0x00310013    #获取心跳配置响应
    ClientReportHbConf = 0x00310014     #客户端上报心跳配置
    ClientReportHbConfRsp = 0x00310015  #上报心跳配置响应
    ClientAccess = 0x00310020   #客户端接入
    ClientAccessRsp = 0x00310021    #客户端接入响应
    UserLogin = 0x00310024  #用户账号密码登陆
    UserLoginRsp = 0x00310025   #登陆响应
    GetAnonymousUid = 0x00310026  #获取匿名登录账号
    GetAnonymousUidRsp = 0x00310027   #获取匿名登录账号响应
    AnonymousLogin = 0x00310028 #匿名用户登陆
    AnonymousLoginRsp = 0x00310029  #登陆响应
    LoginComplete = 0x0031002A  #登陆完成请求
    UserLogout = 0x0031002C #用户登出
    UserLogoutRsp = 0x0031002D  #用户登出响应
    TokenLogin = 0x00310030 #用户token登陆
    TokenLoginRsp = 0x00310031  #用户token登陆响应
    UpdateToken = 0x00310032   #通过refresh_token更新token
    UpdateTokenRsp = 0x00310033    #通过refresh_token更新token响应
    UpdateRefreshToken = 0x00310034 #通过refresh token更新refresh token
    UpdateRefreshTokenRsp = 0x00310035  #通过refresh token更新refresh token响应
    EnterClass = 0x00380020 #进入教室
    EnterClassRsp = 0x00380021  #进入教室响应
    EnterClassNotify = 0x00380022   #进入房间通知
    EnterClassComplete = 0x00380023 #进教室完成
    LeaveClass = 0x00380024 #离开教室
    LeaveClassRsp = 0x00380025  #离开教室响应
    LeaveClassNotify = 0x00380026   #离开房间通知
    ForceLeaveClass = 0x00380028    #强制离开教室
    ForceLeaveClassRsp = 0x00380029 #强制离开教室响应
    ForceLeaveClassNotify = 0x0038002A  #强制离开教室通知
    CloseClass = 0x0038002C #关闭房间
    CloseClassRsp = 0x0038002D  #关闭房间响应
    CloseClassNotify = 0x0038002E   #关闭房间通知
    UserSendMessage = 0x00380070    #用户A发送聊天消息
    UserSendMessageRsp = 0x00380071 #用户A发送聊天消息响应
    UserReceiveMessage = 0x00380072 #服务端转发消息给用户B
    UserReceiveMessageRsp = 0x00380073  #用户B收到消息响应
    ReceiveOfflineMessage = 0x00380074  #接收离线消息
    HandUp = 0x00380090 #举手
    HandUpRsp = 0x00380091  #举手响应
    HandDown = 0x00380092   #放手
    HandDownRsp = 0x00380093    #放手响应
    ChangeSpeakOrder = 0x00380094   #修改发言列表
    ChangeSpeakOrderRsp = 0x00380095    #修改发言列表响应
    ChangeSpeakOrderNotify = 0x00380096 #修改发言列表通知


