<?php
	header("Content-type:text/html;charset=utf-8");
	echo $_SERVER['HTTP_REFERER'];
	$url = "window.location='".$_SERVER['HTTP_REFERER']."';";
	//$url = "window.location='tasklist.php';";
	echo $url;
	//pcntl_signal(SIGCHLD, SIG_IGN);
	$pid = pcntl_fork();
	//父进程和子进程都会执行下面代码  
    if ($pid == -1) {  
        //错误处理：创建子进程失败时返回-1.  
        die('could not fork');  
    } else if ($pid) {  
        //父进程会得到子进程号，所以这里是父进程执行的逻辑  
        //如果不需要阻塞进程，而又想得到子进程的退出状态，则可以注释掉pcntl_wait($status)语句，或写成：  
        //pcntl_wait($status,WNOHANG); //等待子进程中断，防止子进程成为僵尸进程。  
    } else {  
        //子进程得到的$pid为0, 所以这里是子进程执行的逻辑。  
        echo exec("/usr/bin/open /Applications/ios_detect_py/config/para_config.conf")."\n";  
        exit(0) ;  
    }  
	///usr/bin/open /Applications/ios_detect_py/config/para_config.conf
	echo '<script>';
	echo $url;
	echo '</script>';
	
	
?>
