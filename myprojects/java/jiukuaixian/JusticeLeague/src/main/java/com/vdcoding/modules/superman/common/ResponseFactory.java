package com.vdcoding.modules.superman.common;

import java.util.HashMap;
import java.util.Map;

/**
 * 响应工厂
 */
public class ResponseFactory {
    private static final Map<ResponseType,BaseResponse> responseMap = new HashMap<ResponseType,BaseResponse>();
    
    static {
        responseMap.put(ResponseType.OK, new BaseResponse(0, "ok"));
        responseMap.put(ResponseType.GOODSID_EMPTY, new BaseResponse(401, "商品ID不能为空"));
        responseMap.put(ResponseType.GOODSID_NOT_EXSIT, new BaseResponse(201, "根据传入的商品ID未查到任何数据"));
        responseMap.put(ResponseType.PATH_VARIABLE_ERROR, new BaseResponse(400, "请求参数错误"));
        responseMap.put(ResponseType.SHOP_CLOSED, new BaseResponse(1, "商家还未开始营业"));
        responseMap.put(ResponseType.FEEDBACK_URL_EMPTY, new BaseResponse(301, "callback有误，callback不能为空"));
        responseMap.put(ResponseType.FEEDBACK_URL_NONSTANDARD, new BaseResponse(302, "callback有误，callback不是有效的URL"));
        responseMap.put(ResponseType.CLICK_TIME_FORMAT_ERROR, new BaseResponse(501, "clicktime格式有误"));
    }
    
    public static BaseResponse getResponse(ResponseType responseType) {
        return responseMap.get(responseType);
    }
    
    public static BaseResponse getResponse(String error){
    	return new BaseResponse(500, error);
    }
}
