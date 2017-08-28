
<?php
$app_id = $_GET['id'];

header("Content-type:text/html;charset=utf-8");

function delDirAndFile($dirName)
{
	if ($handle = opendir($dirName)){
		while (false !== ($item = readdir($handle))){
			if ($item != "." && $item != ".."){
				if (is_dir("$dirName/$item")){
					delDirAndFile("$dirName/$item");
				}else{
					if(unlink("$dirName/$item"))
						//echo "成功删除文件： $dirName/$item\n";
						;
				}
			}
		}
	closedir( $handle );
	if(rmdir($dirName))
		echo "成功删除目录： $dirName\n";
	}
}

class MyDB extends SQLite3{
	function __construct(){
    	$this->open('/Applications/ios_detect_py/task.db');
	}
}
$db = new MyDB();
if (!$db) {
		echo $db->lastErrorMsg();
} else {
	$sql = <<<EOF
    	select status, reportpath from ios_app where appid = $app_id;
EOF;
	$row = $db->query($sql);
	$row = $row->fetchArray();
	$status = $row[0];
	$report_path = $row[1];
	//echo $row;
	//echo $status;
	//echo system("whoami");
	$dir = dirname(dirname($report_path));
	//echo $dir;

	if ($status == 3) {
		echo "<script>alert('任务执行中，无法删除');</script>";
	} else {
		$sql = <<<EOF
    	delete from ios_app where appid = $app_id;
EOF;
		$ret = $db->exec($sql);
		if (!$ret) {
			echo "删除失败，请尝试重新下发...\n" . ($db->lastErrorMsg());
			echo "<script>alert('删除失败，请尝试重新下发');</script>";
		} else {
				echo "<script>alert('删除成功');</script>";  
				delDirAndFile($dir);
				   
		}
	}
    
}
$db->close();
echo "<script>window.location='tasklist.php';</script>";

?>

