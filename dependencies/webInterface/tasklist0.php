<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>任务管理</title>
<!-- <link href="img/favicon.png" rel="shortcut icon" /> -->
<!-- <link href="css/base.css" rel="stylesheet" type="text/css" /> -->
<!-- <link href="css/styleNew.css" rel="stylesheet" type="text/css" /> -->
<link href="css/bootstrap.min.css" rel="stylesheet" />
<script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>
<!-- <script type="text/javascript" src="js/login.js"></script> -->

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
	width:90%;
	margin:50px auto;
	position: relative;
	left:-3%;
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
					<li><a href="applist.php">本机应用列表</a></li>
					<li class='active'><a href="tasklist.php">任务管理</a></li>
			</ul>
			</div>
		</div>
		<div class="mainContent">
			<h4>已下发任务状态列表</h4>
			<table class="table table-bordered table-hover" style="width:100%;">
				<tr><th>序号</th><th>应用名</th><th>下发任务时间</th><th>状态</th><th>检测报告</th></tr>
		

			<?php
			//连接数据库
			class MyDB extends SQLite3
			{
				function __construct()
				{
					$this->open('/Applications/ios_detect_py/task.db');
				}
			}
			$db = new MyDB();
			if(!$db){
				echo $db->lastErrorMsg();
			} else {
				$sql = <<<EOF
					SELECT * FROM ios_app;
EOF;
				$ret = $db->query($sql);
				$j = 1;
				while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
					switch ($row['STATUS']) {
						case 1:
							$echo_row1 = "<tr class='success'>";
							$echo_row3 = "<td>已完成</td>";
							$detect_flag[$j] = 1;
							break;
						case 2:
							$echo_row1 = "<tr class='info'>";
							$echo_row3 = "<td>待检测</td>";
							break;
						case 3:
							$echo_row1 = "<tr class='warning'>";
							$echo_row3 = "<td>正在检测</td>";
							break;
						case 4:
							$echo_row1 = "<tr class='danger'>";
							$echo_row3 = "<td>安装失败</td>";
							break;
						default:
							$echo_row1 = "<tr class='danger'>";
							$echo_row3 = "<td>应用存在未知错误，请重新上传</td>";
					}


					$echo_row2 = "<td>" . $row['APPID'] . "</td><td>"
						. $row['NAME'] . "</td><td>" . date('Y-m-d H:i:s', $row['TIME']) . "</td>";
					$echo_row = $echo_row1.$echo_row2.$echo_row3;
					echo $echo_row;

					if (isset($detect_flag[$j])) {

						echo "<td><button class='btn btn-default'><a href='downloadreport.php?name=" . $row['NAME'] . "&path=" . $row['REPORTPATH'] . "'>下载</a></button></td></tr>";
					}
					else{
						echo "<td>未生成</td></tr>";
					}
					$j++;
				}


				$db->close();

			}
			?>
			</table>

		</div>
	</div>

</body>
</html>