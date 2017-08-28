function selectAll(){
	var obj = document.getElementsByName("applist[]");
	if(document.getElementById("selectAll").checked == false){
		for(var i =0;i<obj.length;i++){
			obj[i].checked=false;
		}
	}
	else{
		for(var i = 0;i<obj.length;i++){
			obj[i].checked = true;
		}
	}
}
//当选中所有的时候，全选按钮会勾上
function setSelectAll(){
	var obj = document.getElementsByName("applist[]");
	var count=obj.length;
	var selectCount = 0;
	
	for(var i =0;i<count;i++){
		if(obj[i].checked == true){
			selectCount ++;
		}
	}
	
	if(count == selectCount){
		document.getElementById("selectAll").checked = true;
	}
	else{
		document.getElementById("selectAll").checked = false;
	}
}


/**
 * 通过ajax实现检测功能
 */
$(document).ready(function(){
	$('#app_detect').click(function(){
		var dis_url = 'app_distribute.php';
		//以下参数均为数组
		var select_appname = new Array();

		var app_name = document.getElementsByName('appname[]');
		var app_list = document.getElementsByName('applist[]');

		for(var i = 0; i<app_list.length;i++){
			if(app_list[i].checked){
				select_appname.push(app_name[i].value);
			}
		}

		if(select_appname.length!=0){
			var response = $.ajax({
				url:dis_url,
				type:"POST",
				// put_db: 1,
				data:{
					put_db: 1,
					select_appname: select_appname
				},
				error:function(){
					alert('通信故障');
				},
				success:function(){
					var response_data = response.responseText;
					alert(response_data);
					window.location='applist.php';
				}
			});
		}
	});
});
