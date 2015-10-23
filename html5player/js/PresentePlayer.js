document.addEventListener("DOMContentLoaded", function() { initialiseMediaPlayer(); }, false);

// Variables to store handles to various required elements
var biggerPlayer;
var videoScreen;
var videoWebcam;
var playPauseBtn;
var muteBtn;
var progressBar;

function initialiseMediaPlayer() {
	biggerVideo = "screen";
	videoScreen = $("#videoScreen")[0];
	videoScreen.jquery = $("#videoScreen");
	videoWebcam = $("#videoWebcam")[0];
	videoWebcam.jquery = $("#videoWebcam");

	
	// Get handles to each of the buttons and required elements
	playPauseBtn = $("#play-pause-button")[0];
	muteBtn = $("#mute-button")[0];
	progressBar = $("#progress-bar")[0];
	progressBar.width = progressBar.clientWidth;
	progressBar.height = progressBar.clientHeight;
	videoWebcam.currentTime = 2;

	progressBar.addEventListener("click", function(e) {
	    var canvas = document.getElementById('progress-bar');

	    if (!e) {
	        e = window.event;
	    } //get the latest windows event if it isn't set
	    videoScreen.currentTime = videoScreen.duration * (e.offsetX / canvas.clientWidth);
	    videoWebcam.currentTime = 2 + videoWebcam.duration * (e.offsetX / canvas.clientWidth);

	}, true);

	videoScreen.addEventListener('timeupdate', updateProgressBar, false);

	videoScreen.controls = false;
	videoWebcam.controls = false;
	
	// Add a listener for the timeupdate event so we can update the progress bar
	videoScreen.addEventListener('timeupdate', updateProgressBar, false);
	
	// Add a listener for the play and pause events so the buttons state can be updated
	videoScreen.addEventListener('play', function() {
		// Change the button to be a pause button
		changeButtonType(playPauseBtn, 'pause');
	}, false);
	videoScreen.addEventListener('pause', function() {
		// Change the button to be a play button
		changeButtonType(playPauseBtn, 'play');
	}, false);
	
	// need to work on this one more...how to know it's muted?
	videoScreen.addEventListener('volumechange', function(e) { 
		// Update the button to be mute/unmute
		if (videoScreen.muted) changeButtonType(muteBtn, 'unmute');
		else changeButtonType(muteBtn, 'mute');
	}, false);

	loadPois(captureSession["pointsOfInterest"]);
	updateProgressBar();
}

function loadPois(pois) {
	var poisDiv = $("#navigationContainer");

	for (i = 0; i < pois.length; i++) {
		var newDiv = createPoiDiv(pois[i], i);
		poisDiv.append(newDiv);

		newDiv[0].poiTime = pois[i]["begin"];
		newDiv[0].addEventListener("click", function(e) {
	    	videoScreen.currentTime = this.poiTime
	    	videoWebcam.currentTime = this.poiTime +2

			if (videoScreen.paused || videoScreen.ended) {
				// Change the button to be a pause button
				changeButtonType(playPauseBtn, 'pause');
				// Play the media
				videoScreen.play();
				videoWebcam.play();
			}
		}, true);

		if (i == 0) {
			newDiv.focus();
		}
	}
}

function createPoiDiv(poi, index) {
	var newdiv1 = $( "<div id='poi_" + poi["type"] + "_" + index.toString() + "' class='poiContainer'></div>" );
	newdiv1.append( $("<spam>Transição de Slide: " + fromSecondsToTimeString(poi["begin"], false) + "</spam>"))
	newdiv1.append( $("<img src='images/" + poi["slideImage"] + "'></img>)") );
	return newdiv1;

}

function updateProgressBar() {
    //get current time in seconds
    var elapsedTime = videoScreen.currentTime;

    //update the progress bar
    if (progressBar.getContext) {
        var ctx = progressBar.getContext("2d");
        //console.log(progressBar.width, progressBar.height);
        //clear canvas before painting
        ctx.clearRect(0, 0, progressBar.clientWidth, progressBar.clientHeight);
        ctx.fillStyle = "rgb(255,125,0)";
        var fWidth = Math.round((elapsedTime / videoScreen.duration) * progressBar.clientWidth);
        //console.log(fWidth, '/', progressBar.clientWidth);
        
        if (fWidth > 0) {
            ctx.fillRect(0, 0, fWidth,  progressBar.clientHeight);
        }

        var fontSize = 20;
        ctx.font= fontSize + "px Verdana";
		ctx.fillStyle = "white";
		var text = getTimeString(elapsedTime, captureSession["duration"])
		ctx.fillText(text, progressBar.width - 10 - ctx.measureText(text).width, fontSize + (progressBar.height - fontSize)/2);
    }
}

function getTimeString(current, total) {
	var currentStr, totalStr;
	if (total >= 3600) {
		currentStr = fromSecondsToTimeString(current, true);
		totalStr = fromSecondsToTimeString(total, true);
	} else {
		currentStr = fromSecondsToTimeString(current, false);
		totalStr = fromSecondsToTimeString(total, false);
	}

	return currentStr + " / " + totalStr;
}

function fromSecondsToTimeString(totalSec, useHours) {
	var h, m, s, time = "";
	m = Math.floor(totalSec/60);
	s = Math.floor(totalSec%60);
	h = Math.floor(m/60);
	m = m%60;

	if (useHours) {
		time += h.toString() + ":";

		if (m < 10)
			time += "0"
	}

	time += m.toString() + ":"

	if (s < 10)
		time += "0";

	time += s.toString()

	return time;

}

function togglePlayPause() {
	// If the mediaPlayer is currently paused or has ended
	if (videoScreen.paused || videoScreen.ended) {
		// Change the button to be a pause button
		changeButtonType(playPauseBtn, 'pause');
		// Play the media
		videoScreen.play();
		videoWebcam.play();
	}
	// Otherwise it must currently be playing
	else {
		// Change the button to be a play button
		changeButtonType(playPauseBtn, 'play');
		// Pause the media
		videoScreen.pause();
		videoWebcam.pause();
	}
}

// Stop the current media from playing, and return it to the start position
function stopPlayer() {
	videoScreen.pause();
	videoScreen.currentTime = 0;

	videoWebcam.pause();
	videoWebcam.currentTime = 2;
}

// Changes the volume on the media player
function changeVolume(direction) {
	if (direction === '+') {
		videoScreen.volume += videoScreen.volume == 1 ? 0 : 0.1;
		videoWebcam.volume += videoWebcam.volume == 1 ? 0 : 0.1;
	} else {
		videoScreen.volume -= (videoScreen.volume == 0 ? 0 : 0.1);
		videoWebcam.volume -= (videoWebcam.volume == 0 ? 0 : 0.1);

	} 
	videoScreen.volume = parseFloat(videoScreen.volume).toFixed(1);
	videoWebcam.volume = parseFloat(videoWebcam.volume).toFixed(1);
}

// Toggles the media player's mute and unmute status
function toggleMute() {
	if (videoScreen.muted) {
		// Change the cutton to be a mute button
		changeButtonType(muteBtn, 'mute');
		// Unmute the media player
		videoScreen.muted = false;
		videoWebcam.muted = false;
	}
	else {
		// Change the button to be an unmute button
		changeButtonType(muteBtn, 'unmute');
		// Mute the media player
		videoScreen.muted = true;
		videoWebcam.muted = true;
	}
}

// Replays the media currently loaded in the player
function replayMedia() {
	resetPlayer();
	videoScreen.play();
	videoWebcam.play();
}
// Updates a button's title, innerHTML and CSS class to a certain value
function changeButtonType(btn, value) {
	btn.title = value;
	btn.innerHTML = value;
	btn.className = value;
}

// Resets the media player
function resetPlayer() {
	// Reset the progress bar to 0
	progressBar.value = 0;
	// Move the media back to the start
	videoScreen.currentTime = 0;
	videoWebcam.currentTime = 0;
	// Ensure that the play pause button is set as 'play'
	changeButtonType(playPauseBtn, 'play');
}

function changeBiggerVideo(buttonId){
		console.log("changeBiggerVideo: ", buttonId);

		if (buttonId == biggerVideo) {
			return;
		}

		if (buttonId == "webcam") {
			videoWebcam.jquery.removeClass("lesserVideo");
			videoWebcam.jquery.addClass("biggerVideo");
			videoScreen.jquery.removeClass("biggerVideo");
			videoScreen.jquery.addClass("lesserVideo");
			biggerVideo = "webcam";
		} else {
			videoScreen.jquery.removeClass("lesserVideo");
			videoScreen.jquery.addClass("biggerVideo");
			videoWebcam.jquery.removeClass("biggerVideo");
			videoWebcam.jquery.addClass("lesserVideo");
			biggerVideo = "screen";
		}
}