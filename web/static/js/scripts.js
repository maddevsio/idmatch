var width = 480;
var height = 0;

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var startbutton = null;
var streamObj = null;

$(function () {
    $("#typed").typed({
        stringsElement: $('#typed-strings'),
        typeSpeed: -40,
        startDelay: 0.5,
        cursorChar: "&block;",
        callback: function() {
            $('.typed-cursor').hide();
            var timer = setInterval(
                function(){
                    clearInterval(timer);
                    $('.json_wrap').show();
                    $('.inst-info').fadeIn('slow');
                }, 50
            );
        }
    });
});

function addphoto(image) {
    $('#webcam-face').val(image);
}

$(function () {
    $('#face').change(function () {
        var fileName = $(this).val();
        var photo_label = $(this).closest('#photo').find(".filename");
        fileName = fileName.replace('C:\\fakepath\\','') ;
        if(!fileName){
            photo_label.removeClass('add_item');
            fileName = photo_label.data('message');
            $('#arrows').removeClass('animate');
            $('.my_scan').addClass('disabled');
            $('#arrows_dock').removeClass('animate');
            $('.submit').addClass('disabled');
            $('#id').attr('disabled', true);
            $('#submit_btn').attr('disabled', true);
        }else{
            photo_label.addClass('add_item');
            $('#arrows').addClass('animate');
            $('.my_scan').removeClass('disabled');
            $('#id').removeAttr('disabled')
        }
        photo_label.html(fileName);
        $('#id').trigger('change');
    });
    $('#id').change(function () {
        var fileName = $(this).val();
        var webcam = $('#webcam-face').val();
        console.log(webcam);
        var dock_label = $(this).closest('#document').find(".filename");
        var photo_val = $('#face').val();
        fileName = fileName.replace('C:\\fakepath\\','');
        if(!fileName && photo_val){
            console.log('043434343434343-');
            dock_label.removeClass('add_item');
            fileName = dock_label.data('message');
            $('#arrows_dock').removeClass('animate');
            $('.submit').addClass('disabled');
            $('#submit_btn').attr('disabled', true);
        }
        else if (!fileName && webcam){
            console.log('0-0-0-0-0-0-0-0-0-0-');
            fileName = dock_label.data('message');
            $('.submit').addClass('disabled');
            $('#submit_btn').attr('disabled', true);
            $('#arrows_dock').removeClass('animate');
        }
        else if(webcam && fileName){
            console.log('-=--=-=-==-=-=-=-=-=-=');
            dock_label.addClass('add_item');
            $('.submit').removeClass('disabled');
            $('#submit_btn').removeAttr('disabled');
            $('#arrows_dock').addClass('animate');
        }
        else if(photo_val){
            console.log('1232321312321321');
            dock_label.addClass('add_item');
            $('#arrows_dock').addClass('animate');
            $('.submit').removeClass('disabled');
            $('#submit_btn').removeAttr('disabled');
        }
        dock_label.html(fileName);
    });
    $('label').click(function (e) {
        var photo_val = $('#face').val();
        var id_val = $('#id').val();
        if($(e.target).closest('div').find('input').attr('disabled')){
            if(!photo_val && !id_val){
                $('#photo').effect( "shake" );
            } else if(!id_val){
                $('#document').effect( "shake" );
            } else if(!photo_val){
                $('#photo').effect( "shake" );
            }
        }
    });
    $('.submit label').click(function (e) {
        if($(e.target).closest('div').find('input').attr('disabled')){
        } else{
            $('.submit_icon').addClass('submit_rotate');
        }
    });
});

function getPercentClass(percent) {
    if(percent <= 50) {
        return 'failed';
    }else if(percent <= 70){
        return 'normal';
    }
    return 'correct';
}

function initWebcam() {

    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function (stream) {
            streamObj = stream;
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err) {
            console.log("An error occured! " + err);
        });

    video.addEventListener('canplay', function (ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);

    startbutton.addEventListener('click', function (ev) {
        takepicture();
        ev.preventDefault();
    }, false);

    function clearphoto() {
        var context = canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);
        addphoto('');
    }
    function takepicture() {
        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);
        } else {
            clearphoto();
        }
    }

}

function stopWebcam() {
    streamObj.getTracks().forEach(track => track.stop());
}

$(function () {
   var percent = parseInt($('.match-percent').text());
   $('.results-images').addClass(getPercentClass(percent));
});

$(function () {
    $('#open_takePhoto').click(function () {
        $('#takePhoto').fadeIn();
        initWebcam();
    });
    $('#startbutton').click(function () {
        $('.camera').addClass('flesh-animation').delay(800).queue(function(){
           $(this).removeClass('flesh-animation').dequeue();
        });
        $('#canvas').show();
        $('#apply, #cancel').addClass('show');
    });
    $('#cancel').click(function () {
        $('#canvas').hide();
        $('#apply, #cancel').removeClass('show');
    });
    $('#apply').click(function () {
        var data = $('#canvas')[0].toDataURL('image/png');
        addphoto(data);
        $('#takePhoto').fadeOut();
        $('#arrows').addClass('animate');
        $('.my_scan').removeClass('disabled');
        $('#id').removeAttr('disabled');
        if(video){
            stopWebcam();
        }
    });
    $('#close_modal').click(function () {
        $('#takePhoto').fadeOut();
        if(video){
            stopWebcam();
        }
    })
});