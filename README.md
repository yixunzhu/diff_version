## 前言

用于对比两个版本之间配置文件变更。

## 一、auto_run_115.py

这个可以不用看，因为已经集成到 Jenkins 上，直接执行就可以了，执行方法如下：

1. 打开构建地址：`http://192.168.3.110/view/push_bugs/job/diff_version/build?delay=0sec`
2. 填写新老版本的 tag 号，如：`base-2.4.3-20230630-1` 和 `base-2.4.3-20230803`
3. 最终对比结果会保存在 `3.115`，`/mnt/backup/安装包/diff` 中整个过程差不多 10 分钟左右，主要看解压的时间。
备注：完成后，会发生通知到测试群中。

## 二、run_localhost.py

这个要看，这个是在自己本地电脑执行的，使用场景：如果 `3.115` 机器太卡太慢或者挂了，无法进行在 `115` 机器上操作时，就要执行这个脚本，执行方法如下：

1. 在自己电脑 `D` 盘新建文件夹 `diff`（其他盘也可以，如果其他盘，则需要修改代码第 13 行，改成自定义盘即可）
2. 代码第 10 行和第 11 行，分别修改要对比的 tag 号，如 `tag_1 = "base-2.4.3-20230630-1"`，`tag_2 = "base-2.4.4-20230803"`
3. 把对比的升级包粘贴到 `D://diff` 中，右键选择解压到 `XXXXXX`（文件夹名称）
4. 如上三部完成后，执行脚本即可出结果