function createWaveSurferElement(containerId, audioFilepath, waveformPeaks) {

    var peaksId = containerId + "-peaks",
        timeRemainingId = containerId + "-time-remaining",
        timeCurrentId = containerId + "-time-current",
        timeTotalId = containerId + "-time-total";


    var rootElement = document.getElementById(containerId);

    var waveFormDiv = document.createElement("div");
    rootElement.appendChild(waveFormDiv);

    waveFormDiv.classList.add("row");
    var innerWaveFormDiv = document.createElement("div");
    waveFormDiv.appendChild(innerWaveFormDiv);
    innerWaveFormDiv.id = peaksId;

    var wavesurfer = WaveSurfer.create({
        // Use the id or class-name of the element you created, as a selector
        container: "#" + peaksId,
        backend: "MediaElement",
        // The color can be either a simple CSS color or a Canvas gradient
        waveColor: "grey",
        progressColor: "black",
        cursorColor: "grey",
        // This parameter makes the waveform look like SoundCloud"s player
        barWidth: 2,
        normalize: true
    });

    if (waveformPeaks != null) {
        wavesurfer.load(audioFilepath, waveformPeaks);
    } else {
        wavesurfer.load(audioFilepath);
    }

    var buttonsDiv = document.createElement("div");
    rootElement.appendChild(buttonsDiv);
    buttonsDiv.classList.add("row");
    var playDiv = document.createElement("div");

    buttonsDiv.appendChild(playDiv);
    playDiv.classList.add('col-md-2');
    playDiv.classList.add('text-center');

    var playButton = document.createElement("button");
    playDiv.appendChild(playButton);

    playButton.innerHTML = "&#9658";
    playButton.onclick = function() { wavesurfer.playPause(); };

    var volumeDiv = document.createElement("div");
    buttonsDiv.appendChild(volumeDiv);

    volumeDiv.classList.add('col-md-8');

    var volumeSlider = document.createElement('input');
    volumeDiv.appendChild(volumeSlider);
    volumeSlider.type = "range";
    volumeSlider.max = "0";
    volumeSlider.max = "1";
    volumeSlider.step = "0.01";

    var timeDiv = document.createElement('div'),
        remainingSpan = document.createElement('span'),
        currentSpan = document.createElement('span'),
        totalSpan = document.createElement('span');

    timeDiv.classList.add('col-md-2');
    timeDiv.classList.add('text-left');
    var spanClass = 'time-span';
    totalSpan.classList.add(spanClass);
    currentSpan.classList.add(spanClass);
    remainingSpan.classList.add(spanClass);

    remainingSpan.id = timeRemainingId;
    currentSpan.id = timeCurrentId;
    totalSpan.id = timeTotalId;

    buttonsDiv.appendChild(timeDiv);
    timeDiv.appendChild(remainingSpan);
    timeDiv.appendChild(currentSpan);
    timeDiv.appendChild(totalSpan);


    wavesurfer.on('ready', function () {

        wavesurfer.setVolume(0.5);

        volumeSlider.value = wavesurfer.backend.getVolume();


        var totalTime = wavesurfer.getDuration(),
            currentTime = Math.round(wavesurfer.getCurrentTime()),
            remainingTime = Math.round(totalTime - currentTime);


        document.getElementById(timeCurrentId).innerText = currentTime;
        document.getElementById(timeTotalId).innerText = Math.round(totalTime);
        document.getElementById(timeRemainingId).innerText = remainingTime;

        var onChangeVolume = function (e) {
            wavesurfer.setVolume(e.target.value);
        };

        volumeSlider.addEventListener('input', onChangeVolume);
        volumeSlider.addEventListener('change', onChangeVolume);

    });

    wavesurfer.on('audioprocess', function() {
        if(wavesurfer.isPlaying()) {
            var totalTime = wavesurfer.getDuration(),
                currentTime = Math.round(wavesurfer.getCurrentTime()),
                remainingTime = Math.round(totalTime - currentTime);


            document.getElementById(timeCurrentId).innerText = currentTime;
            document.getElementById(timeTotalId).innerText = Math.round(totalTime);
            document.getElementById(timeRemainingId).innerText = remainingTime;
        }
    });
}

for (var i = 0; i < audioIterator.waveformPeaks.length; i++) {
    createWaveSurferElement(
        audioIterator.containersIds[i],
        audioIterator.audioPaths[i],
        audioIterator.waveformPeaks[i]);
}

