
<?php
$file_name = $_GET['name'];
$file_path = $_GET['path'];

header("Content-type:text/html;charset=utf-8");

//首先要判断给定的文件存在与否
if(!file_exists($file_path)){
    echo "<script>alert('未找到报告文件');</script>";
    echo "<script>window.location='tasklist.php';</script>";
    //Header('Location:tasklist.php');
    return ;
}
// $fp=fopen($file_path,"r");
// $file_size=filesize($file_path);
//下载文件需要用到的头
// Header("Content-type: application/octet-stream");
// Header("Accept-Ranges: bytes");
// Header("Accept-Length:".$file_size);
// Header("Content-Disposition: attachment; filename=".basename($file_path));
// $buffer=1024;
// $file_count=0;
// //向浏览器返回数据
// while(!feof($fp) && $file_count<$file_size){
//     $file_con=fread($fp,$buffer);
//     $file_count+=$buffer;
//     echo $file_con;
// }
// fclose($fp);

// ob_clean();
// ob_end_flush();
// readfile($file_path);

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename='.basename($file_path));
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: public');
header('Content-Length: ' . filesize($file_path));
@ob_end_clean();
readfile($file_path);

echo "<script>alert('下载完成');</script>";
echo "<script>window.location='tasklist.php';</script>";

?>

