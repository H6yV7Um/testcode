$(function () {
    $("#jqGrid").jqGrid({
        url: baseURL + 'test/stress/list',
        datatype: "json",
        colModel: [
            {label: '用例ID', name: 'caseId', width: 50, key: true},
            {label: '名称', name: 'caseName', width: 200},
            {label: '项目', name: 'project', width: 80},
            {label: '模块', name: 'module', width: 80},
            {label: '操作人', name: 'operator', width: 80},
            // {label: '备注', name: 'remark', width: 100},
            // { label: 'cron表达式 ', name: 'cronExpression', width: 100 },
            // { label: '备注 ', name: 'remark', width: 100 },
            {
                label: '执行操作', name: '', width: 200, formatter: function (value, options, row) {
                // return value === 0 ?
                //     '<span class="label label-success">未执行</span>' :
                //     '<span class="label label-danger">正在执行</span>';
                var runOnceBtn = "<a href='#' class='btn btn-primary' onclick='runOnce(" + row.caseId + ")' ><i class='fa fa-arrow-circle-right'></i>&nbsp;启动</a>";
                var stopBtn = "<a href='#' class='btn btn-primary' onclick='stop(" + row.caseId + ")' ><i class='fa fa-stop'></i>&nbsp;停止</a>";
                var stopNowBtn = "<a href='#' class='btn btn-primary' onclick='stopNow(" + row.caseId + ")' ><i class='fa fa-times-circle'></i>&nbsp;强制停止</a>";
                return runOnceBtn + '&nbsp;&nbsp;' + stopBtn + '&nbsp;&nbsp;' + stopNowBtn;
                }
            }
        ],
        viewrecords: true,
        height: 385,
        rowNum: 10,
        rowList: [10, 30, 50],
        rownumbers: true,
        rownumWidth: 25,
        autowidth: true,
        multiselect: true,
        pager: "#jqGridPager",
        jsonReader: {
            root: "page.list",
            page: "page.currPage",
            total: "page.totalPage",
            records: "page.totalCount"
        },
        prmNames: {
            page: "page",
            rows: "limit",
            order: "order"
        },
        gridComplete: function () {
            //隐藏grid底部滚动条
            $("#jqGrid").closest(".ui-jqgrid-bdiv").css({"overflow-x": "hidden"});
        }
    });


    new AjaxUpload('#upload', {
        action: baseURL + 'test/stress/upload?token=' + token,
        name: 'file',
        autoSubmit: true,
        responseType: "json",
        onSubmit: function (file, extension) {
            if (!(extension && /^(txt|jmx)$/.test(extension.toLowerCase()))) {
                alert('只支持jmx、txt格式的用例相关文件！');
                return false;
            }
            var caseId = getSelectedRow();
            if (caseId == null) {
                return false;
            }

            this.setData({caseIds: caseId})
        },
        // onChange: function(file, ext){
        //     debugger
        //     if(!(ext && (/^(jmx)$/.test(ext))){
        //         alert("只支持jmx格式的文件！");
        //         return false
        //     }
        // },
        onComplete: function (file, r) {
            if (r.code == 0) {
                // alert(r.url);
                vm.reload();
            } else {
                alert(r.msg);
            }
        }
    });

});

var vm = new Vue({
    el: '#rrapp',
    data: {
        q: {
            caseName: null
        },
        showList: true,
        title: null,
        stressCase: {}
    },
    methods: {
        query: function () {
            if (vm.q.caseName != null) {
                vm.reload();
            }
        },
        add: function () {
            vm.showList = false;
            vm.title = "新增";
            vm.stressCase = {};
        },
        update: function () {
            var caseId = getSelectedRow();
            if (caseId == null) {
                return;
            }

            $.get(baseURL + "test/stress/info/" + caseId, function (r) {
                vm.showList = false;
                vm.title = "修改";
                vm.stressCase = r.stressCase;
            });
        },
        saveOrUpdate: function () {
            if (vm.validator()) {
                return;
            }

            var url = vm.stressCase.caseId == null ? "test/stress/save" : "test/stress/update";
            $.ajax({
                type: "POST",
                url: baseURL + url,
                contentType: "application/json",
                data: JSON.stringify(vm.stressCase),
                success: function (r) {
                    if (r.code === 0) {
                        // alert('操作成功', function(){
                        vm.reload();
                        // });
                    } else {
                        alert(r.msg);
                    }
                }
            });
        },
        del: function () {
            var caseIds = getSelectedRows();
            if (caseIds == null) {
                return;
            }

            confirm('确定要删除选中的记录？', function () {
                $.ajax({
                    type: "POST",
                    url: baseURL + "test/stress/delete",
                    contentType: "application/json",
                    data: JSON.stringify(caseIds),
                    success: function (r) {
                        if (r.code == 0) {
                            alert('操作成功', function () {
                                vm.reload();
                            });
                        } else {
                            alert(r.msg);
                        }
                    }
                });
            });
        },
        reload: function (event) {
            vm.showList = true;
            var page = $("#jqGrid").jqGrid('getGridParam', 'page');
            $("#jqGrid").jqGrid('setGridParam', {
                postData: {'caseName': vm.q.caseName},
                page: page
            }).trigger("reloadGrid");
        },
        validator: function () {
            if (isBlank(vm.stressCase.caseName)) {
                alert("用例名称不能为空");
                return true;
            }

            if (isBlank(vm.stressCase.project)) {
                alert("项目名称不能为空");
                return true;
            }

            if (isBlank(vm.stressCase.module)) {
                alert("模块名称不能为空");
                return true;
            }

            if (isBlank(vm.stressCase.operator)) {
                alert("操作人不能为空");
                return true;
            }
        },
        uploadCase: function () {
            debugger

            var caseId = getSelectedRow();
            if (caseId == null) {
                return;
            }
        }
    }
});

function runOnce(caseIds) {
    if (!caseIds) {
        return;
    }
    confirm('确定要立即执行选中的用例？', function () {
        $.ajax({
            type: "POST",
            url: baseURL + "test/stress/runOnce",
            contentType: "application/json",
            data: JSON.stringify(numberToArray(caseIds)),
            success: function (r) {
                if (r.code == 0) {
                    vm.reload();
                    alert('操作成功', function () {
                    });
                } else {
                    alert(r.msg);
                }
            }
        });
    });
}


function stop(caseIds) {
    if (!caseIds) {
        return;
    }

    confirm('确定要停止执行选中的用例？', function () {
        $.ajax({
            type: "POST",
            url: baseURL + "test/stress/stop",
            contentType: "application/json",
            data: JSON.stringify(numberToArray(caseIds)),
            success: function (r) {
                if (r.code == 0) {
                    alert('操作成功', function () {
                        vm.reload();
                    });
                } else {
                    alert(r.msg);
                }
            }
        });
    });
}

function stopNow(caseIds) {
    if (!caseIds) {
        return;
    }
    confirm('确定要立即停止选中的用例？', function () {
        $.ajax({
            type: "POST",
            url: baseURL + "test/stress/stopNow",
            contentType: "application/json",
            data: JSON.stringify(numberToArray(caseIds)),
            success: function (r) {
                if (r.code == 0) {
                    alert('操作成功', function () {
                        vm.reload();
                    });
                } else {
                    alert(r.msg);
                }
            }
        });
    });
}
