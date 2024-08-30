if(!requestScreenCapture()) { // 请求截图权限
    toast("请求截图失败！");
    exit();
}
captureScreen("/storage/emulated/0/Pictures/screenshot.jpg")
var template = images.read('/storage/emulated/0/Pictures/like.jpg')
var p = findImage(captureScreen(), template)
if (p) {
    log("find")
} else {
    log("not find")
}