<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>应用上传</title>
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

li a {
	font-style: '微软雅黑';
	font-size: 15px;
	font-weight: bold;
}

.mainContent{
	width:80%;
	margin:50px auto;
}


</style>
</head>
<body>

	<div class="container">
		<div class="row">
			<div class="span12" style="margin-top: 30px">
				<ul class="nav nav-pills">
					<li class='active'><a href="upload.php">应用上传</a></li>										
					<li><a href="applist.php">本机应用列表</a></li>					
					<li><a href="tasklist.php">任务管理</a></li>				
			</ul>
			</div>
		</div>
		<div class="mainContent" style="width:100%;overflow:hidden;zoom:1;background-color: #dff3f5;">
				<div class="form-group" style="float:left;position:relative;left:80px;top:20px;">
					<div class="blank" style="width:100%;height:30px;"></div>
					<form action="upload.php" method="post" enctype="multipart/form-data">
							<input type="hidden" name="upload_flag" value="1" />
							<input type="hidden" name="upload_time" value="<?php echo mktime(); ?>" />
							<input type="file" name="file" id="file" />
							<br/>
						<div class="blank" style="width:100%;height:0px;"></div>
						<input class="btn btn-primary" type="submit" name="submit" value="上传文件" style=""/>
					</form>
					<div class="info">
						<?php
						class MyDB extends SQLite3{
							function __construct(){
								$this->open('/Applications/ios_detect_py/task.db');
							}
						}

						if(isset($_POST['submit'])) {
							if ($_FILES["file"]["type"] == "application/octet-stream"){
								if ($_FILES["file"]["error"] > 0)
								{
									echo "<br/><p><b>文件上传失败</b></p>";
									echo "错误码(Error): " . $_FILES["file"]["error"] . "<br />";
								}
								else
								{
									//文件大小计算
									$size_b = $_FILES["file"]["size"];
									$size_kb = round($size_b/1024);
									$size_mb = $size_kb/1024;
									if($size_mb >= 1){$size = $size_mb."MB";}
									else {$size = $size_kb."KB";}

									//文件参数存储
									$app_name = $_FILES["file"]["name"];
									$upload_time = $_POST['upload_time'];


									echo "<br/><p><b>文件上传成功</b></p>";
									echo "文件名: " . $_FILES["file"]["name"] . "<br />";
									echo "文件大小: " . $size. "<br />";
									$file_path = './ipa/'.$_FILES["file"]["name"];
									$abs_path = '/Applications/XAMPP/xamppfiles/htdocs/iosDetect/ipa/'.$_FILES["file"]["name"];

									$ipa_tmp = file_get_contents($_FILES["file"]["tmp_name"]);
									file_put_contents($file_path,$ipa_tmp);

									$sql =<<<EOF
										INSERT INTO ios_app (NAME,TIME,PATH,STATUS)
										VALUES ('$app_name',$upload_time,'$abs_path',2);
EOF;
									$db = new MyDB();
									if(!$db){
										echo $db->lastErrorMsg();
									} else {
										$ret = $db->exec($sql);
										if (!$ret) {
											echo '<p>任务入数据库失败，请尝试重新上传...</p><br/>';
											echo $db->lastErrorMsg();
										} else {
											echo "<br/><p><b>文件已生成待检测任务，请到“任务管理”页面查看</b></p><br/>";
										}
									}

								}
							}
							else
							{
								echo "<br/><br/><p><b>请选择.ipa格式的文件上传</b></p><br/>";
								@unlink($_FILES['file']['tmp_name']);

							}
						}

						?>
					</div>
			</div>
			<div class="upload_img" style="float:right;">
				<img src="img/timg845.jpg" alt="">
			</div>


		</div>
	</div>

</body>
</html>
