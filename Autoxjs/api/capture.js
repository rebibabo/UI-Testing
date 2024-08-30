if(!requestScreenCapture()) { // 请求截图权限
    toast("请求截图失败！");
    exit();
}
img = captureScreen("/storage/emulated/0/DCIM/Camera/0.png");   // 保存截图到指定路径