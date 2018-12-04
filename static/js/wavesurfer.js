
var wavesurfer = WaveSurfer.create({
    // Use the id or class-name of the element you created, as a selector
    container: '#wavesurfer-waveform',
    // The color can be either a simple CSS color or a Canvas gradient
    waveColor: 'grey',
    progressColor: 'black',
    cursorColor: 'grey',
    // This parameter makes the waveform look like SoundCloud's player
    barWidth: 1,
    normalize: true
});

wavesurfer.load(audio_file);

wavesurfer.on('ready', function () {

    wavesurfer.setVolume(0.4);
    document.querySelector('#volume').value = wavesurfer.backend.getVolume();

    var volumeInput = document.querySelector('#volume');
    var onChangeVolume = function (e) {
      wavesurfer.setVolume(e.target.value);
      console.log(e.target.value);
    };

    volumeInput.addEventListener('input', onChangeVolume);
    volumeInput.addEventListener('change', onChangeVolume);

    wavesurfer.play();
});