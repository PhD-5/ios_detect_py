<?php

$put_db = $_POST['put_db'];
$select_app = $_POST['select_appname'];

if(isset($put_db) && $put_db == 1) {

    class MyDB extends SQLite3{
        function __construct(){
            $this->open('/Applications/ios_detect_py/task.db');
        }
    }
    $db = new MyDB();
    if (!$db) {
        echo $db->lastErrorMsg();
    } else {
        $i = 0;
        while ($i < count($select_app)) {
            $time = mktime();
            $sql = <<<EOF
                INSERT INTO ios_app (NAME,TIME,STATUS)
                VALUES ('$select_app[$i]',$time,2);
EOF;
            $ret = $db->exec($sql);
            if (!$ret) {
                echo "$select_app[$i]任务下发失败，请尝试重新下发...\n" . ($db->lastErrorMsg());
            } else {
                    echo "$select_app[$i]\n任务成功下发，请到“任务管理”页面查看\n";       
            }

//            echo $select_app[$i];
            $i++;
        }
    }
    $db->close();
}
?>