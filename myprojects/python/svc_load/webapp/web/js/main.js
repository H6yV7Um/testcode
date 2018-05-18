$(document).ready(function () {
    getProfile();
    //add format function for string
    String.prototype.format = function(args) {
        var result = this;
        if (arguments.length > 0) {
            if (arguments.length == 1 && typeof (args) == "object") {
                for (var key in args) {
                    if(args[key]!=undefined){
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            }
            else {
                for (var i = 0; i < arguments.length; i++) {
                    if (arguments[i] != undefined) {
                        var reg= new RegExp("({)" + i + "(})", "g");
                        result = result.replace(reg, arguments[i]);
                    }
                }
            }
        }
        return result;
    }

//-------------------------validate password--------------------
$("#password_form").formValidation({
    button: {
        selector: '#sub_pwd_btn',
        disabled: 'disabled'
    },
    // excluded: [':disabled', ':hidden', ':not(:visible)'],
    exculded: ':disabled',
    live: "disabled",
    icon: CONSTANT.VALIDATE_OPTION.icon,
    fields: {
        password1: {
            validators: {
                notEmpty: {
                    message: '密码不能为空'
                }
            }
        },
        password2: {
            validators: {
                notEmpty: {
                    message: '密码不能为空'
                },
                identical: {
                    field: 'password1',
                    message: '两次输入的密码不一致'
                }
            }
        }
    }
})
.on('err.form.fv', function(e, data) {
    e.preventDefault();
})
.on('success.form.fv', function(e, data) {
    commitChange();
    e.preventDefault();
});

//-------------------------left navigator-------------------------
$("#left-nav li[data-url]").click(function(){
    clearInterval(TIMER);
    $("#left-nav li").each(function(){
        $(this).removeClass('active');
    });
    $(this).addClass('active')
    var url = $(this).data('url');
    if(url){
        loadPage(url);
    }
})

//----------------get profile--------------------
function getProfile(){
    var username;
    $.ajax({
        type: "GET",
        url: CONSTANT.URL.SVC.GET_USER_PROFILE,
        dataType: "json",
        success: function(response) {
            var data = response.data
            if(response.status == 1){
                username = data.name
                if(!!!data.is_super){
                    $("#svc_admin").remove();
                    switch (data.group) {
                        case "dev":
                            $("#test_group").remove();
                            break;
                        case "testgroup":
                            $("#svc").remove();
                            break;
                        default:
                            $("#left-nav").empty();
                            $("#sub-page").html("<h1><strong>无任何权限，请联系管理员！</strong></h1>");
                            break;
                    } 
                }
                $("#left-nav").show();
                $("#left-nav ul:eq(0) li:eq(1)").trigger('click');
            }
            else {
                username = '未登录';
            }
            $("#user_name").html(username);
        }
    });
}


//--------------user logout-----------------
$("#logout").click(function(){
    $.ajax({
        type: "GET",
        url: CONSTANT.URL.SVC.USER_LOGOUT,
        dataType: "json",
        success: function(response) {
                window.location.href = response.msg
        }
    })
})

$("#pwdModal").on('hide.bs.modal', function(){
    resetModal();
});

function commitChange(){
    $.ajax({
        type: "POST",
        url: CONSTANT.URL.SVC.CHANGE_PASSWORD,
        data: $("#password-form").serialize(),
        dataType: "json",
        success: function(response) {
            $("#pwdModal").modal("hide");
        }
    })
}

function resetModal(){
    $("input[type='password']").val('');
    $("#password_form").formValidation('resetForm', true);
}

function loadPage(url){
    $("#sub-page").html();
    if(url == 'locust'){
        $.ajax({
            type: "GET",
            url: CONSTANT.URL.SVC.GET_LOCUST_MASTER_URL,
            timeout: 3000,
            dataType: "json",
            datafilter: function(data, type){},
            success: function(response) {
                if(response.status !='1'){
                    alert("请先启动locust master！");
                    $('#operation').trigger('click');
                }
                else{
                    var locust_ip = response.data.locust_master;
                    var locust_page = '<iframe id="locust" name="locust" src="http://' + locust_ip + ':8089" style="overflow:visible;min-height:800px;" scrolling="yes" frameborder="no" height="100%" width="100%"></iframe>'
                    $("#sub-page").html(locust_page);
                }
            },
        });
    }
    else if(url == 'service_mgr'){
        var service_mgr_page = '<iframe id="service_mgr" name="service_mgr" src="http://172.16.16.72:5000" style="overflow:visible;min-height:800px;" scrolling="yes" frameborder="no" height="100%" width="100%"></iframe>'
        $("#sub-page").html(service_mgr_page);
    }
    else{
        url = 'html/' + url;
        $.ajax({
            type: "GET",
            url: url,
            dataType: "html",
            success: function(data) {
                $("#sub-page").html(data);
            }
        });
    }
}


});

function request(url, method, data){
    //创建loading元素
    var target = document.createElement("div");
    document.body.appendChild(target);
    var spinner = new Spinner(CONSTANT.SPIN.opts).spin(target);
    var overlay = iosOverlay({
        text: "Loading",
        spinner: spinner
    });
    $.ajax({
        type: method,
        url: url,
        data: data,
        dataType: "json",
        success: function (response) {
            if(response.status == 1){
                overlay.update({
                    icon: "img/check.png",
                    text: "Success",
                    duration: 2000
                });
                setTimeout(function() {
                    overlay.hide();
                }, 2000);
            }
            else{
                overlay.update({
                    icon: "img/cross.png",
                    text: response.msg,
                    duration: 2000 
                });
                setTimeout(function() {
                    overlay.hide();
                }, 2000);
            }
            document.body.removeChild(target);
        },
        error: function(response){
            overlay.hide();
            document.body.removeChild(target);
            $('#errorModal div.modal-body').text("internal error!");
            $('#errorModal').modal({
                keyboard: true
            });
        }
    });
    return false;
}

