<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>本机应用列表</title>
<link href="css/bootstrap.min.css" rel="stylesheet" />
<script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>
<script type="text/javascript" src="js/select_applist.js"></script>

<style type="text/css">
html,body {
	margin: 0;
	padding: 0
}

body {
	font-family: 微软雅黑;
}

.STYLE2 {
	font-size: 14px
}

.STYLE3 {
	color: #1d8bd8;
	font-size: 28px;
	font-weight: bold;
}

li a {
	font-style: '微软雅黑';
	font-size: 15px;
	font-weight: bold;
}

.mainContent{
	width:80%;
	margin:50px auto;
}

h4{
    width:100%;
    margin:20px auto;
    text-align: center;
}

</style>
</head>
<body>

	<div class="container">
		<div class="row">
			<div class="span12" style="margin-top: 30px">
				<ul class="nav nav-pills">
					<li><a href="upload.php">应用上传</a></li>
					<li class='active'><a href="applist.php">本机应用列表</a></li>
					<li><a href="tasklist.php">任务管理</a></li>				
			</ul>
			</div>
		</div>
		<div class="mainContent">
            <h4>当前本机已安装应用列表</h4>
			<table class="table table-bordered table-hover">
				<tr><th>应用名称</th><th>选择检测</th></tr>

			<?php
			//逐行读取文件
			$file = fopen("/Applications/ios_detect_py/apps.txt", "r") or exit("无法打开手机应用列表，出现未知错误，请稍后刷新重试...");
			while(!feof($file))
			{
				$filename = fgets($file);
				echo '<tr><td>'.$filename. '</td><input type="hidden" name="appname[]" id="hidden_name"
									value="'.$filename.'" /><td><input type="checkbox" name="applist[]"
											value="'.$filename.'" id="applist"
											onclick="setSelectAll();" /></td>';
			}
			fclose($file);

			?>

			</table>
            <br/>
			<div><input type='checkbox' id="selectAll" onclick="selectAll()" />全选</div>
			</br> </br>
			<button class='btn btn-info' id="app_detect" style="width:20%;position: relative;left:40%;">检测已选中的应用</button>

		</div>
	</div>

</body>
</html>
