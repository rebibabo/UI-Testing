function in12306() {    // 等待进入12306
    while (true) {
        var node = className("android.widget.FrameLayout").findOnce()
        if (node) {
            if (node.packageName() == "com.MobileTicket") {
                break
            }
            else {
                sleep(1000)
            }
        }
    }
}

in12306()
log("进入12306")
id("h5_title").text("确认订单").waitFor()
log("点击确认订单")
className("android.widget.Button").text("选择乘车人").findOne().click()
text("袁忠升，学生，，证件号，4 3 1 3 ***********5 1 7 ，").findOne().click()
id("cancel").text("购买成人票").findOne().click()
className("android.widget.Button").text("确认 已选1/9人").findOne().click()
sleep(1500)
className("android.widget.Button").text("提交订单").findOne().click()