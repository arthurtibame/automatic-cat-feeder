// Google Sheet settings
var SPREAD_SHEET_ID = "1zAKEXWGmKkwLOwg98hvRhQOgGtXiF_KrX7LUaYgPiag";
var SAVED_TOKEN_SHEET_NUM=1 // token of sheet number
var SAVED_LOGS_SHEET_NUM=2 // logs to be saved in sheet
var SAVED_FILES_SHEET_NUM=3  // logs of saving files in sheet
var SAVED_REGISTED_SHEET_NUM=4
var SAVED_REGISTER_LOGS_SHEET_NUM=5
var sheet = SpreadsheetApp.openById(SPREAD_SHEET_ID).getSheets()[SAVED_TOKEN_SHEET_NUM]; // get sheet object
var CHANNEL_ACCESS_TOKEN = sheet.getSheetValues(1,1,1,1)[0][0]; // Line channel access token
var REGISTER_ACCESS_TOKEN = sheet.getSheetValues(3,1,1,1)[0][0]; // Line chat access token

// folder name to save your types of file from line
var IMAGES_FOLDER="saved_images"; 
var VIDEOS_FOLDER="saved_videos";
var VOICES_FOLDER="saved_voices";

// Line configs
var replyUrl = 'https://api.line.me/v2/bot/message/reply';

function debug(e){
  
}

function saveFile(messageId, type) {
  var types = {
    "image": {
      "extension": ".jpg",
      "folder": IMAGES_FOLDER
    },
    "video": {
      "extension": ".mp4",
      "folder": VIDEOS_FOLDER
    },
    "audio": {
      "extension": ".mp3",
      "folder": VOICES_FOLDER
    }      
  }
  
  var url= "https://api.line.me/v2/bot/message/" + messageId + "/content";
  var response = UrlFetchApp.fetch(url, {
        'headers': {      
          'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
        },
        'method': 'get'
  }).getBlob()          
  var folder = DriveApp.getFoldersByName(types[type]["folder"]).next(); 
  
  //  if not exists folder create
  if (folder.getFoldersByName(now_date()).hasNext() === false) {
    var subfolder =  folder.createFolder(now_date());  
    
  } else {
    var subfolder =  folder.getFoldersByName(now_date()).next()
    
  }
  
  var result = subfolder.createFile(response).setName(messageId + types[type]["extension"]);
  writeSheet(data=[type, folder, subfolder, result, url], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_FILES_SHEET_NUM)
  
}



function doPost(e) {   
  var events = JSON.parse(e.postData.contents).events[0];
  var userId = events.source.userId;
  var userMessage = events.message.text;
  try {
    var userMessageArray = userMessage.split(" ");
  } catch (e) {
    var userMessageArray = "";
  }
  var replyToken = events.replyToken;
  writeSheet(data=[e.postData.contents], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_LOGS_SHEET_NUM);
  if (checkUser(userId) == true && userMessage != "register") {
    
    
    // 取出 replayToken 和發送的訊息文字
    
    var messageType = events.message.type;
    var messageId = events.message.id;
    var userMessage = events.message.text;
    
    if (typeof replyToken === 'undefined') {
      return;
    }
    
    if (events.type == "follow") {
      writeSheet(data=[events.source.userId], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_REGISTED_SHEET_NUM);
      textReply(replyToken, "hello please register to use it")
    }
    
    if (messageType === 'image' || messageType === 'video' || messageType === 'audio') {
      saveFile(messageId, messageType)
    }
    
    textReply(replyToken, userMessage)
  
  } else if (userMessageArray.includes("register")){
    if (registerUser(userId=userId, password=userMessageArray[1]) == true){
      textReply(replyToken, "Successfully register !")
    } else {
      textReply(replyToken, "Wrong password ! \nPlease to contact to Administrator")
    }
    
  
  } else {
    textReply(replyToken, "Please to contact to Administrator")
  }
}



function textReply(replyToken, message) {
  var response = UrlFetchApp.fetch(replyUrl, {
    'headers': {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
    },
    'method': 'post',
    'payload': JSON.stringify({
      'replyToken': replyToken,
      'messages': [{
        'type': 'text',
        'text': message+' ( google )',
      }],
    }),
  });
  Logger.log(response)

}

function writeSheet(data=now_datetime(), spread_sheet_id=SPREAD_SHEET_ID, sheet_num=2){
  var Sheet = SpreadsheetApp.openById(spread_sheet_id).getSheets()[sheet_num];
  //  insert latest data before second row
  //  In this case the header will not be changed   
  Sheet.insertRowBefore(2);

  if (sheet_num!=SAVED_TOKEN_SHEET_NUM &&  data[0]!=now_datetime()){
    // unshift (in python append) to the first position of array
    data.unshift(now_datetime());
  } 
  
  data.forEach(function(e,i){
  Sheet.getRange(2, i+1).setValue(e);
  }); 
  return ContentService.createTextOutput(true);  
}

function registerUser(userId, password){
  var decode = Utilities.base64DecodeWebSafe(REGISTER_ACCESS_TOKEN, Utilities.Charset.UTF_8);
  var accepted_password = Utilities.newBlob(decode).getDataAsString()
  if (password==accepted_password) {
    writeSheet([userId], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_REGISTED_SHEET_NUM)
    writeSheet([userId, 1], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_REGISTER_LOGS_SHEET_NUM)    
    return true
  } else {
    writeSheet([userId, 0], spread_sheet_id=SPREAD_SHEET_ID, sheet_num=SAVED_REGISTER_LOGS_SHEET_NUM)
    return false
  }
}

function checkUser(userId) {
  var sheet = SpreadsheetApp.openById(SPREAD_SHEET_ID).getSheets()[SAVED_REGISTED_SHEET_NUM]; // get sheet object
  var userIds = flattenArray(sheet.getSheetValues(2,2,sheet.getLastRow(),1));  
  return userIds.includes(userId)
}

function flattenArray(arrayOfArrays){
  return [].concat.apply([], arrayOfArrays);
}

function now_datetime() {
  var date = new Date();
  var dd = String(date.getDate()).padStart(2, '0');
  var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = date.getFullYear();  
  var now_datetime = yyyy +"-" + mm + '-' + dd + " " + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() ;//+ ',';
  return now_datetime
}

function now_date() {
  var date = new Date();
  var dd = String(date.getDate()).padStart(2, '0');
  var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = date.getFullYear();  
  var date = yyyy+mm+dd;
  return date
}