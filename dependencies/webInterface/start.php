<?php
	header("Content-type:text/html;charset=utf-8");

	$result = system("cd /Applications/ios_detect_py/;
					  /usr/bin/python -c 'import subprocess; subprocess.call(/'/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/bin/python2.7 server.py/')'");
	//echo "<script>window.location='tasklist.php';</script>";
?>
