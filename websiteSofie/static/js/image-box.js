window.imageBox = {
    currentSlide: -1,
    goto: function(index) {
        var slides = document.querySelectorAll(".image-box__largeslide");
        window.imageBox.currentSlide = index;
        for(var i = 0; i < slides.length; i++) {
            if(slides[i].hasClass("current-slide")) slides[i].removeClass("current-slide");
            if(i==window.imageBox.currentSlide) slides[i].addClass("current-slide");
        }
    },
    initialize: function() {
        var slides = document.querySelectorAll(".image-box__slide");
        for(var i = 0; i < slides.length; i++) {
            slides[i].tap((function() {
                window.imageBox.goto(this);
            }).bind(i));
        }
    }
}
window.imageBox.initialize();
window.imageBox.goto(0);
