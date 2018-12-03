
console.log('got it');

var wavesurfer = WaveSurfer.create({
 // Use the id or class-name of the element you created, as a selector
 container: '#wavesurfer-waveform',
 // The color can be either a simple CSS color or a Canvas gradient
 waveColor: 'grey',
 progressColor: 'black',
 cursorColor: 'black',
 // This parameter makes the waveform look like SoundCloud's player
 barWidth: 1,
 normalize: true
});

wavesurfer.load('/static/audio/1/1/00035_EdmeeGarcia_AutorreferenteSoySuFan_2013_EDGA_EDGA_4.mp3');

wavesurfer.on('ready', function () {
    wavesurfer.play();
});