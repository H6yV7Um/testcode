$(function () {
    $("#jqGrid").jqGrid({
        url: baseURL + 'test/stressFile/list',
        datatype: "json",
        colModel: [			
            { label: '文件ID', name: 'fileId', width: 50, key: true },
			{ label: '用例ID', name: 'caseId', width: 50},
			{ label: '文件名称', name: 'originName', width: 60 },
			{ label: '添加时间', name: 'addTime', width: 80 }
			// 当前不做更新，页面复杂性价比不高。
            // { label: '更新时间', name: 'updateTime', width: 80 }
        ],
		viewrecords: true,
        height: 385,
        rowNum: 10,
		rowList : [10,30,50,100,200],
        rownumbers: true, 
        rownumWidth: 25, 
        autowidth:true,
        multiselect: true,
        pager: "#jqGridPager",
        jsonReader : {
            root: "page.list",
            page: "page.currPage",
            total: "page.totalPage",
            records: "page.totalCount"
        },
        prmNames : {
            page:"page", 
            rows:"limit", 
            order: "order"
        },
        gridComplete:function(){
        	//隐藏grid底部滚动条
        	$("#jqGrid").closest(".ui-jqgrid-bdiv").css({ "overflow-x" : "hidden" }); 
        }
    });
});

var vm = new Vue({
	el:'#rrapp',
	data:{
		q:{
			fileId: null
		}
	},
	methods: {
		query: function () {
			$("#jqGrid").jqGrid('setGridParam',{ 
                postData:{'fileId': vm.q.fileId},
                page:1 
            }).trigger("reloadGrid");
		},
		showError: function(logId) {
			// 目前没有展示文件内容信息的需要。
			$.get(baseURL + "test/stressFile/info/"+fileId, function(r){
				// parent.layer.open({
				//   title:'失败信息',
				//   closeBtn:0,
				//   content: r.log.error
				// });
			});
		},
        del: function () {
            var fileIds = getSelectedRows();
            if (fileIds == null) {
                return;
            }

            confirm('确定要删除选中的记录？', function () {
                $.ajax({
                    type: "POST",
                    url: baseURL + "test/stressFile/delete",
                    contentType: "application/json",
                    data: JSON.stringify(fileIds),
                    success: function (r) {
                        if (r.code == 0) {
                            vm.reload();
                        } else {
                            alert(r.msg);
                        }
                    }
                });
            });
        },
		back: function () {
			history.go(-1);
		},
        reload: function (event) {
            vm.showList = true;
            var page = $("#jqGrid").jqGrid('getGridParam', 'page');
            $("#jqGrid").jqGrid('setGridParam', {
                postData: {'fileId': vm.q.fileId},
                page: page
            }).trigger("reloadGrid");
        }
	}
});

