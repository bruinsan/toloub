var numTesters = 7;

// Data limits spreadsheet
var startRowData = 3;  // First row of data to process
var startColData = 1;
var numRowsData = 40;   // Number of rows to process
var numColsData = 100;

// Personal information limits spreadsheet
var startRowPersoInfo = 96;
var startColPersoInfo = 1;
var numRowsPersoInfo = 2;
var numColsPersoInfo = 8;

// messages
var emailTitle = "Sanity today is up to you!"
var msg1 = "Hey good news,";
var msg2 = "You are the Sanity Tester :D";
var testRailLink = "https://aldebaran.testrail.net/index.php?/projects/overview/10"
var mergePortalLink = "http://merge.aldebaran.lan/versions"
var endMsg = "After finishing the Sanity, take the robot back to where you took it and check if it is connected (power supply and Ethernet connection)!"

var currentMonthColumn = 15;     // column August/2016
var today = new Date();
var day = today.getDate();
var currentMonth = today.getMonth() + 1;
var month = new Array();
month[1] = "January";
month[2] = "February";
month[3] = "March";
month[4] = "April";
month[5] = "May";
month[6] = "June";
month[7] = "July";
month[8] = "August";
month[9] = "September";
month[10] = "October";
month[11] = "November";
month[12] = "December";

//
var emailBoss = "jmasgonty@presta.aldebaran-robotics.fr"

/****************** FUNCTION *********************/
function sendEmails() 
{
  var sheet = SpreadsheetApp.getActiveSheet();
  
  // Fetch the range of cells
  var dataRange = sheet.getRange(startRowData, startColData, numRowsData, numColsData)
  var personalInfoRange = sheet.getRange(startRowPersoInfo,startColPersoInfo,numRowsPersoInfo,numColsPersoInfo)
  
  var data = dataRange.getValues();
  var personalInfo = personalInfoRange.getValues();
    
  // reading each line of data spreadsheet
  for (i in data) 
  {    
    var row = data[i];                     // get each row
    var test = row[currentMonthColumn];   // check the date of the row in the spreadsheet 
    var dayTest = test.getDate();
    var monthTest = test.getMonth() + 1;
     
    if(day == dayTest && currentMonth == monthTest)
    {
      var nameTester = row[currentMonthColumn + 1];
      
      // look for the email of the tester
      for (j = 1 ; j < numTesters+1 ; j++)   // go through the lines of the column with names/email
      {
        var test = personalInfo[0][j];
        if (personalInfo[0][j] == nameTester)
        {
          var emailTester = personalInfo[1][j];
          // send email to the tester
          MailApp.sendEmail(emailTester, emailTitle + " " + month[currentMonth] + " " + dayTest, msg1 + " " + nameTester + "! " + msg2 + "\n\nTest Rail link: " + testRailLink + 
                            "\nMerge Portal link: " + mergePortalLink + "\n\nDo you like chocolate?" + "\n\nPS.: " + endMsg, 
                            {
                            noReply: 'true'
                            });
          MailApp.sendEmail(emailBoss, "Sanity tester on " + month[currentMonth] + " " + dayTest , "The Sanity tester today is: " + nameTester,{noReply: 'true'});
        }
      }
    }
    else{/* do nothing */}
    
  }
}
