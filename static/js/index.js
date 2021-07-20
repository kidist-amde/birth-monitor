
$(document).ready(function () {
    console.log($("#progressbar"))
    $("#progressbar").progressbar({
        value: false,

    });
    $("#progressbar").hide();
    $("#progress-message").hide();
   
    $("#train-progressbar").progressbar({
        value: false,

    });
    $("#train-progressbar").hide();
    $("#loss-section").hide();
    $("#train-progress-message").hide();

    
    console.log("calling ajax")
    $.ajax({
        async: true,
        type: 'GET',
        url: '/sample_tweets',
        success: function (data) {
            console.log("data",data)

            $("#tweet-section div").remove()
            data.tweets.forEach(element => {
                let color = null;
                if (element.label == "positive"){
                    color = "green";

                }else{
                    color = "red"
                }
                $("#tweet-section").append("<p style='width: 50%;color:" +color+";'>" +element.text+"</p>");
            });
            
            
        }
    });
})
function downloadOldTweets() {

    $("#progressbar").show();
    $("#progress-message").show();
    $("#progress-message").text("Downloading old tweets");

    $.ajax({
        async: true,
        type: 'GET',
        url: '/downloadOldTweets',
        success: function (data) {
            console.log("got response")
            $("#progress-message").text(data.msg);
            $("#progressbar").hide();
        }
    });
}


function downloadRecentTweets() {

    $("#progressbar").show();
    $("#progress-message").show();
    $("#progress-message").text("Downloading Recent tweets");

    $.ajax({
        async: true,
        type: 'GET',
        url: '/downloadRecentTweets',
        success: function (data) {
            console.log("got response")
            $("#progress-message").text(data.msg);
            $("#progressbar").hide();
        }
    });
}
function downloadEuroStatData() {

    $("#progressbar").show();
    $("#progress-message").show();
    $("#progress-message").text("Downloading Euro stat data");

    $.ajax({
        async: true,
        type: 'GET',
        url: '/downloadEuroStatData',
        success: function (data) {
            console.log("got response")
            $("#progress-message").text(data.msg);
            $("#progressbar").hide();
        }
    });
}

function callTrainEstimator() {

    $("#train-progressbar").show();
    $("#train-progress-message").show();
    $("#train-progress-message").text("Training estimator... The training might take few minutes.");
    $("#loss-section").hide();
    $.ajax({
        async: true,
        type: 'GET',
        url: '/train_estimator',
        success: function (data) {
            console.log("got response")
            $("#train-progress-message").text(data.msg);
            $("#train-loss").text(data.train_loss);
            $("#test-loss").text(data.test_loss);
            $("#loss-section").show();

            $("#train-progressbar").hide();
        }
    });
}