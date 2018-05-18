package com.vdcoding.modules.superman.oauth2;

import com.google.gson.Gson;
import com.vdcoding.common.utils.R;
import com.vdcoding.modules.superman.common.BaseResponse;

import org.apache.commons.lang.StringUtils;
import org.apache.http.HttpStatus;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.AuthenticationToken;
import org.apache.shiro.authc.UnknownAccountException;
import org.apache.shiro.web.filter.authc.AuthenticatingFilter;

import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * 认证过滤器，用来从请求中获取被认证的字段，比如token或loginCode
 *
 * @author yinzhixin
 */
public class WepyOAuth2Filter extends AuthenticatingFilter {

    @Override
    protected AuthenticationToken createToken(ServletRequest request, ServletResponse response) throws Exception {
        String token = getRequestToken((HttpServletRequest) request);

        if(StringUtils.isBlank(token)){
            return null;
        }

        return new WepyToken(token);
    }

    @Override
    protected boolean isAccessAllowed(ServletRequest request, ServletResponse response, Object mappedValue) {
        return false;
    }

    @Override
    protected boolean onAccessDenied(ServletRequest request, ServletResponse response) throws Exception {
        //如果loginCode不存在，直接返回401
        String token = getRequestToken((HttpServletRequest) request);
        if(StringUtils.isBlank(token)){
            HttpServletResponse httpResponse = (HttpServletResponse) response;
            httpResponse.setContentType("application/json;charset=utf-8");
            String json = new Gson().toJson(new BaseResponse(HttpStatus.SC_UNAUTHORIZED, "invalid token"));
            httpResponse.getWriter().print(json);

            return false;
        }

        return executeLogin(request, response);
    }

    @Override
    protected boolean onLoginFailure(AuthenticationToken token, AuthenticationException e, ServletRequest request, ServletResponse response) {
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        httpResponse.setContentType("application/json;charset=utf-8");
        try {
            //处理登录失败的异常
    		Throwable throwable = e.getCause() == null ? e : e.getCause();
            R r = R.error(HttpStatus.SC_UNAUTHORIZED, "Invalid token!");
            String json = new Gson().toJson(r);
            httpResponse.getWriter().print(json);
        } catch (IOException e1) {

        }

        return false;
    }

    /**
     * 获取请求的login code
     */
    private String getRequestToken(HttpServletRequest httpRequest){
        //从header中获取loginCode
        String token = httpRequest.getHeader("token");

        //如果header中不存在loginCode，则从参数中获取
        if(StringUtils.isBlank(token)){
        	token = httpRequest.getParameter("token");
        }

        return token;
    }


}
