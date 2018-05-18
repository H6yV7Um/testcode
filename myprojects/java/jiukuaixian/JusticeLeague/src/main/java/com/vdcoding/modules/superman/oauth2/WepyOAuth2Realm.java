package com.vdcoding.modules.superman.oauth2;

import org.apache.shiro.authc.*;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.vdcoding.modules.superman.pojos.Customer;
import com.vdcoding.modules.superman.pojos.CustomerToken;
import com.vdcoding.modules.superman.service.CustomerService;
import com.vdcoding.modules.superman.service.CustomerTokenService;


/**
 * wepy认证
 *
 * @author yinzhixin 
 * @date 2018-5-10
 */
@Component
public class WepyOAuth2Realm extends AuthorizingRealm {
    @Autowired
    private CustomerTokenService customerTokenService;
    
    @Autowired
    private CustomerService customerService;

    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof WepyToken;
    }

    /**
     * 授权(验证权限时调用)
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {
        return null;
    }

    /**
     * 认证(登录时调用)
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        String accessToken = (String) token.getPrincipal();
        //根据accessToken，查询用户信息
        CustomerToken customerToken = customerTokenService.queryByToken(accessToken);
        //token失效
        if(customerToken == null||customerToken.getExpireTime().getTime() < System.currentTimeMillis()){
//            throw new IncorrectCredentialsException("token失效，请重新登录");
        	//这里最好不要手动抛异常，会被shiro捕获并输出warn级别日志，然后抛出另一个异常信息，所以Fileter中的onLoginFailure会捕获到shiro抛的异常
        	//而不是此处抛的异常。直接返回null比较好一点，避免冗余日志输出
        	return null;
        }

        //查询用户信息
        Customer customer = customerService.getCustomerById(customerToken.getCustomerId());

        SimpleAuthenticationInfo info = new SimpleAuthenticationInfo(customer, accessToken, getName());
        return info;
    }
}
