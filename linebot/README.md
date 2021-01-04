# Line chatbot on Google App Scripts
## Setting Configuration
```cmd
Environments:
    SPREAD_SHEET_ID: your google sheet id
    
    CHANNEL_ACCESS_TOKEN: Line message api token ( you can save it in your google sheet)

    XXX_SHEET_NUM: the worksheet to save token, logs, logs of save files and so on.
```

## Functions Info.

``` js
function now_date() {
    return String of date
}

function now_datetime(){
    return String of datetime
}

function flattenArray(arrayofArrays){
    return the flatten array if original array is recursive.
} 

function checkuser(userId) {
    //  Check userId whether is in the Google Sheet
    return Boolean
}

function writeSheet(data=Array, spread_sheet_id=String, sheet_num=Number) {
    // write data to Google Sheet
    // if Success return true else false
    return Boolean 
}

function textReply(replyToken=String, message=String) {
    // requests Line textMessage api url with replytoken from Line api,
}

function saveFile(messageId=String, type=String){
    // save file to your Google Drive from user sent to LineBOT
    // image, video and audio
}
function doPost(e) {
    // main controller of this system, 

}    

```