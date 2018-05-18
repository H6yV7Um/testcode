/*常量*/
//全局定时器
var TIMER;

var CONSTANT = {
        DATA_TABLES : {
            DEFAULT_OPTION : { //DataTables初始化选项
                language: {
                    "sProcessing":   "处理中...",
                    "sLengthMenu":   "每页 _MENU_ 项",
                    "sZeroRecords":  "没有匹配结果",
                    "sInfo":         "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
                    "sInfoEmpty":    "当前显示第 0 至 0 项，共 0 项",
                    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                    "sInfoPostFix":  "",
                    "sSearch":       "搜索:",
                    "sUrl":          "",
                    "sEmptyTable":     "表中数据为空",
                    "sLoadingRecords": "载入中...",
                    "sInfoThousands":  ",",
                    "oPaginate": {
                        "sFirst":    "首页",
                        "sPrevious": "上页",
                        "sNext":     "下页",
                        "sLast":     "末页",
                        "sJump":     "跳转"
                    },
                    "oAria": {
                        "sSortAscending":  ": 以升序排列此列",
                        "sSortDescending": ": 以降序排列此列"
                    }
                },
                autoWidth: false,   //禁用自动调整列宽
                stripeClasses: ["odd", "even"],//为奇偶行加上样式，兼容不支持CSS伪类的场合
                order: [],          //取消默认排序查询,否则复选框一列会出现小箭头
                processing: false,  //隐藏加载提示,自行处理
                serverSide: true,   //启用服务器端分页
                searching: true    //禁用原生搜索
            },
            COLUMN: {
                CHECKBOX: { //复选框单元格
                    className: "td-checkbox",
                    orderable: false,
                    width: "30px",
                    data: null,
                    render: function (data, type, row, meta) {
                        return '<input type="checkbox" class="iCheck">';
                    }
                }
            },
            RENDER: {   //常用render可以抽取出来，如日期时间、头像等
                ELLIPSIS: function (data, type, row, meta) {
                    data = data||"";
                    return '<span title="' + data + '">' + data + '</span>';
                }
            }
        },
        SPIN: {
            opts:{
                lines: 13, // The number of lines to draw
                length: 11, // The length of each line
                width: 5, // The line thickness
                radius: 17, // The radius of the inner circle
                corners: 1, // Corner roundness (0..1)
                rotate: 0, // The rotation offset
                color: '#FFF', // #rgb or #rrggbb
                speed: 1, // Rounds per second
                trail: 60, // Afterglow percentage
                shadow: true, // Whether to render a shadow
                hwaccel: true, // Whether to use hardware acceleration
                className: 'spinner', // The CSS class to assign to the spinner
                zIndex: 2e9, // The z-index (defaults to 2000000000)
                top: '28%', // Top position relative to parent in px
                left: 'auto' // Left position relative to parent in px
            }
        },
        URL:{
            SVC:{
                START_HATCH_URL: "/svc/data/start_hatch",
                SLAVE_RESET_URL: "/svc/data/reset",
                OP_NODE_URL: "/svc/deploy",
                CLIENT_LIST_URL: "/svc/clientlist",
                ADD_CLIENT_URL: "/svc/add",
                UPDATE_CLIENT_URL: "/svc/update",
                DELETE_CLIENT_URL: "/svc/delete",
                DATA_STAT_URL: "/svc/data/stats",
                GET_LOCUST_MASTER_URL: "/svc/getlocust",
                GET_TEST_RECORD: "/svc/getrecords",
                GET_USER_PROFILE: "/svc/profile",
                USER_LOGOUT: "/svc/logout",
                CHANGE_PASSWORD: "/svc/change_password",
                FUNC_TEST_RECORD: "/svc/functest/records",
                FUNC_TEST_DETAIL_INFO: "/svc/functest/detail_info",
                FUNC_TEST_CONSOLE: "/svc/functest/console",
                FUNC_TEST_START_BUILD: "/svc/functest/start_build",
                FUNC_TEST_STOP_BUILD: "/svc/functest/stop_build"
            },
            TestGroup: {
                SERVER_LIST_URL: "/testgroup/serverlist",
                ADD_SERVER_URL: "/testgroup/add",
                UPDATE_SERVER_URL: "/testgroup/update",
                DELETE_SERVER_URL: "/testgroup/delete",
            }
            
        },
        SELECT_OPTION: {
            actionsBox: true,
            deselectAllText: "反选全部",
            selectAllText: "选择全部",
            selectedTextFormat: 'count>2',
            countSelectedText: selectedText,
            noneSelectedText: "-请选择-",
            liveSearch: true,
            liveSearchPlaceholder: "搜索",
            width: '153px'
        },
        VALIDATE_OPTION: {
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            }
        },
        MODAL_OPTIONS: {
            CHANGE_PASSWORD: {
                title: "修改密码",
                iconClass: 'icon-chat',
                overlayColor: 'rgba(0, 0, 0, 0.6)',
                overlayClose: true,
                headerColor: '#334c7b',
                iconColor: '#00ffba',
                width: '40%',
                padding: 10
            },
            FUNC_TEST_CONSOLE: {
                title: "Job日志",
                subtitle: 'Jenkins执行自动化用例时的日志',
                iconClass: 'icon-chat',
                overlayColor: 'rgba(255, 255, 255, 0.4)',
                overlayClose: true,
                headerColor: '#334c7b',
                iconColor: '#00ffba',
                // bodyOverflow: true,
                width: '80%',
                padding: 10,
            },
            FUNC_TEST_INFO: {
                title: "信息",
                subtitle: '详细的错误信息',
                iconClass: 'icon-chat',
                overlayColor: 'rgba(255, 255, 255, 0.4)',
                overlayClose: true,
                headerColor: '#334c7b',
                iconColor: '#00ffba',
                // bodyOverflow: true,
                width: '80%',
                padding: 10,
            }
        }
};

function selectedText(cur, total){
    if(cur==total){
        return "已全选" + total + "个"
    }
    else{
        return "已选择" + cur + "个"
    }
}